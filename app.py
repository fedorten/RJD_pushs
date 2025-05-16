from flask import Flask, jsonify
from threading import Timer
from db import init_db, get_bookings_for_notification, add_booking
from yandex_api import fetch_yandex_schedule
from config import SMTP_SERVER, SMTP_PORT, EMAIL, EMAIL_PASSWORD
import smtplib

app = Flask(__name__)

def send_email(to_email, message):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, to_email, f"Subject: Напоминание о поездке\n\n{message}")
        print(f"Email отправлен на {to_email}")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

def check_bookings():
    # 1. Получаем бронирования, до которых осталось 24 часа
    bookings = get_bookings_for_notification()
    for booking in bookings:
        _, trip_date, email, phone, from_city, to_city, train_num = booking
        message = f"Напоминание: ваш поезд {train_num} из {from_city} в {to_city} завтра в {trip_date}!"
        send_email(email, message)
        print(f"SMS на {phone}: {message}")  # Заглушка для SMS

    # 2. Повторяем проверку каждые 5 минут
    Timer(300, check_bookings).start()

@app.route('/update_trains')
def update_trains():
    """Загружает актуальные поезда из API в базу (для теста)."""
    schedules = fetch_yandex_schedule("c54", "c213")  # Москва → Сочи
    for schedule in schedules:
        add_booking(
            trip_date=schedule["departure"],
            email="test@example.com",  # Можно заменить на реальные email
            phone="+79001234567",
            transport="train",
            from_city=schedule["from"]["title"],
            to_city=schedule["to"]["title"],
            train_num=schedule["thread"]["number"]
        )
    return jsonify({"status": "Расписание обновлено!"})

@app.route('/check')
def manual_check():
    """Ручной запуск проверки уведомлений."""
    check_bookings()
    return jsonify({"status": "Проверка выполнена!"})

if __name__ == '__main__':
    init_db()
    Timer(10, check_bookings).start()  # Первая проверка через 10 сек
    app.run(debug=True)