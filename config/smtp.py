from django.core.mail import send_mail


def send_otp(recipient_mail,user):
  
    otp = user.update_otp()
    subject = 'WanderWeb OTP verification'
    message = f'Your OTP for verification is{otp}'
    from_email = 'wanderweb@gmail.com'
    recipient_list =[recipient_mail]

    return send_mail(subject, message, from_email, recipient_list)