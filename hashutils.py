import hashlib

def hash_sha256(obj_str):
    hashfunc = hashlib.sha256()
    hashfunc.update(obj_str)
    return hashfunc.hexdigest()
