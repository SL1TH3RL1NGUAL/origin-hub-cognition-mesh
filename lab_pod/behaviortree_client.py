import os
import uuid
from typing import Dict, Any
import redis
import json
from datetime import datetime

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class BehaviorTreeClient:
    """
    MVP Redis-backed behavior tree client.
    Stores insights and returns static behavior branches for now.
    """

    def __init__(self):
        self.r = redis.from_url(REDIS_URL, decode_responses=True)

    async def get_applicable_nodes(self, observation: Dict) -> Dict:
        """
        MVP behavior lookup.
        Later this will query RedisGraph or RedisJSON.
        """
        return {
            "strategy": "default",
            "notes": "MVP behavior branch",
            "observation_type": observation.get("payload_type"),
        }

    async def append_insight(self, observation: Dict, insight_payload: Dict) -> Dict:
        """
        Store a new insight in Redis.
        """
        insight_id = f"insight:{uuid.uuid4()}"
        doc = {
            "insight_id": insight_id,
            "obs_id": observation["obs_id"],
            "summary": insight_payload["summary"],
            "metadata": insight_payload.get("metadata", {}),
            "created_at": datetime.utcnow().isoformat(),
        }

        self.r.set(insight_id, json.dumps(doc))
        return doc
