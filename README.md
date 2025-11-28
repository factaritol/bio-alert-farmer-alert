# 🌾 Bio-IT Farmer Alert System

**Deploy in 60 seconds - NO cloud accounts needed:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Features
✅ **DeepSeek-Math-V2** for medical-grade certainty scoring  
✅ **Twilio SMS** to Hong Kong farmers (no phone verification needed)  
✅ **Zero cloud account setup** - just click and deploy  
✅ **Offline fallback** if APIs are down  

## Test after deploy
```bash
curl -X POST https://your-render-url.onrender.com/calculate-risk \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": "HK_FARMER_001",
    "plasma_dha_pct": 2.5,
    "mri_volume_norm": 0.35,
    "phone_number": "+85291234567",
    "village_name": "Lamma Island"
  }'
