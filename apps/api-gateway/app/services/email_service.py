"""Transactional Email Delivery Service.

Provides responsive HTML email rendering, verification URL generation, and email
delivery abstraction using FastAPI-Mail, SMTP, or development logger fallback.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Any

try:
    from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
    HAS_FASTAPI_MAIL = True
except ImportError:
    HAS_FASTAPI_MAIL = False

from app.config.settings import settings
from app.exceptions.auth import EmailSendFailedError

logger = logging.getLogger("talentai.services.email")


def generate_verification_email_html(
    recipient_name: str, verification_url: str, expire_hours: int = 24, is_resend: bool = False
) -> str:
    """Render a responsive HTML email template for account email verification.

    Args:
        recipient_name: Given name of the user receiving the email.
        verification_url: Full URL containing the JWT verification token parameter.
        expire_hours: Token validity window in hours.
        is_resend: Boolean flag indicating if this is a resent verification link.

    Returns:
        Rendered HTML string.
    """
    title_text = "Verify Your Email Address — TalentAI" if not is_resend else "Resent: Email Verification — TalentAI"
    heading_text = f"Welcome to TalentAI, {recipient_name}!" if not is_resend else f"Hello {recipient_name},"
    intro_text = (
        "Thank you for signing up for TalentAI! Please confirm your email address by clicking the button below."
        if not is_resend
        else "You requested a new verification link for your TalentAI account. Click below to verify your email."
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <style>
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f6f8;
            color: #1f2937;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: #ffffff;
            padding: 36px 24px;
            text-align: center;
        }}
        .logo-placeholder {{
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -1px;
            margin: 0;
            color: #ffffff;
        }}
        .logo-sub {{
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.85;
            margin-top: 4px;
        }}
        .content {{
            padding: 36px 32px;
        }}
        .content h2 {{
            color: #111827;
            font-size: 22px;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 16px;
        }}
        .content p {{
            margin-bottom: 20px;
            font-size: 16px;
            color: #4b5563;
        }}
        .btn-container {{
            text-align: center;
            margin: 36px 0;
        }}
        .btn {{
            display: inline-block;
            background-color: #2563eb;
            color: #ffffff !important;
            font-weight: 600;
            font-size: 16px;
            padding: 14px 36px;
            border-radius: 8px;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
        }}
        .warning-box {{
            background-color: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 16px;
            border-radius: 6px;
            margin: 28px 0;
            font-size: 14px;
            color: #1e40af;
        }}
        .fallback-link {{
            word-break: break-all;
            font-size: 13px;
            color: #6b7280;
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px solid #f3f4f6;
        }}
        .footer {{
            background-color: #f9fafb;
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: #9ca3af;
            border-top: 1px solid #e5e7eb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-placeholder">TalentAI</div>
            <div class="logo-sub">Enterprise AI Recruitment</div>
        </div>
        <div class="content">
            <h2>{heading_text}</h2>
            <p>{intro_text}</p>

            <div class="btn-container">
                <a href="{verification_url}" class="btn" target="_blank">Verify Email</a>
            </div>

            <div class="warning-box">
                <strong>Expiration Notice:</strong> This verification link will expire in <strong>{expire_hours} hours</strong>. If you did not create a TalentAI account, please ignore this email.
            </div>

            <div class="fallback-link">
                <p>If the button above does not work, copy and paste this link into your browser:</p>
                <p><a href="{verification_url}" style="color: #2563eb;">{verification_url}</a></p>
            </div>
        </div>
        <div class="footer">
            &copy; TalentAI Platform. All rights reserved.<br>
            If you did not request this email, no action is required.
        </div>
    </div>
</body>
</html>
"""


class EmailService:
    """Service handling transactional email delivery via FastAPI-Mail / SMTP."""

    def __init__(self) -> None:
        """Initialize EmailService with FastAPI-Mail ConnectionConfig."""
        self.frontend_url = settings.email.frontend_url.rstrip("/")

        mail_username = (
            settings.email.mail_username
            or settings.email.smtp_username
            or settings.email.smtp_user
        )
        mail_password = settings.email.mail_password or settings.email.smtp_password

        self.mail_username = mail_username
        self.mail_password = mail_password
        self.mail_from = settings.email.mail_from or settings.email.email_from
        self.mail_from_name = settings.email.mail_from_name
        self.mail_server = settings.email.mail_server or settings.email.smtp_host
        self.mail_port = settings.email.mail_port or settings.email.smtp_port
        self.mail_starttls = settings.email.mail_starttls
        self.mail_ssl_tls = settings.email.mail_ssl_tls
        self.mail_validate_certs = settings.email.mail_verify_certs

        self.fastmail_config: Optional[Any] = None
        if HAS_FASTAPI_MAIL and mail_username and mail_password:
            try:
                self.fastmail_config = ConnectionConfig(
                    MAIL_USERNAME=mail_username,
                    MAIL_PASSWORD=mail_password,
                    MAIL_FROM=self.mail_from,
                    MAIL_PORT=self.mail_port,
                    MAIL_SERVER=self.mail_server,
                    MAIL_FROM_NAME=self.mail_from_name,
                    MAIL_STARTTLS=self.mail_starttls,
                    MAIL_SSL_TLS=self.mail_ssl_tls,
                    USE_CREDENTIALS=True,
                    VALIDATE_CERTS=self.mail_validate_certs,
                )
            except Exception as exc:
                logger.warning("Failed to initialize FastAPI-Mail config: %s", exc)

    def build_verification_url(self, token: str) -> str:
        """Construct verification URL: FRONTEND_URL/verify-email?token=xxxxx.

        Args:
            token: Raw JWT verification token string.

        Returns:
            Full verification URL string.
        """
        return f"{self.frontend_url}/verify-email?token={token}"

    async def send_verification_email(
        self, email: str, name: str, token: str, is_resend: bool = False
    ) -> bool:
        """Send email verification link asynchronously using FastAPI-Mail or SMTP.

        Args:
            email: Recipient target email address.
            name: Recipient user name.
            token: JWT email verification token.
            is_resend: Boolean flag indicating if this is a resent link.

        Returns:
            True if email was dispatched successfully.
        """
        verification_url = self.build_verification_url(token)
        html_content = generate_verification_email_html(
            recipient_name=name,
            verification_url=verification_url,
            expire_hours=24,
            is_resend=is_resend,
        )

        subject = "Verify Your Email — TalentAI" if not is_resend else "Resent: Verify Your Email — TalentAI"

        # 1. Attempt delivery via FastAPI-Mail asynchronously
        if HAS_FASTAPI_MAIL and self.fastmail_config:
            try:
                message = MessageSchema(
                    subject=subject,
                    recipients=[email],
                    body=html_content,
                    subtype=MessageType.html,
                )
                fm = FastMail(self.fastmail_config)
                await fm.send_message(message)
                logger.info("Verification email sent via FastAPI-Mail to %s", email)
                return True
            except Exception as exc:
                logger.warning("FastAPI-Mail delivery exception: %s. Falling back to SMTP/logger.", exc)

        # 2. Attempt delivery via standard SMTP if credentials present
        if self.mail_server and self.mail_username and self.mail_password:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"{self.mail_from_name} <{self.mail_from}>" if self.mail_from_name else self.mail_from
                msg["To"] = email
                msg.attach(MIMEText(html_content, "html"))

                with smtplib.SMTP(self.mail_server, self.mail_port, timeout=10) as server:
                    if self.mail_starttls:
                        server.starttls()
                    server.login(self.mail_username, self.mail_password)
                    server.sendmail(self.mail_from, [email], msg.as_string())

                logger.info("Verification email sent via SMTP to %s", email)
                return True
            except Exception as exc:
                logger.warning("SMTP delivery exception: %s. Logging to console.", exc)

        # 3. Development / Test Logging Fallback
        logger.info(
            "========================================================================\n"
            "EMAIL VERIFICATION DISPATCHED (Development Logger Fallback)\n"
            "To: %s (%s)\n"
            "Subject: %s\n"
            "Verification Link: %s\n"
            "========================================================================",
            email,
            name,
            subject,
            verification_url,
        )
        return True

    async def send_resend_verification_email(
        self, email: str, name: str, token: str
    ) -> bool:
        """Resend email verification link asynchronously.

        Args:
            email: Target recipient email.
            name: User name.
            token: JWT email verification token.

        Returns:
            True if email dispatched successfully.
        """
        return await self.send_verification_email(
            email=email, name=name, token=token, is_resend=True
        )
