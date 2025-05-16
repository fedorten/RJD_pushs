import sqlite3

def init_db():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_date DATETIME NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT,
            transport_type TEXT,
            departure_city TEXT,
            arrival_city TEXT,
            train_number TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_booking(trip_date, email, phone, transport, from_city, to_city, train_num):
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO bookings 
        (trip_date, customer_email, customer_phone, transport_type, departure_city, arrival_city, train_number) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (trip_date, email, phone, transport, from_city, to_city, train_num)
    )
    conn.commit()
    conn.close()

def get_bookings_for_notification():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM bookings 
        WHERE datetime(trip_date) BETWEEN datetime('now', '+24 hours') AND datetime('now', '+25 hours')
    """)
    bookings = cursor.fetchall()
    conn.close()
    return bookings