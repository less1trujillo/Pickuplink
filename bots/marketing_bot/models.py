# bots/marketing_bot/models.py

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MarketDemandSignal:
    """Represents a data point signaling where marketing focus is needed."""
    region: str
    driver_density_score: float  # Lower score means higher need for recruitment
    delivery_requests_7d: int      # Volume of recent requests
    conversion_rate: float         # Current driver conversion efficiency
    priority_score: float          # Calculated metric for immediate action

@dataclass
class ViralContentDraft:
    """Represents an AI-generated piece of content."""
    platform: str          # e.g., 'Twitter', 'Facebook', 'LinkedIn'
    headline: str
    body: str
    call_to_action: str
    estimated_reach_metric: float # AI-predicted performance metric
    
@dataclass
class PartnershipProposal:
    """Represents an automatically generated proposal for a carrier."""
    partner_name: str
    integration_focus: str # e.g., 'LTL overflow', 'Last-mile integration'
    proposed_fee_structure: str
    status: str = "DRAFTED" # DRAFTED, SENT, NEGOTIATING, ACTIVE
