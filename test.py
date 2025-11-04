import bcrypt


def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode('utf-8'), hashed)
