"""Regression coverage for the audit, input handling, and standalone browser demonstration."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from pydantic import ValidationError

from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from agents.llm_factory import LLMFactory
from cli import _safe_resolve_path
from radiogenomics_sentinel.cli import _safe_resolve_path as frontier_safe_resolve_path


def test_hmac_detects_record_tampering_and_broken_links():
    audit = AuditTrail(secret_key="test-only-32-byte-secret")
    first = audit.log("worker", "system", "STARTED", {"count": 1})
    audit.log("worker", "system", "FINISHED", {"count": 2})
    assert audit.verify_integrity()
    audit.logs[0]["actor"] = "impostor"
    assert not audit.verify_integrity()
    audit.logs[0]["actor"] = "worker"
    assert audit.verify_integrity()
    audit.logs[1]["current_hash"] = "0" * 64
    assert not audit.verify_integrity()
    audit.logs[1]["current_hash"] = "restored-invalid-value"
    assert not audit.verify_integrity()
    # Modifying the returned snapshot must not modify the audit.
    snapshot = audit.get_trail()
    snapshot[0]["actor"] = "external"
    assert audit.logs[0]["actor"] == "worker"


def test_hmac_snapshot_does_not_mutate_chain():
    audit = AuditTrail(secret_key="test-only-key")
    audit.log("worker", "system", "STARTED", {"count": 1})
    snapshot = audit.get_trail()
    snapshot[0]["current_hash"] = "tampered"
    assert audit.verify_integrity()


@pytest.mark.parametrize("bad_path", [
    "../outside.csv",
    r"..\\..\\outside.csv",
    r"C:\\sensitive\\data.csv",
    r"\\\\server\\share\\data.csv",
])
def test_path_containment_rejects_cross_platform_traversal(bad_path):
    for resolver in (_safe_resolve_path, frontier_safe_resolve_path):
        with pytest.raises(ValueError, match="Path traversal detected"):
            resolver(bad_path)


def test_nearby_legitimate_file_is_allowed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for resolver in (_safe_resolve_path, frontier_safe_resolve_path):
        assert resolver("input.csv") == tmp_path / "input.csv"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_numbers_rejected(value):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T", target_identifier="KEY", primary_metric=value)
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T", target_identifier="KEY", primary_metric=1.0, secondary_metric=value)


def test_nested_phi_is_rejected_before_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="T", target_identifier="KEY", primary_metric=1,
        attributes={"metadata": {"contact": "alice@example.org"}},
    )
    with pytest.raises(SecurityException):
        supervisor.process_task(payload)


def test_nonexistent_llm_providers_do_not_claim_support():
    with pytest.raises(ValueError, match="only mock"):
        LLMFactory.create("openai")
    assert "No clinical or scientific verification" in LLMFactory.create("mock").invoke("demo test")


@pytest.mark.skipif(shutil.which("node") is None, reason="Node required for browser JavaScript check")
def test_static_web_javascript_and_rule_parity(tmp_path):
    html = (Path(__file__).parent.parent / "web" / "index.html").read_text()
    assert "no API requests" in html
    assert "Signed audit blocks" in html
    assert "HMAC_SHA256_e83f" not in html
    assert "fetch('/api/audit'" not in html
    script = re.search(r"<script>(.*?)</script>", html, re.DOTALL).group(1)
    path = tmp_path / "app.js"
    path.write_text(script)
    syntax = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
    assert syntax.returncode == 0, syntax.stderr
    harness = (
        "const vm=require('node:vm');const fs=require('node:fs');"
        "const src=fs.readFileSync(process.argv[1],'utf8');"
        "const context={document:{getElementById:()=>({addEventListener(){}})}};"
        "vm.createContext(context);vm.runInContext(src,context);"
        "const base={task_id:'T',target_identifier:'KEY',primary_metric:10,"
        "secondary_metric:4,status_descriptor:'NOMINAL',is_critical_flag:false};"
        "const out=[context.evaluate(base),context.evaluate({...base,primary_metric:30}),"
        "context.evaluate({...base,is_critical_flag:true})];"
        "process.stdout.write(JSON.stringify(out));"
    )
    execution = subprocess.run(["node", "-e", harness, str(path)], capture_output=True, text=True)
    assert execution.returncode == 0, execution.stderr
    normal, warning, critical = json.loads(execution.stdout)
    assert normal["overall_urgency"] == "ROUTINE"
    assert warning["overall_urgency"] == "ELEVATED_RISK"
    assert critical["overall_urgency"] == "CRITICAL_STAT_PANIC"
    assert not any("audit_hash" in result for result in (normal, warning, critical))


def test_api_success_and_safe_sensitive_input_failure():
    from fastapi.testclient import TestClient
    from agents.api import app

    client = TestClient(app)
    response = client.post("/api/audit", json={
        "task_id": "SYNTHETIC-T",
        "target_identifier": "MODEL-1",
        "primary_metric": 30.0,
        "secondary_metric": 4.0,
    })
    assert response.status_code == 200
    dossier = response.json()
    assert dossier["overall_urgency"] == "ELEVATED_RISK"
    assert dossier["audit_hash"]
    assert client.get("/api/audit/logs").json()["verified"] is True

    bad = client.post("/api/audit", json={
        "task_id": "SYNTHETIC-T",
        "target_identifier": "person@example.org",
        "primary_metric": 1.0,
    })
    assert bad.status_code == 400
    assert "person@example.org" not in bad.text

    nested = client.post("/api/audit", json={
        "task_id": "SYNTHETIC-T",
        "target_identifier": "MODEL-1",
        "primary_metric": 1.0,
        "attributes": {"contact": "person@example.org"},
    })
    assert nested.status_code == 400
    assert "person@example.org" not in nested.text


def test_benchmark_cases_remain_consistent():
    from agents.base import PHIGuard
    from agents.models import SystemIntegrityStatus, UrgencyLevel
    data = json.loads((Path(__file__).parent.parent / "benchmark_dataset.json").read_text())
    supervisor = SystemSupervisor(model_provider="mock")
    for case in data["test_cases"]:
        if case.get("expected_security_exception"):
            with pytest.raises(SecurityException):
                PHIGuard.assert_no_phi(case["adversarial_prompt"])
        else:
            output = supervisor.process_task(SystemTaskPayload(**case["payload"]))
            assert output.overall_urgency.value == case["expected_urgency"]
            assert output.integrity_status.value == case["expected_integrity"]
