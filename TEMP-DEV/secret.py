import secrets

def generate_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(chars) for _ in range(50))

secret_key = generate_secret_key()
print(secret_key)
