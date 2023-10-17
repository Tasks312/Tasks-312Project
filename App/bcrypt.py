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
    return "I DONT KNOW HOW TO DO THIS PLEASE HELP"
