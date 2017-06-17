from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template


def auction_email_notification(emails, url, template, subject=''):
    text_template = get_template('%s.txt' % template)
    html_template = get_template('%s.html' % template)

    text_content = text_template.render({'url': url})
    html_content = html_template.render({'url': url})

    with get_connection() as _:
        for email in emails:
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                # from_email,
                to=[email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
