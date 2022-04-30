from django.core.mail import EmailMessage



def emailInvoiceClient(to_email, from_client, filepath, title):
    subject = 'Rainbow Tailors Invoice Notification'
    body = f"""
    Good day,
    Please find attached invoice from Rainbow Tailors for your immediate attention.
    regards,
    Rainbow Tailors - Manufacturers of Uniforms\n
    {title}
    """

    print(from_email, settings.EMAIL_HOST_PASSWORD)
    message = EmailMessage(subject, body, from_client, [to_email])
    message.attach_file(filepath)
    message.send()