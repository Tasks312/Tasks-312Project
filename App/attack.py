from flask import Flask,request,make_response,redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta


ip_dictionary = {}

def get_ip():
    return request.headers.get('X-Real-IP')
    #gets the ip check nginx.conf 

def limit_rate(ip_address):
    if(ip_address not in ip_dictionary):
        current_time = datetime.now()
        record = {'requests': 0, 'blocked_time': timedelta(seconds=0), 'request_time_period': timedelta(seconds=0),'isBlocked':False, 'first_request_time': current_time}
        ip_dictionary[ip_address] = record
        return success_response()
    else:
        client_record = ip_dictionary[ip_address]
        return handling_function(client_record,ip_address)

def handling_function(client_record,ip_address):
   
    #still supposed to be blocked? 
    current_time = datetime.now()


    if(client_record['blocked_time'] + timedelta(seconds=30) >= current_time and client_record['isBlocked'] == True):
        return overload_response()
    
    # need to block 
    if ((client_record['requests'] > 50) and (abs(current_time - client_record['first_request_time'])<= timedelta(seconds=10))):
        return(block_function(client_record))

    #blocked time period is over 
    if(current_time > client_record['blocked_time'] + timedelta(seconds=30) and client_record['isBlocked'] == True):
        return(unblock_function(client_record))
    
    # case where more then 50 requests in time more then 10 seconds: 
    if ((client_record['requests'] > 50) and (abs(current_time - client_record['first_request_time']) >= timedelta(seconds=10))):
        return(reset_operations(client_record))
        
    else:
        client_record['requests'] += 1
        client_record['request_time_period'] = current_time
        return success_response()


def reset_operations(client_record):
    current_time = datetime.now()
    client_record['requests'] = 0
    client_record['blocked_time'] = timedelta(seconds=0)
    client_record['request_time_period'] = timedelta(seconds=0)
    client_record['isBlocked'] = False
    client_record['first_request_time'] = current_time
    return success_response()

def block_function(client_record):
    current_time = datetime.now()
    client_record['blocked_time'] = current_time
    client_record['isBlocked'] = True
    return overload_response()



def unblock_function(client_record):
    client_record['isBlocked'] = False
    client_record['requests'] = 0
    current_time = datetime.now()
    client_record['first_request_time'] = current_time
    return success_response()



def overload_response():
    response = make_response(redirect('/'), 'Too Many Requests. Please try again later.')
    response.status_code = 429
    return response

def success_response():
    response = make_response(redirect('/'), 'Request successful.')
    response.status_code = 200
    return response

