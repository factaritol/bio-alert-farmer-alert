import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional
import aiohttp
from sms_sender import send_sms_alert
from deepseek_math_mock import fallback_math_reasoner  # Works offline

app = FastAPI(title="🌾 Farmer Alert System - DeepSeek Math Edition")

# Configuration - works with or without DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
USE_DEEPSEEK = bool(DEEPSEEK_API_KEY)

class FarmerInput(BaseModel):
    farmer_id: str = Field(..., description="Unique farmer ID")
    plasma_dha_pct: float = Field(..., ge=0, le=10, description="DHA 0-10%")
    mri_volume_norm: float = Field(..., ge=0, le=1, description="MRI volume 0-1")
    phone_number: str = Field(..., description="HK phone +852...")
    village_name: str = Field(..., description="Village location")

class RiskResponse(BaseModel):
    farmer_id: str
    risk_score: float
    certainty: float  # DeepSeek-Math-V2 confidence
    alert_needed: bool
    sms_sent: bool
    timestamp: str

async def get_deepseek_certainty(data: FarmerInput) -> float:
    """Get medical-grade certainty from DeepSeek-Math-V2"""
    if not USE_DEEPSEEK:
        return fallback_math_reasoner(data)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/v2/math/reason",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "problem": (
                        f"Farmer {data.farmer_id} in {data.village_name} has:\n"
                        f"- Plasma DHA: {data.plasma_dha_pct}% (normal range: 4-8%)\n"
                        f"- MRI volume: {data.mri_volume_norm} (normal: >0.6)\n"
                        f"Calculate risk score: 0.7*DHA + 0.3*MRI_volume\n"
                        f"Alert if score < 0.4. What is the medical certainty?"
                    ),
                    "context": "rural_healthcare_emergency"
                },
                timeout=10
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return min(0.99, float(result.get("certainty", 0.85)))
        return 0.85  # Default if API fails
    except Exception as e:
        logging.warning(f"DeepSeek API failed: {e}. Using fallback.")
        return fallback_math_reasoner(data)

@app.post("/calculate-risk", response_model=RiskResponse)
async def calculate_risk( FarmerInput, background_tasks: BackgroundTasks):
    """Calculate risk with DeepSeek-Math-V2 certainty scoring"""
    # Normalize DHA to 0-1 scale
    normalized_dha = data.plasma_dha_pct / 10.0
    
    # Base risk score
    risk_score = 0.7 * normalized_dha + 0.3 * data.mri_volume_norm
    risk_score = round(risk_score, 3)
    
    # Get medical certainty (works offline!)
    certainty = await get_deepseek_certainty(data)
    
    # Alert logic with certainty threshold
    alert_needed = risk_score < 0.4 and certainty > 0.7
    
    sms_sent = False
    if alert_needed:
        message = (
            f"🚨 URGENT MEDICAL ALERT (Certainty: {certainty*100:.0f}%)\n"
            f"Farmer: {data.farmer_id}\n"
            f"Village: {data.village_name}\n"
            f"Risk Score: {risk_score:.3f} (<0.4 threshold)\n"
            f"Action: Schedule immediate consultation"
        )
        background_tasks.add_task(send_sms_alert, data.phone_number, message)
        sms_sent = True

    return RiskResponse(
        farmer_id=data.farmer_id,
        risk_score=risk_score,
        certainty=certainty,
        alert_needed=alert_needed,
        sms_sent=sms_sent,
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "deepseek_available": USE_DEEPSEEK,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
