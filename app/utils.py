from app_init.app_factory import pwd_context



def get_hash_password(plain_text):
    return pwd_context.hash(plain_text)


def verify_password(plain_text,hashed_password):
    return pwd_context.verify(plain_text,hashed_password)