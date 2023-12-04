from flask import Flask,request,make_response,redirect
from datetime import datetime, timedelta


ip_dictionary = {}

def get_ip():
    client_ip = request.headers.get('X-Real-IP')
    #gets the ip check nginx.conf 
    if(client_ip):
        return client_ip
    else:
        return request.remote_addr

def limit_rate(ip_address):
    if(ip_address not in ip_dictionary):
        current_time = datetime.now()
        #zero_datetime = datetime(1, 1, 1, 0, 0, 0, 0)
        record = {'requests': 0, 'blocked_time': current_time, 'request_time_period': current_time,'isBlocked':False, 'first_request_time': current_time}
        ip_dictionary[ip_address] = record
        return success_response()
    else:
        client_record = ip_dictionary[ip_address]
        return handling_function(client_record,ip_address)

def handling_function(client_record,ip_address):
   
    #still supposed to be blocked? 
    current_time = datetime.now()
    blocked_time = client_record['blocked_time']
    block_elapsed = current_time - blocked_time
    blockSec = block_elapsed.total_seconds()
    number_requests = client_record['requests']

    original_time = client_record['first_request_time']
    total_elapsed = current_time - original_time
    totalSec = total_elapsed.total_seconds()




    if ((timedelta(seconds=30) >= timedelta(seconds=blockSec)) and client_record['isBlocked'] == True):
        return overload_response()
    
    # need to block 
    if ((number_requests > 8) and (timedelta(seconds = totalSec)<= timedelta(seconds=10))):
        return(block_function(client_record))

    #blocked time period is over 
    if( timedelta(seconds=blockSec)> timedelta(seconds=30) and client_record['isBlocked'] == True):
        return(unblock_function(client_record))
    
    # case where more then 50 requests in time more then 10 seconds: 
    if ((number_requests > 8) and (timedelta(seconds = totalSec)>= timedelta(seconds=10))):
        return(reset_operations(client_record))
        
    else:
        client_record['requests'] += 1
        client_record['request_time_period'] = current_time
        return success_response()


def reset_operations(client_record):
    current_time = datetime.now()
    client_record['requests'] = 0
    client_record['blocked_time'] = current_time
    client_record['request_time_period'] = current_time
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
    response = make_response(redirect('/'), 429)
    response.headers['Content-Type'] = 'text/plain'
    response.data = 'Too Many Requests. Please try again later.'
    return response

def success_response():
    response = make_response(redirect('/'), 'Request successful.')
    response.status_code = 200
    return response

# def block_attack(ip_address , ip_dictionary):
#         if ip_address not in ip_dictionary:
#             dict[ip]= [datatime.now(),1,0]
#         else:
#             if check_delay:
#                 response = make_response(redirect('/'), 'Too Many Requests. Please try again later.')
#                 response.status_code = 429
#                 return response
#             prev_time = dict[ip][0]
#             response_amount = dict[ip][1]
#             seconds = seconds_difference(prev_time, datatime.now())
#             if(seconds <10.0):
#                 dict[ip][1] += 1
#                 if check_response_count:
#                         ip_dictionary[ip_address][2] = datatime.now()
#                         response = make_response(redirect('/'), 'Too Many Requests. Please try again later.')
#                         response.status_code = 429
#                         return response
#             else:
#                 dict[ip][0] = datatime.now()
#                 dict[ip][1] = 0

    # def check_delay(ip_address,ip_dictionary):
    #     the_delay = ip_dictionary[ip_address][2]
    #     if the_delay != 0 :
    #         seconds = seconds_difference(the_delay, datetime.now())
    #         if seconds > 30:
    #             dict[ip][2] = 0
    #             return False
    #         else:
    #             return True
    #     return False

    # def check_response_count(ip_address,ip_dictionary):
    #     the_responses = ip_dictionary[ip_address][1]
    #     if (the_responses > 50):
    #         return True
    #     return False
    # def seconds_difference(time1, time2):
    #     seconds = time2 - time1
    #     seconds = seconds.total_seconds()
    #     return seconds



