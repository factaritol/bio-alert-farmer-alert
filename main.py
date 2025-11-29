import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import aiohttp
from sms_sender import send_sms_alert
from deepseek_math_mock import fallback_math_reasoner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bio-alert")

app = FastAPI(title="🌾 Bio-Alert Farmer System", version="1.0")

class FarmerInput(BaseModel):
    farmer_id: str = Field(..., description="Unique farmer ID")
    plasma_dha_pct: float = Field(..., ge=0, le=10, description="DHA 0-10%")
    mri_volume_norm: float = Field(..., ge=0, le=1, description="MRI volume 0-1")
    phone_number: str = Field(..., description="HK phone +852...")
    village_name: str = Field(..., description="Village location")

class RiskResponse(BaseModel):
    farmer_id: str
    risk_score: float
    certainty: float
    alert_needed: bool
    sms_sent: bool
    timestamp: str

@app.post("/calculate-risk")
async def calculate_risk( FarmerInput, background_tasks: BackgroundTasks):
    """Calculate risk with medical-grade certainty scoring"""
    try:
        # Normalize DHA to 0-1 scale
        normalized_dha = data.plasma_dha_pct / 10.0
        
        # Calculate base risk score
        risk_score = 0.7 * normalized_dha + 0.3 * data.mri_volume_norm
        risk_score = round(risk_score, 3)
        
        # Get medical certainty (works offline!)
        certainty = fallback_math_reasoner(data)
        
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

        logger.info(f"Risk calculated for {data.farmer_id}: score={risk_score}, certainty={certainty:.2f}, alert={alert_needed}")
        
        return {
            "farmer_id": data.farmer_id,
            "risk_score": risk_score,
            "certainty": certainty,
            "alert_needed": alert_needed,
            "sms_sent": sms_sent,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing farmer {data.farmer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "bio-alert-farmer",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
