from time import time
import uuid
from datetime import datetime
from termcolor import colored, cprint
# from functools import wraps
class Services:
 
    def timer_func(func): 
        # This function shows the execution time of 
            # the function object passed 
            def wrap_func(*args, **kwargs): 
                t1 = time() 
                result = func(*args, **kwargs) 
                t2 = time() 
                cprint(f'                                                                                   Function {func.__name__!r} executed in {(t2-t1):.4f}s', 'cyan',attrs=['bold']) 
                return result 
            return wrap_func
    
    def generators(n):
         val = 0
         while(val < n):
            yield val
            val+=1

    def lower_replace(text):
         lowercase_text=text.lower()
         no_space_text=lowercase_text.replace(" ", "")
         print("iniside fun",no_space_text)
         return no_space_text

    def unique_id_generator():
         while True:
              yield uuid.uuid4()

    def generate_booking_ids():
        counter = 0
        while True:
            timestamp = str(datetime.now().time())
            booking_id = f"{timestamp}{counter:03d}"
            print(f"booking id: {booking_id}")
            counter += 1
            yield booking_id

# Create a generator for booking IDs
    
    def get_next_booking_id():
        booking_id_generator = Services.generate_booking_ids()
        return booking_id_generator



