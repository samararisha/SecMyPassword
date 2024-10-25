#!/usr/bin/env python3
import re
import hashlib
import requests
import time
import sys
from colorama import Fore
from colorama import init, Fore, Style

def Banner(): 
    banner  = """
   _____           __  ___      ____                 
  / ___/___  _____/  |/  /_  __/ __ \____ ___________
  \__ \/ _ \/ ___/ /|_/ / / / / /_/ / __ `/ ___/ ___/
 ___/ /  __/ /__/ /  / / /_/ / ____/ /_/ (__  |__  ) 
/____/\___/\___/_/  /_/\__, /_/    \__,_/____/____/  
                      /____/                         

              By Samara Risha
              Tool: SecMyPass
"""
    return banner

def loading_animation(duration):
    """Displays a loading animation for a given duration."""
    end_time = time.time() + duration
    while time.time() < end_time:
        for symbol in '-\\|/':
            sys.stdout.write(f'\r{Fore.RED}Checking .... {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)  # Adjust the speed of the animation here

def is_common_password(password):
    # Hash the password with SHA-1
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    # Send the prefix to the HIBP API
    loading_animation(2) 
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    # Check if the suffix is in the response
    hashes = (line.split(':') for line in response.text.splitlines())
    for hash_suffix, count in hashes:
        if hash_suffix == suffix:
            return True, count
    return False, 0

def repeating_status(password): 
    repeat_count =1 
    for i in range (1 ,len(password)) : 
        if password[i]==password[i-1] : 
           repeat_count+=1
           if repeat_count >3 : 
               return False , password
        else : 
            repeat_count = 1
            
    return True ,password

def validation_check(password):
    found, password = repeating_status(password)
    while not found:
        password = input("Password contains more than 3 consecutive repeated characters.\nEnter the password again: ")
        found, password = repeating_status(password)
    
    found, password = length_check(password)  # Adjusted to consistently call length_check
    while not found:
        password = input("A length error, Enter the password meeting the length requirements: ")
        found, password = length_check(password)  # Adjusted to consistently call length_check
    return True, password



def complexity_check(password):
    checks = {
        'lower_needed': not re.search(r'[a-z]', password),
        'upper_needed': not re.search(r'[A-Z]', password),
        'digit_needed': not re.search(r'[0-9]', password),
        'special_needed': not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    }
    return checks
   
def enforce_complexity(password):
    complexity_issues = complexity_check(password)
    while any(complexity_issues.values()):
        if complexity_issues['lower_needed']:
            password = input("Password must contain at least 1 lowercase letter. Enter again: ")
        elif complexity_issues['upper_needed']:
            password = input("Password must contain at least 1 uppercase letter. Enter again: ")
        elif complexity_issues['digit_needed']:
            password = input("Password must contain at least 1 digit. Enter again: ")
        elif complexity_issues['special_needed']:
            password = input("Password must contain at least 1 special character. Enter again: ")
        complexity_issues = complexity_check(password)
    return True , password

    

def length_check(password) :
    size = len(password) 
    while size < 8 or size > 64: #length check
        if size < 8 : 
            password=input(f"The password must be at least 8, you still need {8 - size} characters to meet the minmum length \n enter the password again : ")
            size = len(password) 
        elif size > 64 : 
            password=input(f"The password must not exceed 64 characters , \n enter the password again")
            size = len(password) 
    global feedback
    feedback = []
    if size in range(8 , 12) : 
        feedback.append("Password meets the minimum length requirement but is weak due to its short length (8-11 characters)")
    elif size in range(12 , 16) : 
        feedback.append("Stronger than short passwords but still could be vulnerable if it lacks complexity (12-15 characters)")
    elif size in range(16 , 20) : 
        feedback.append("strong password due it its length (16-20 characters)")
    elif size >= 21 :
        feedback.append("Highly secure when it comes to it length (21+)")
    return True,password

    
print(Fore.LIGHTCYAN_EX +Banner())
password = input("Please enter your password: ") 
loading_animation(2)
print("\n")
cond1 , password = validation_check(password)
if cond1 : 
    print("Complexity Checking , don't change the Whole password\n")
    cond2 , password = enforce_complexity(password)
    if cond2 :
        print("IS a common password checking.....\n")
        found , count = is_common_password(password)
        if found:
           feedback.append( f"The password has been found {count} times! It might not be secure.")
        else:
            feedback.append("This password hasn't been found in known breaches.")
            
            
print("FeedBack: "+"\n".join(feedback))

