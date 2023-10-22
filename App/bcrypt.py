import hashlib
import secrets
from flask_bcrypt import Bcrypt

from flask import current_app, g

def init_bcrypt():
    if ('bcrypt' not in g):
        g.bcrypt = Bcrypt(current_app)

    return g.bcrypt

def hash(string: str):
    return init_bcrypt().generate_password_hash(string).decode('utf-8')

def hash_compare(hash, rawstring: str):
    return init_bcrypt().check_password_hash(hash, rawstring)

def gen_token():
    return secrets.token_hex(16)

def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def escape_html(string: str):
    escaped = ""

    for chr in string:
        if chr == '&':
            escaped += "&amp"
        elif chr == '<':
            escaped += "&lt"
        elif chr == '>':
            escaped += "&gt"
        else:
            escaped += chr

    return escaped