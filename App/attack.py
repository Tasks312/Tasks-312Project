from flask import Flask,request,make_response,redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



total_request = 50  #requests
allowed_time = 10 #seconds 
ip_block = 30 #seconds 

def get_ip():
    return request.headers.get('X-Real-IP')
    #gets the ip check nginx.conf 

def limit_rate(ip_address):
    None

def overload_response():
    response = make_response(redirect('/'), 'Too Many Requests. Please try again later.')
    response.status_code = 429
    return response