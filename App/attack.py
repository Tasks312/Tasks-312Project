from flask import Flask,request,make_response,redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


ip_dictionary = {}
total_request = 50  #requests
allowed_time = 10 #seconds 
ip_block = 30 #seconds 

def get_ip():
    return request.headers.get('X-Real-IP')
    #gets the ip check nginx.conf 

def handling_function(client_record,ip_address):
    if(client_record['is_blocked']):
        None

def limit_rate(ip_address):
    if(ip_address not in ip_dictionary):
        record = {'requests': 0, 'blocked_time': 0, 'request_time_period': None,
                  'is_blocked':False}
        ip_dictionary[ip_address] = record

    client_record = ip_dictionary[ip_address]
    handling_function(client_record,ip_address)


def overload_response():
    response = make_response(redirect('/'), 'Too Many Requests. Please try again later.')
    response.status_code = 429
    return response