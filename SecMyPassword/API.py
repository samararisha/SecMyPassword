import hashlib
import requests

def is_common_password(password):
    # Hash the password with SHA-1
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    # Send the prefix to the HIBP API
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    # Check if the suffix is in the response
    hashes = (line.split(':') for line in response.text.splitlines())
    for hash_suffix, count in hashes:
        if hash_suffix == suffix:
            return True, count
    return False, 0

password = input("Enter a password to check: ")
found, count = is_common_password(password)
if found:
    print(f"The password has been found {count} times! It might not be secure.")
else:
    print("This password hasn't been found in known breaches.")
