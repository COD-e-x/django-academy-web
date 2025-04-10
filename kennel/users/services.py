from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    html_message = """
    <html>
        <body>
            <h1 style="font-family: Arial, sans-serif; color: #165cc6; text-align: center">Поздравляем с регистрацией!</h1>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                Вы успешно зарегистрировались на <strong style="color: #165cc6">cod-ex.ru</strong>. Добро пожаловать!
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                Для начала работы, пожалуйста, перейдите по
                <a href="https://cod-ex.ru" style="color: #1e90ff; text-decoration: none">ссылке</a>.
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                С уважением, команда Cod-Ex.
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 12px; color: #868686b6; text-align: center">
                Это сообщение было отправлено автоматически. Можете не отвечать на него.
            </p>
        </body>
    </html>
    """
    send_mail(
        subject="Поздравляем с регистрацией на нашем сервисе.",
        message="https://cod-ex.ru",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=html_message,
    )


def send_new_password(email, new_password):
    html_message = f"""
    <html>
        <body>
            <h1 style="font-family: Arial, sans-serif; color: #165cc6; text-align: center">Ваш новый пароль</h1>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                Ваш новый пароль для доступа к платформе 
                <a href="https://cod-ex.ru" style="color: #1e90ff; text-decoration: none">www.cod-ex.ru</a>.
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                <strong style="font-size: 18px; color: #1e90ff">{new_password}</strong>
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                Пожалуйста, храните ваш пароль в безопасности.
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; text-align: center">
                С уважением, команда Cod-Ex.
            </p>
            <p style="font-family: Arial, sans-serif; font-size: 12px; color: #868686b6; text-align: center">
                Это сообщение было отправлено автоматически. Можете не отвечать на него.
            </p>
        </body>
    </html>
    """
    send_mail(
        subject="Вы успешно обновили пароль.",
        message="https://cod-ex.ru",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=html_message,
    )
