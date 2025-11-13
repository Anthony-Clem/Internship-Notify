import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(listings, name="Anthony"):
    if not listings:
        return

    msg = EmailMessage()
    msg['Subject'] = f"🆕 {len(listings)} new internship(s)"
    msg['From'] = os.getenv("EMAIL_FROM")
    msg['To'] = os.getenv("EMAIL_TO")

    rows = ""
    for l in listings:
        rows += f"""
        <tr>
            <td>{l['company']}</td>
            <td>{l['role']}</td>
            <td>{l['location']}</td>
            <td><a href="{l['link']}">Apply</a></td>
            <td>{l['age']}</td>
        </tr>
        """

    html_content = f"""
    <html>
    <body>
        <p>Hey {name},<br>
        I found {len(listings)} new internships for you:</p>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Location</th>
                    <th>Application</th>
                    <th>Age</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <p>Good luck applying! 🚀</p>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype='html')

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("EMAIL_USER")
    smtp_pass = os.getenv("EMAIL_PASS")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
