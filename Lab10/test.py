import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)