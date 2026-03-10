# Origin Hub Cognition Mesh – Architecture

## 1. High-level overview

The Origin Hub Cognition Mesh is a distributed cognition fabric that:

- Sits in front of existing infrastructure (RF, APIs, devices).
- Normalizes all signals into `Observation` objects.
- Fans them out to `lab_pod`s via NATS.
- Uses a global behavior tree (Redis/RedisGraph) as shared memory.
- Returns enriched `Insight`s to callers via the `insightproxylayer`.

```text
[ Clients / Devices / RF Sources ]
                |
         (over the air)
                |
        [ origin_hub ]
                |
        [ insightproxylayer ]
        /          |           \
   [lab_pod A] [lab_pod B] ... [lab_pod N]
        \          |           /
         \         |          /
          [ globalbehaviortree DB ]
