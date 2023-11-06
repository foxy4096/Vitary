from hashlib import md5


def get_gravatar(email):
    return f'https://www.gravatar.com/avatar/{md5(email.lower().encode("utf-8")).hexdigest()}'
