"""
FastAPI REST API Server for RadioGenomics Sentinel: PyRadiomics Feature & Somatic Mutation Association Agent.
"""
from typing import Dict, Any
from .models import FrontierPayload
from .agents import RadioGenomicsCoordinator

coordinator = RadioGenomicsCoordinator()


def create_app():
    try:
        from fastapi import FastAPI, Request
        from pydantic import BaseModel

        app = FastAPI(
            title="RadioGenomics Sentinel: PyRadiomics Feature & Somatic Mutation Association Agent",
            description="Evaluates illustrative numeric thresholds and descriptor keywords; no radiomic extraction or genomic association analysis.",
            version="2.0.0-FRONTIER",
        )

        # Security headers middleware
        @app.middleware("http")
        async def add_security_headers(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Cache-Control"] = "no-store"
            return response

        class TaskRequest(BaseModel):
            task_id: str = "TASK-2026-001"
            target_identifier: str = "TARGET-BIO-KEY"
            primary_metric: float = 28.5
            secondary_metric: float = 14.2
            status_descriptor: str = "DISCORDANT_ANOMALY"
            is_critical_flag: bool = True
            attributes: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "radiogenomics-imaging-genomics-agent", "domain": "Biomedical Scientific Discovery & Multi-Omics", "version": "2.0.0-FRONTIER"}

        @app.post("/api/audit")
        def api_audit(req: TaskRequest):
            payload = FrontierPayload(
                task_id=req.task_id,
                target_identifier=req.target_identifier,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_descriptor=req.status_descriptor,
                is_critical_flag=req.is_critical_flag,
                attributes=req.attributes,
            )
            return coordinator.process(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
