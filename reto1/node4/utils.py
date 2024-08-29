# common/utils.py
import hashlib

def get_hash(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2**160)
