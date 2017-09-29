import hashlib

def hash_sha256(encoded_str):
    hashfunc = hashlib.sha256()
    hashfunc.update(encoded_str)
    return hashfunc.hexdigest()

def hash_object(obj):
    """ Return the sha256 hash of the encoded string of
        the object passed as parameter.
    """
    return hash_sha256(str(obj).encode('utf-8'))

def encoded_hash_object(obj):
    """ Return the utf-8 encoded hash of the encoded string
        of the object passed as parameter.
    """
    return hash_object(obj).encode('utf-8')
