# apps/client_app_api/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from settings import DISPATCHER_URL, FINANCE_URL

app = FastAPI(title="PickupLink Client API")

class DeliveryRequest(BaseModel):
    pickup_coords: tuple
    dropoff_coords: tuple
    required_capacity: float
    is_express: bool = False
    client_id: int

@app.post("/jobs/create")
def create_job(request: DeliveryRequest):
    """Submits a new delivery request to the Dispatcher Bot."""
    print(f"Client {request.client_id} submitted new job.")
    
    # 1. Calculate preliminary price (Simplification: Fixed rate per km)
    # (In a real system, this would call the Dispatcher/Finance for dynamic pricing)
    preliminary_price = 50.00 # Placeholder base price
    
    job_data = request.dict()
    job_data['base_price'] = preliminary_price
    
    # 2. Forward the request to the Dispatcher Bot for matching
    try:
        dispatcher_response = requests.post(f"{DISPATCHER_URL}/match_job", json=job_data)
        dispatcher_response.raise_for_status()
        match_result = dispatcher_response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Dispatcher service unavailable: {e}")

    return {"status": "Job Submitted", "job_id": 9001, "match_info": match_result}

@app.get("/jobs/{job_id}/track")
def track_job(job_id: int):
    """Retrieves real-time status and location of a job."""
    # This would query the Dispatcher Bot or the main DB
    # Simulation:
    return {"job_id": job_id, "status": "EN_ROUTE", "driver_location": (35.25, -80.8)}

@app.post("/jobs/{job_id}/invoice")
def process_invoice(job_id: int):
    """Triggers final fee calculation and invoicing via Finance Bot."""
    # Sends job completion data to Finance Bot
    try:
        finance_response = requests.post(f"{FINANCE_URL}/process_invoice", json={"job_id": job_id})
        finance_response.raise_for_status()
        return {"status": "Invoicing Complete", "details": finance_response.json()}
    except:
        raise HTTPException(status_code=500, detail="Finance Bot processing failed.")
