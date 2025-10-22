# apps/driver_app_api/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from settings import DISPATCHER_URL, LEGAL_URL

app = FastAPI(title="PickupLink Driver API")

class DriverRegistration(BaseModel):
    license_number: str
    truck_plate: str
    vehicle_type: str
    insurance_status: bool

@app.post("/register")
def register_driver(data: DriverRegistration):
    """Initial driver registration and truck verification."""
    # 1. Check TRUCKS ONLY compliance via Legal Bot
    legal_response = requests.post(f"{LEGAL_URL}/verify_truck", json={"vehicle_type": data.vehicle_type})
    
    if legal_response.json().get("status") != "SUCCESS":
        raise HTTPException(status_code=400, detail="Registration failed: Vehicle is not an approved truck type.")

    # 2. Register driver in the database (simulated)
    # db_insert(data)
    
    return {"status": "SUCCESS", "driver_id": 9000, "message": "Truck verified and driver registered."}

@app.put("/status")
def update_driver_status(driver_id: int, lat: float, lon: float, is_active: bool):
    """Updates driver's location and active status for Dispatcher Bot."""
    # Sends data directly to the Dispatcher Bot for real-time matching
    requests.post(f"{DISPATCHER_URL}/update_location", json={"driver_id": driver_id, "lat": lat, "lon": lon})
    return {"status": "Updated", "active": is_active}

# ... (Routes for /job_accept, /job_complete, etc.)
