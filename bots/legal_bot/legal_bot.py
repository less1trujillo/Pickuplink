# bots/legal_bot/legal_bot.py

import requests
import json
from settings import LEGAL_URL, PHASE, TRUCKS_ONLY_ENABLED

class LegalBot:
    def __init__(self):
        print(f"LegalBot Initialized. Compliance mode: Phase {PHASE}.")
        
    def verify_truck_compliance(self, registration_data: dict) -> dict:
        """
        CRITICAL function: Ensures the vehicle is a registered truck and not a sedan/SUV.
        This enforces the 'TRUCKS ONLY' core principle.
        """
        if not TRUCKS_ONLY_ENABLED:
            return {"status": "SUCCESS", "message": "TRUCKS_ONLY rule is disabled (dev mode)."}

        vehicle_type = registration_data.get('vehicle_type', '').upper()
        plate = registration_data.get('plate', 'N/A')
        
        # --- AI/Database Lookup Simulation (External API Check) ---
        # In a real app, this integrates with state/national DMV APIs.
        
        # Basic filter check: Must contain keywords associated with pickup trucks
        if any(keyword in vehicle_type for keyword in ["PICKUP", "TRUCK", "F-150", "RAM", "SILVERADO", "TUNDRA"]):
            print(f"Truck Verified: Plate {plate}, Type: {vehicle_type}")
            return {"status": "SUCCESS", "is_truck": True, "liability_checked": True}
        else:
            print(f"VERIFICATION FAILED: Vehicle {vehicle_type} is not a valid truck type.")
            # Trigger a block on the Dispatcher/Driver API
            return {"status": "FAILED", "is_truck": False, "message": "Vehicle is not an approved truck type."}

    def verify_insurance_and_license(self, driver_data: dict) -> bool:
        """Ensures all independent driver documentation is valid."""
        license_status = driver_data.get('license_status', 'INVALID')
        insurance_valid = driver_data.get('insurance_status', False)
        
        if license_status == 'VALID' and insurance_valid:
            print("Driver license and insurance verified. Zero direct liability confirmed.")
            return True
        else:
            print("WARNING: Driver documentation incomplete or invalid.")
            return False

    def get_terms_of_service(self, region: str) -> str:
        """
        Adapts the Terms of Service based on regional compliance needs (e.g., California vs. NC).
        """
        # This function would use an LLM or a localized DB to generate the appropriate legal text.
        if "CA" in region:
            return "TOS_CALIFORNIA_2025: Includes AB5 compliance notes for independent contractors..."
        elif "NC" in region:
            return "TOS_NORTH_CAROLINA_2025: Standard independent contractor agreement."
        else:
            return "TOS_GLOBAL_STANDARD_2025."

# Example Usage
if __name__ == '__main__':
    bot = LegalBot()
    
    # Test 1: Valid Truck
    result_success = bot.verify_truck_compliance({
        "vehicle_type": "FORD F-150 LIGHT DUTY",
        "plate": "PKPLK1",
        "owner_id": 101
    })
    print(f"\nVerification 1 Result: {result_success}")

    # Test 2: Invalid Vehicle (Must fail to enforce the core rule)
    result_fail = bot.verify_truck_compliance({
        "vehicle_type": "TOYOTA CAMRY SEDAN",
        "plate": "SEDDAN",
        "owner_id": 102
    })
    print(f"\nVerification 2 Result: {result_fail}")
