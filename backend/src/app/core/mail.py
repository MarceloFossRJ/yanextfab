from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import get_settings

settings = get_settings()

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_user or "",
    MAIL_PASSWORD=settings.smtp_password or "",  # pyright: ignore[reportArgumentType] — pydantic coerces str -> SecretStr
    MAIL_FROM=settings.smtp_from,
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_host,
    MAIL_STARTTLS=settings.smtp_tls,
    MAIL_SSL_TLS=settings.smtp_ssl,
    USE_CREDENTIALS=bool(settings.smtp_user),
    VALIDATE_CERTS=False,
)

fast_mail = FastMail(mail_config)


async def send_password_reset_email(email: str, token: str) -> None:
    reset_link = f"{settings.frontend_url}/reset-password?token={token}"
    message = MessageSchema(
        subject="Reset your Yanextfab password",
        recipients=[email],  # pyright: ignore[reportArgumentType] — pydantic coerces str -> NameEmail
        body=(
            "<p>Click the link below to reset your password:</p>"
            f'<p><a href="{reset_link}">{reset_link}</a></p>'
            "<p>If you didn't request this, you can safely ignore this email.</p>"
        ),
        subtype=MessageType.html,
    )
    await fast_mail.send_message(message)
