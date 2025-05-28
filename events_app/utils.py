from config import SMTP_PORT, SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD
import smtplib

def send_mail(subject, message, to_email):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        email_message = f"Subject: {subject}\n\n{message}".encode('utf-8')
        server.sendmail(SENDER_EMAIL, to_email, email_message)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def send_registration_email(user, event):
    subject = f"Реєстрація на подію: {event.title}"
    message = f"Ви успішно зареєстровані на подію '{event.title}', яка відбудеться {event.date}.\n\n" \
              f"Деталі: {event.description}\n\n" \
              f"Дякуємо, що користуєтесь нашим сервісом!"
    recipient = user.email

    send_mail(subject, message, recipient)