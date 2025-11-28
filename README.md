# 🌾 Bio-IT Farmer Alert System

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## ✅ ONE-CLICK DEPLOY (NO CLOUD ACCOUNTS!)
1. Click the **Deploy to Render** button above
2. Create free Render account (email only - no phone verification)
3. Fork this repo to your GitHub
4. Connect your forked repo to Render
5. **Done!** Your API is live at `https://your-app.onrender.com`

## 📱 TWILIO SETUP (FREE)
1. Go to [twilio.com/labs/functions](https://www.twilio.com/labs/functions)
2. Create free account (use email verification to avoid OTP loops)
3. Create a new Function named "send-alert"
4. Paste this code into the function:
```javascript
exports.handler = function(context, event, callback) {
  const client = context.getTwilioClient();
  client.messages.create({
    to: event.to,
    from: context.TWILIO_PHONE_NUMBER,
    body: event.body
  }).then(() => callback(null, {success: true}))
   .catch(err => callback(err));
};
