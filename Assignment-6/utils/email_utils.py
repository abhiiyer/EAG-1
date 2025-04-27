import smtplib
from email.message import EmailMessage

def generate_email(customer, decision, intent_score, pitch_text):
    subject = f"Special Offer from Mashreq – {decision.suggested_action}"

    # Risk alerts
    risk_alerts = []
    if 'drop' in decision.message.lower():
        risk_alerts.append("⚠️ Sudden drop in balance observed.")
    if 'competitor' in customer.recent_activity.lower():
        risk_alerts.append("⚠️ Recent transfer to competitor bank (e.g., Wio/Liv).")
    if 'fd' in customer.products and 'maturity' in customer.recent_activity.lower():
        risk_alerts.append("⚠️ Fixed deposit maturing soon.")

    risk_section = "\n".join(risk_alerts) if risk_alerts else "No risk flags at this time."

    # Competitor rates
    competitor_fx = 3.53
    mashreq_fx = 3.57
    competitor_fd = 3.85
    mashreq_fd = 4.25

    # Personalized FD offer
    if 'Etisalat' in customer.employer:
        personal_fd_offer = "You are eligible for an exclusive 4.50% FD rate for 12 months."
    else:
        personal_fd_offer = "Based on your profile, we recommend our 4.25% FD rate for 12 months."

    body = f"""Dear {customer.name},

We’re reaching out based on your recent banking activity with Mashreq.

📋 Summary:
{decision.message}

🛡 Risk Alerts:
{risk_section}

🏦 Competitor Comparison:
- FX Rate at Wio: {competitor_fx}
- FX Rate at Mashreq: {mashreq_fx}
- FD Rate at Liv: {competitor_fd}%
- FD Rate at Mashreq: {mashreq_fd}%

🎯 Personalized Offer:
{personal_fd_offer}

📞 Recommended Pitch:
{pitch_text}

📈 Engagement Score: {intent_score}/100

Would you like to proceed?
👉 Request a callback: mailto:{customer.email}?subject=Request Callback
👉 Book a time: https://calendly.com/mashreq-advisor/fd-review

Best regards,  
Mashreq RM Team
"""
    return subject, body

def send_email(subject, body, from_email="rm.assist.notifier@gmail.com", password="your_app_password"):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = "abiyer88@gmail.com"
    msg.set_content(body)
    msg.add_attachment("Rate Card and Offer Sheet Placeholder", filename="rate_card.txt")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)