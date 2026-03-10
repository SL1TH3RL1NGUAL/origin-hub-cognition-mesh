from pydantic import BaseModel, Field
from typing import Any, List, Dict
import uuid
from datetime import datetime


class Observation(BaseModel):
    """
    Canonical unit of reality entering the cognition mesh.
    """
    obs_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_origin: str
    payload_type: str  # RF | JSON | TELEMETRY | HUMAN_PROMPT
    raw_data: Any
    context_stack: List[str] = []


class Insight(BaseModel):
    """
    Output of a lab_pod agent_unit.
    """
    insight_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    obs_id: str
    lab_pod_id: str
    summary: str
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
