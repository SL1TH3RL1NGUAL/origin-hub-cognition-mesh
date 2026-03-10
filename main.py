import asyncio
import json
import os
from typing import List

import nats
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from schemas import Observation, Insight

NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")

app = FastAPI(title="Insight Proxy Layer")

@app.on_event("startup")
async def startup_event():
    app.state.nc = await nats.connect(NATS_URL)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.nc.drain()

@app.post("/observe", response_model=List[Insight])
async def observe(observation: Observation):
    nc = app.state.nc
    obs_dict = observation.dict()
    obs_id = observation.obs_id

    # Publish observation to mesh
    await nc.publish("mesh.observation.in", json.dumps(obs_dict).encode())

    # Listen for insights on a dedicated subject
    subject = f"mesh.insight.out.{obs_id}"
    insights: List[Insight] = []

    async def _collect_insights():
        sub = await nc.subscribe(subject)
        try:
            # naive: collect for 500ms
            try:
                while True:
                    msg = await asyncio.wait_for(sub.next_msg(), timeout=0.5)
                    data = json.loads(msg.data.decode())
                    insights.append(Insight(**data))
            except asyncio.TimeoutError:
                pass
        finally:
            await sub.unsubscribe()

    await _collect_insights()
    return JSONResponse([i.dict() for i in insights])
