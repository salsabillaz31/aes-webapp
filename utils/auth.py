import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password, conn):
    cur = conn.cursor()
    query = "SELECT password, role FROM users WHERE username = %s"
    cur.execute(query, (username,))
    result = cur.fetchone()
    cur.close()

    if result:
        stored_password, role = result
        if stored_password == password:
        #if stored_password == hash_password(password):
            return role
    return None
