# bots/dispatcher_bot/models.py

from dataclasses import dataclass
from typing import Tuple, Dict, Any

@dataclass
class DeliveryJob:
    """Represents a delivery request submitted by a client/partner."""
    id: int
    pickup_location: Tuple[float, float]    # (latitude, longitude)
    dropoff_location: Tuple[float, float]   # (latitude, longitude)
    base_price: float
    required_capacity: float                # Truck capacity needed (e.g., in sqft)
    is_express: bool = False

@dataclass
class DriverStatus:
    """Represents the current status of an available and verified driver."""
    id: int
    location: Tuple[float, float]
    capacity: float
    rating: float
    is_verified: bool = True
    is_active: bool = False                 # Online status

@dataclass
class Route:
    """Represents the optimized route details."""
    distance_km: float
    duration_minutes: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "distance_km": round(self.distance_km, 2),
            "duration_minutes": round(self.duration_minutes, 2)
        }
