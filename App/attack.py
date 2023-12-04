from flask import Flask,request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



def get_ip():
    return request.headers.get('X-Real-IP')
    #gets the ip check nginx.conf 

def limit_rate(ip_address):
    None