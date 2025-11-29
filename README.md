# 🌾 Bio-Alert Farmer System

**Real-time medical alerts for remote farmers using AI-powered risk scoring**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## ✅ DEPLOYMENT (60 SECONDS - NO PHONE VERIFICATION!)

### Step 1: Create Twilio Function (FREE)
1. Go to [twilio.com/labs/functions](https://www.twilio.com/labs/functions)
2. Sign up with **email verification** (avoid phone OTP loops)
3. Create new Service → "farmer-alert"
4. Create Function named "send-alert" with this code:
```javascript
exports.handler = function(context, event, callback) {
  const client = context.getTwilioClient();
  const twilioNumber = context.TWILIO_PHONE_NUMBER;
  
  client.messages.create({
    to: event.to,
    from: twilioNumber,
    body: event.body
  })
  .then(() => callback(null, { success: true, message: "SMS sent" }))
  .catch(err => {
    console.error("SMS failed:", err);
    callback(null, { success: false, error: err.message });
  });
};
