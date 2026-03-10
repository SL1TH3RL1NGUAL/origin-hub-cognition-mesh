from typing import Any, Dict
from .behaviortree_client import BehaviorTreeClient


class AgentUnit:
    """
    Minimal cognitive unit inside a lab_pod.
    Handles:
      - Behavior lookup
      - Model invocation (placeholder for now)
      - Insight generation
    """

    def __init__(self, agent_id: str, behavior_client: BehaviorTreeClient):
        self.agent_id = agent_id
        self.behavior_client = behavior_client

    async def generate_insight(self, data: Any, guidance: Dict) -> Dict:
        """
        Placeholder "thinking" logic.
        This is where LLM calls or local model inference would go.
        """
        return {
            "summary": f"Agent {self.agent_id} processed payload of type {type(data).__name__}",
            "metadata": {
                "guidance_used": guidance,
            },
        }


async def process_observation(
    observation: Dict,
    agent: AgentUnit,
    bt_client: BehaviorTreeClient
) -> Dict:
    """
    Core conceptual agent logic:
      1. Fetch relevant behavior branches
      2. Execute agent logic
      3. Commit insight back to the mesh
    """

    # 1. Behavior lookup
    behaviors = await bt_client.get_applicable_nodes(observation)

    # 2. Generate insight
    insight_payload = await agent.generate_insight(
        data=observation.get("raw_data"),
        guidance=behaviors,
    )

    # 3. Commit to global behavior tree
    insight = await bt_client.append_insight(observation, insight_payload)
    return insight
