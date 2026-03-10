import asyncio
import json
import os

import nats

from .behaviortree_client import BehaviorTreeClient
from .agent_runtime import AgentUnit, process_observation
from .schemas import Observation


NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
LAB_POD_ID = os.getenv("LAB_POD_ID", "lab_pod_unknown")


async def main():
    nc = await nats.connect(NATS_URL)
    bt_client = BehaviorTreeClient()
    agent = AgentUnit(agent_id=f"agent:{LAB_POD_ID}:001", behavior_client=bt_client)

    async def message_handler(msg):
        observation = json.loads(msg.data.decode())
        obs_id = observation["obs_id"]

        # Process observation → generate insight
        insight_doc = await process_observation(observation, agent, bt_client)
        insight_doc["lab_pod_id"] = LAB_POD_ID

        # Publish insight back to the proxy layer
        await nc.publish(
            f"mesh.insight.out.{obs_id}",
            json.dumps(insight_doc).encode()
        )

    # Subscribe to mesh observation stream
    await nc.subscribe("mesh.observation.in", cb=message_handler)

    print(f"{LAB_POD_ID} listening on mesh.observation.in")

    # Keep worker alive
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
