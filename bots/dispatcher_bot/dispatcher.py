# bots/dispatcher_bot/dispatcher.py

import requests
import json
from settings import ORS_API_KEY # Assuming settings.py is correctly imported
from bots.dispatcher_bot.models import DeliveryJob, DriverStatus, Route
from typing import List, Optional, Tuple, Dict, Any

# NOTE: For this script to run, you must ensure 'settings.py' (from infrastructure/config)
# is accessible, likely by configuring Python's path or by running the bot as a microservice.

class Dispatcher:
    def __init__(self):
        self.ors_base_url = "https://api.openrouteservice.org/v2/directions"
        print("Dispatcher Bot initialized. Matching algorithm ready.")

    def _simulate_db_query(self, location: Tuple[float, float]) -> List[DriverStatus]:
        """
        Simulates database lookup for active, nearby, and verified TRUCK drivers (F-150, etc.).
        """
        # Phase 1: Charlotte, NC Area (Example Coordinates)
        print(f"Searching DB for active drivers near {location}...")
        
        return [
            # Driver 1: Closer to Uptown (35.2271, -80.8431)
            DriverStatus(id=101, location=(35.2300, -80.8500), capacity=250.0, rating=4.9, is_active=True), 
            # Driver 2: Closer to University Area (35.3050, -80.7300)
            DriverStatus(id=102, location=(35.2900, -80.7500), capacity=180.0, rating=4.5, is_active=True), 
        ]

    def optimize_route(self, start_loc: Tuple[float, float], end_loc: Tuple[float, float]) -> Route:
        """
        Uses OpenRouteService (ORS) API (simulated) to calculate distance and duration.
        The goal is to minimize the distance from the driver's current location to the pickup point (empty miles).
        """
        print("Calculating route via ORS API...")
        
        # --- ORS API Call Simulation (Replace with actual request in live system) ---
        
        try:
            # Format: longitude,latitude
            start_str = f"{start_loc[1]},{start_loc[0]}"
            end_str = f"{end_loc[1]},{end_loc[0]}"
            
            # Simulated calculation based on a simple distance metric for demo
            
            # Haversine distance calculation (simple approximation)
            import math
            R = 6371 # Earth radius in km
            d_lat = math.radians(end_loc[0] - start_loc[0])
            d_lon = math.radians(end_loc[1] - start_loc[1])
            a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
                 math.cos(math.radians(start_loc[0])) * math.cos(math.radians(end_loc[0])) * math.sin(d_lon / 2) * math.sin(d_lon / 2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance_km = R * c
            
            # Simple duration estimation (e.g., 60 km/h average speed)
            duration_minutes = (distance_km / 60.0) * 60.0
            
            return Route(distance_km=distance_km, duration_minutes=duration_minutes)

        except Exception as e:
            # Fallback if external API fails
            print(f"Warning: ORS simulation failed. Using default fallback. Error: {e}")
            return Route(distance_km=10.0, duration_minutes=15.0)


    def match_job(self, job: DeliveryJob) -> Dict[str, Any]:
        """
        Core AI Matching Algorithm: Finds the driver with the lowest 'Empty Miles'
        that meets capacity requirements.
        """
        drivers = self._simulate_db_query(job.pickup_location)
        best_match: Optional[Tuple[DriverStatus, Route, float]] = None
        min_empty_miles = float('inf')

        for driver in drivers:
            if not driver.is_active or driver.capacity < job.required_capacity:
                continue

            # Route from Driver's current location to Pickup point (Empty Miles)
            route_to_pickup = self.optimize_route(driver.location, job.pickup_location)
            
            empty_miles = route_to_pickup.distance_km 
            
            if empty_miles < min_empty_miles:
                min_empty_miles = empty_miles
                best_match = (driver, route_to_pickup, min_empty_miles)

        if best_match:
            driver, route, empty_miles = best_match
            print(f"\n✅ MATCH FOUND! Driver ID: {driver.id} selected.")
            print(f"   -> Empty Miles: {empty_miles:.2f} km")
            
            # Send job alert to driver's app API here
            
            return {
                "driver_id": driver.id,
                "status": "MATCHED",
                "empty_miles_km": round(empty_miles, 2)
            }
        
        return {"status": "NO_MATCH_FOUND", "message": "No suitable truck found in the area."}


if __name__ == '__main__':
    # --- Example Execution ---
    # NOTE: You must have a basic 'settings.py' file available for this to run!
    
    dispatcher = Dispatcher()
    
    # Mock Job: Pickup in Uptown Charlotte, req capacity 100 sqft
    job_request = DeliveryJob(
        id=1, 
        pickup_location=(35.2271, -80.8431), # Uptown Charlotte
        dropoff_location=(35.3500, -80.7000), # Heading northeast
        base_price=65.00,
        required_capacity=100.0,
        is_express=True
    )
    
    match_result = dispatcher.match_job(job_request)
    print("\n--- Dispatcher Result ---")
    print(json.dumps(match_result, indent=4))
