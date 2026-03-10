# Origin Hub Cognition Mesh

A distributed cognition fabric that transforms every RF/API/telemetry/human signal into a compounding insight asset.

This repository contains the full skeleton of the **Origin Hub Cognition Mesh**, including:

- `origin_hub` — primary ingress for all signals  
- `insightproxylayer` — generative reverse proxy + NATS fan‑out  
- `lab_pod` — distributed micro‑cognition nodes  
- `globalbehaviortree` — Redis/RedisGraph‑backed shared memory  
- `examples` — end‑to‑end mesh test harness  
- `docker-compose.yml` — full local mesh orchestration  

The system is designed to **learn from its own traffic**, building a proprietary behavior tree that deepens over time.

---

## ✨ High‑Level Architecture

```text
[ Clients / Devices / RF Sources ]
                |
        [ origin_hub ]
                |
        [ insightproxylayer ]
        /          |           \
   [lab_pod A] [lab_pod B] ... [lab_pod N]
        \          |           /
         \         |          /
          [ globalbehaviortree DB ]
