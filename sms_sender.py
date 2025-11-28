import os
import aiohttp
import logging

# Twilio Function URL (create free at twilio.com/labs/functions)
TWILIO_FUNCTION_URL = "https://farmer-alert-7894.twil.io/send-alert"

async def send_sms_alert(phone_number: str, message: str) -> bool:
    """Send SMS via Twilio Functions - no account verification needed"""
    try:
        # Format HK numbers properly
        if not phone_number.startswith('+852'):
            phone_number = '+852' + phone_number.lstrip('+852').lstrip('0')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                TWILIO_FUNCTION_URL,
                json={
                    "to": phone_number,
                    "body": message[:1600],  # HK SMS limit
                    "from": "+1234567890"  # Your Twilio Function phone
                },
                timeout=15
            ) as response:
                if response.status == 200:
                    logging.info(f"✅ SMS sent to {phone_number}")
                    return True
                else:
                    error = await response.text()
                    logging.error(f"❌ SMS failed: {error}")
                    return False
    except Exception as e:
        logging.error(f"🔥 SMS crashed: {str(e)}")
        return False
