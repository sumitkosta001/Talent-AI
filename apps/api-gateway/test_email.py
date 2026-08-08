import asyncio

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.config.settings import settings


# Narrow settings.email.mail_username and settings.email.mail_password to satisfy type checkers that expect str
mail_username = settings.email.mail_username or ""
mail_password = settings.email.mail_password or ""

mail_config = ConnectionConfig(
    MAIL_USERNAME=mail_username,
    MAIL_PASSWORD=mail_password,
    MAIL_FROM=settings.email.mail_from,
    MAIL_FROM_NAME=settings.email.mail_from_name,
    MAIL_SERVER=settings.email.mail_server,
    MAIL_PORT=settings.email.mail_port,
    MAIL_STARTTLS=settings.email.mail_starttls,
    MAIL_SSL_TLS=settings.email.mail_ssl_tls,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=settings.email.mail_verify_certs,
)



async def send_test_email():
    message = MessageSchema(
        subject="TalentAI SMTP Test",
        recipients=["sumitkosta002@gmail.com"],
        body="""
        <html>
            <body>
                <h2>TalentAI Email Test</h2>

                <p>
                    This is a test email from the TalentAI API Gateway.
                </p>

                <p>
                    If you received this email, Gmail SMTP is configured correctly.
                </p>
            </body>
        </html>
        """,
        subtype=MessageType.html,
    )

    fast_mail = FastMail(mail_config)

    await fast_mail.send_message(message)

    print("========================================")
    print("EMAIL SENT SUCCESSFULLY")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(send_test_email())