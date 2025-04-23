import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

def get_or_create_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return user_id

def get_user_score(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT score, level, speed FROM user_score WHERE user_id = %s;", (user_id,))
    result = cur.fetchone()

    if result:
        cur.close()
        conn.close()
        return result
    else:
        cur.execute(
            "INSERT INTO user_score (user_id, score, level, speed) VALUES (%s, 0, 1, 10);",
            (user_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return (0, 1, 10)

def save_score(user_id, score, level, speed):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_score SET score = %s, level = %s, speed = %s
        WHERE user_id = %s;
    """, (score, level, speed, user_id))

    conn.commit()
    cur.close()
    conn.close()