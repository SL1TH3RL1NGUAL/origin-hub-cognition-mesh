import requests
import uuid

obs = {
    "obs_id": str(uuid.uuid4()),
    "source_origin": "origin://rf-gateway-demo",
    "payload_type": "RF",
    "raw_data": {"signal_strength": -42, "frequency": "2.4GHz"},
    "context_stack": []
}

resp = requests.post("http://localhost:8000/observe", json=obs)
print("Status:", resp.status_code)
print("Insights:", resp.json())
