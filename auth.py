from bcrypt import hashpw, gensalt, checkpw



def hash_password(password: str):
    password = password.encode()
    password = hashpw(password, gensalt())
    password = password.decode()
    return password

def check_password(db_password_hash: str, password: str):
    password = password.encode()
    db_password_hash = db_password_hash.encode()
    return checkpw(password, db_password_hash)


