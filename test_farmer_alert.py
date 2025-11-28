import asyncio
import aiohttp
import sys
from main import calculate_risk, FarmerInput
from fastapi import BackgroundTasks

async def test_hk_alert():
    """Test with real Hong Kong numbers"""
    test_cases = [
        {
            "farmer_id": "TEST_001",
            "plasma_dha_pct": 2.1,    # Critical low
            "mri_volume_norm": 0.32,   # Critical low  
            "phone_number": "+85291234567",
            "village_name": "Testing Village"
        },
        {
            "farmer_id": "TEST_002", 
            "plasma_dha_pct": 5.5,    # Normal
            "mri_volume_norm": 0.75,   # Normal
            "phone_number": "+85267890123",
            "village_name": "Healthy Village"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for test in test_cases:
            input_data = FarmerInput(**test)
            result = await calculate_risk(input_data, BackgroundTasks())
            
            print(f"\n{'🚨 ALERT TEST' if result.alert_needed else '✅ NORMAL TEST'}")
            print(f"Farmer: {result.farmer_id}")
            print(f"Risk Score: {result.risk_score:.3f}")
            print(f"Certainty: {result.certainty*100:.1f}%")
            print(f"SMS Sent: {'✅ YES' if result.sms_sent else '❌ NO'}")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_hk_alert())
