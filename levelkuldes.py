from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pathlib import Path

def levelkuldes_dir(kitol, kiknek, email_template_dir, context, debugmessage='') -> bool:
    DIR = Path(email_template_dir)
    subject   = render_to_string(DIR/'subject.txt', context).strip()
    body_txt  = render_to_string(DIR/'body.txt', context).strip()
    body_html = render_to_string(DIR/'body.html', context).strip()
    email = EmailMultiAlternatives(subject=subject, from_email=kitol, to=kiknek, body=body_txt)
    email.attach_alternative(body_html, "text/html")
    siker = email.send(fail_silently=False)
    print(f'{debugmessage}: {siker}')
    return siker

def levelkuldes(kitol, kiknek, subject_txt, body_txt, body_html, debug_message='') -> bool:
    email = EmailMultiAlternatives(subject=subject_txt, from_email=kitol, to=[kiknek], body=body_txt)
    email.attach_alternative(body_html, "text/html")
    siker = email.send(fail_silently=False)
    print(f'{debug_message}: {siker}')
    return siker