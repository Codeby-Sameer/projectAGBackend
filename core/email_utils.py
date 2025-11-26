
import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

# Default template & subject
DEFAULT_SUBJECT = os.getenv("EMAIL_SUBJECT", "New Form Submission")
DEFAULT_TEMPLATE = os.getenv("EMAIL_TEMPLATE")

# Logo path
LOGO_PATH = r"D:\Traning_Livt\anand_Backend\Send_Us_a_Message\templates\logo\Levitica logo.png"


def load_template(path: str):
    """Load HTML template from file."""
    if not path or not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_email(contact: dict, template_path: str = None, subject: str = None) -> MIMEMultipart:
    """
    Universal builder for ALL forms.
    Includes:
    - Placeholder replacement
    - Conditional cleanup (removes empty <p> rows)
    - Section cleanup
    - Inline logo embedding
    """

    # Load template (custom > default)
    tpl = load_template(template_path) or load_template(DEFAULT_TEMPLATE) or ""

    # 🚀 FIRST PASS — Remove empty fields completely
    for key, value in contact.items():
        placeholder = f"{{{{ {key} }}}}"

        if not value or str(value).strip() == "":
            # Remove <p>...</p> lines that contain the placeholder
            tpl = re.sub(
                rf"<p[^>]*>.*?{placeholder}.*?</p>",
                "",
                tpl,
                flags=re.DOTALL,
            )
            # Remove the placeholder if it's inside any other tag
            tpl = tpl.replace(placeholder, "")
        else:
            tpl = tpl.replace(placeholder, str(value))

    # 🚀 SECOND PASS — Remove any now-empty info blocks
    section_patterns = [
        r"<div class=\"info\">\s*</div>",
        r"<div class=\"section-title\">.*?</div>\s*<div class=\"info\">\s*</div>",
    ]

    for pattern in section_patterns:
        tpl = re.sub(pattern, "", tpl, flags=re.DOTALL)

    # Prepare email MIME container
    msg = MIMEMultipart("related")
    msg["Subject"] = subject or DEFAULT_SUBJECT
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    # HTML part
    alt = MIMEMultipart("alternative")
    msg.attach(alt)
    alt.attach(MIMEText(tpl, "html"))

    # Embed company logo with CID
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            logo = MIMEImage(f.read())
            logo.add_header("Content-ID", "<company_logo>")
            logo.add_header("Content-Disposition", "inline", filename="logo.png")
            msg.attach(logo)
    else:
        print(f"⚠ Logo NOT found at: {LOGO_PATH}")

    return msg


def send_email_message(msg: MIMEMultipart):
    """Send email."""
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    try:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO.split(","), msg.as_string())
    finally:
        server.quit()
