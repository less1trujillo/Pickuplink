# bots/finance_bot/finance_bot.py

import requests
from settings import DRIVER_STANDARD_PERCENT, DRIVER_EXPRESS_PERCENT, FINANCE_PAYOUT_API_KEY, GOVERNANCE_URL
from typing import Dict, Any

class FinanceBot:
    def __init__(self):
        # In a real app, this connects to the DB using DATABASE_URL from settings
        print("FinanceBot Initialized. Controlling all platform revenue streams.")
        
    def calculate_distribution(self, job_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculates the split based on job type (Standard vs Express)."""
        
        base_price = job_data.get('base_price', 0.0)
        is_express = job_data.get('is_express', False)
        
        if is_express:
            driver_share = base_price * DRIVER_EXPRESS_PERCENT
            platform_fee = base_price * (1.0 - DRIVER_EXPRESS_PERCENT) # 25%
        else:
            driver_share = base_price * DRIVER_STANDARD_PERCENT
            platform_fee = base_price * (1.0 - DRIVER_STANDARD_PERCENT) # 20%

        # Governance/Bot Allocation Placeholder (controlled by Governance Bot later)
        bot_funding = 0.0 
        
        # Recalculate final driver payout after potential bot allocation
        final_driver_payout = driver_share - bot_funding
        
        return {
            "gross_revenue": base_price,
            "driver_payout": round(final_driver_payout, 2),
            "platform_fee": round(platform_fee, 2),
            "bot_funding_allocated": round(bot_funding, 2)
        }

    def process_payout(self, driver_id: int, amount: float) -> bool:
        """
        Handles automated payout to the independent driver's account via payment gateway.
        """
        print(f"Initiating Payout of ${amount:.2f} to Driver ID: {driver_id}...")
        
        # --- Payment Gateway Integration (Stripe/PayPal/ACH) ---
        # headers = {'Authorization': f'Bearer {FINANCE_PAYOUT_API_KEY}'}
        # response = requests.post(f"https://payment.gateway/payout", json={...})
        
        # Simulation: Assume success 95% of the time
        if amount > 0 and (hash(driver_id) % 20) != 0: 
            print(f"Payout successful for Driver {driver_id}.")
            return True
        else:
            print(f"Payout FAILED for Driver {driver_id}. Logging for manual review.")
            return False
            
    def handle_bot_funding_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Endpoint for other bots (like Marketing Bot) to request micro-funding.
        This function is called by the Marketing Bot's launch_campaign method.
        """
        mission = request_data.get("mission", "UNKNOWN")
        requested_amount = request_data.get("estimated_spend", 0.0)
        
        # Governance Bot interaction needed here to check budget/performance, but 
        # for this script, we'll approve based on a simple check.
        
        # Simple Approval Logic: Approve up to $1000 max per mission request for Phase 1.
        approved_amount = min(requested_amount, 1000.00)
        
        print(f"Funding request: Mission {mission}. Requested: ${requested_amount}, Approved: ${approved_amount}")
        
        # Log the potential allocation to the bot_missions table (via Governance Bot/DB layer)
        
        return {"success": True, "approved_amount": approved_amount}


if __name__ == '__main__':
    # --- Example Execution ---
    finance = FinanceBot()
    
    # 1. Standard Job Example
    standard_job = {'base_price': 100.00, 'is_express': False, 'driver_id': 101}
    dist_std = finance.calculate_distribution(standard_job)
    print("\n--- Standard Job (100.00) ---")
    print(f"Platform Fee (20%): ${dist_std['platform_fee']}")
    print(f"Driver Payout (80%): ${dist_std['driver_payout']}")
    
    # 2. Express Job Example
    express_job = {'base_price': 100.00, 'is_express': True, 'driver_id': 102}
    dist_exp = finance.calculate_distribution(express_job)
    print("\n--- Express Job (100.00) ---")
    print(f"Platform Fee (25%): ${dist_exp['platform_fee']}")
    print(f"Driver Payout (75%): ${dist_exp['driver_payout']}")

    # 3. Payout Test
    finance.process_payout(driver_id=101, amount=dist_std['driver_payout'])
    
    # 4. Funding Test
    funding_result = finance.handle_bot_funding_request({
        "mission": "EXPANSION_CHARLOTTE_SEO",
        "estimated_spend": 850.00
    })
    print(f"\nFunding approval result: {funding_result}")
