import os
import aiohttp
import logging

# Get Twilio Function URL from environment or use placeholder
TWILIO_FUNCTION_URL = os.getenv("TWILIO_FUNCTION_URL", "https://your-twilio-function.twil.io/send-alert")

logger = logging.getLogger("sms_sender")

async def send_sms_alert(phone_number: str, message: str) -> bool:
    """Send SMS via Twilio Functions - works with HK numbers"""
    try:
        # Format HK phone numbers properly
        if not phone_number.startswith('+852'):
            # Clean and format the number
            clean_number = ''.join(filter(str.isdigit, phone_number))
            if clean_number.startswith('852'):
                phone_number = '+' + clean_number
            else:
                phone_number = '+852' + clean_number.lstrip('0')
        
        logger.info(f"Sending SMS to: {phone_number}")
        logger.info(f"Message: {message[:50]}...")  # Log first 50 chars
        
        # Get Twilio phone number from env
        from_number = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                TWILIO_FUNCTION_URL,
                json={
                    "to": phone_number,
                    "body": message[:1600],  # HK SMS character limit
                    "from": from_number
                },
                timeout=15
            ) as response:
                response_text = await response.text()
                logger.info(f"Twilio response: {response.status} - {response_text}")
                
                if response.status == 200:
                    logger.info(f"✅ SMS successfully sent to {phone_number}")
                    return True
                else:
                    logger.error(f"❌ SMS failed. Status: {response.status}, Response: {response_text}")
                    return False
                    
    except Exception as e:
        logger.error(f"🔥 SMS sending crashed: {str(e)}", exc_info=True)
        return False
