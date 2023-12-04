from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def limit_rate(ip_address):
    None