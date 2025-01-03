from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(to_email, receiver, password):
    subject = "Your BIOS Account Password"
    message = (
        f"Dear {receiver},\n\n"
        f"Your account has been created successfully.\n"
        f"Your username is: {to_email}\n"
        f"Your temporary password is: {password}\n\n"
        f"Please log in and change your password as soon as possible.\n\n"
        f"Regards,\n"
        f"Bilkent Information System Team"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        email = EmailMultiAlternatives(subject, message, from_email, [to_email])
        # Optional: Add simple HTML version
        html_message = (
            f"<p>Dear {receiver},</p>"
            f"<p>Your account has been created successfully.</p>"
            f"<p><strong>Your username:</strong> {to_email}</p>"
            f"<p><strong>Your temporary password:</strong> {password}</p>"
            f"<p>Please log in and change your password as soon as possible.</p>"
            f"<p>Regards,<br>Bilkent Information System Team</p>"
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_rejection_email(to_email, receiver, rejection_reason):
    subject = "Your BIOS Registration Request"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Plain text content
    text_content = (
        f"Dear {receiver},\n\n"
        f"We regret to inform you that your registration request has been rejected.\n\n"
        f"Reason for rejection: {rejection_reason}\n\n"
        f"If you believe this is a mistake or have any questions, please contact our support team.\n\n"
        f"Regards,\n"
        f"Bilkent Information System Team"
    )

    # Basic HTML content
    html_content = (
        f"<p>Dear {receiver},</p>"
        f"<p>We regret to inform you that your registration request has been rejected.</p>"
        f"<p><strong>Reason for rejection:</strong> {rejection_reason}</p>"
        f"<p>If you believe this is a mistake or have any questions, please contact our support team.</p>"
        f"<p>Regards,<br>Bilkent Information System Team</p>"
    )

    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        print(f"Rejection email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending rejection email: {e}")