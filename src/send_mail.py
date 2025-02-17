from email.message import EmailMessage

from aiosmtplib import SMTP

from settings import settings


async def send_message(email: str, msg_sub: str):

    message = EmailMessage()
    message["From"] = settings.EMAIL_SENDER_NAME
    message["To"] = email
    message["Subject"] = "Appeal service notification"
    message.set_content(msg_sub)

    smtp_client = SMTP(
        hostname=settings.SMTP_SERVER,
        username=settings.EMAIL_SENDER_NAME,
        password=settings.APPLICATION_EMAIL_PASSWORD,
        port=settings.SMTP_PORT,
    )
    async with smtp_client:
        await smtp_client.send_message(message)
