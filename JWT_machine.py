# This is a project i will be using to work on JWT security
import os
import sys
import jwt
import json
import binascii
import base64
import re
import config
import attacking_url
import pyfiglet
from rich import print
from rich.panel import Panel


# Global Variables here:
required_arguments = 1
number_of_options = 8

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


#I will display a cool hacker's banner on top
def display_banner():
    title = pyfiglet.figlet_format("JWT Machine", font="mono9")
    print(f"{title}")
    banner = "[bold red]Made By[/bold red] SAMYAK KATIYAR"
    #print(Panel(title))
    print(Panel(banner, subtitle="Token Exploiter | Decoder | Brute-Forcer"))
    print(f"\nToken: {config.token}\nsecret: {config.secret_value}\nURL: {config.target_url}\n")


def display_menu(): 
    print("===================")
    print("[1] Decode Token")
    print("[2] Enter / Change the URL to be tested for")
    print("[3] Manually edit the token")
    print("[4] sign the payload with a secret")
    print("[5] Check if application is not verifying the JWT signature")
    print("[6] Check for downgrade attack")
    print("[7] Bruteforce to check for weak symmetric secrets")
    print("[8] Enter the secret if already known")
    print("[0] Exit")
    print("===================")


def take_user_input(display_line):
    try:
        user_input = input(display_line)
        return user_input
    except KeyboardInterrupt:
        print("\nGood Bye..")
        exit()


# This program will return a tuple
def process_jwt(token):
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        print("Invalid JWT format. Should have 3 parts.")
        return None, None, None, False

    # Decode without verification to inspect parts
    try:
        header = jwt.api_jws.base64url_decode(header_b64.encode())
        payload = jwt.api_jws.base64url_decode(payload_b64.encode())
        signature = signature_b64  
    except binascii.Error: # Catch is user enters an invalid base64 value
        print("Invalid JWT")
        return None, None, None, False

    try:
        #header_string = json.dumps(json.loads(header), indent=4)
        header_json = json.loads(header)
        print("converting it to json")
        #payload_string = json.dumps(json.loads(payload), indent=4)
        payload_json = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as e: # catch if decoded base64 is not a valid json 
        #print("A non valid token: {}",e)
        return None, None, None, False

    return header_json, payload_json, signature, True


def show_decoded_token(header, payload, signature):
    print("\n--- Header ---")
    #print(type(header))
    print(json.dumps(header, indent=4))
    print("\n--- Payload ---")
    print(json.dumps(payload, indent=4))
    print(f"\nSignature: {signature}")


def get_url_from_user():
    pattern = r"^https?://(?:[a-zA-Z0-9.-]+|\d{1,3}(?:\.\d{1,3}){3})(?:/[^\s?]*)?(?:\?[^\s]*)?$"

    while True:
        clear()
        display_banner()
        url = input("Enter the target URL or press Enter to go back: ")
        if url == "":
            return ""
        else:
            if re.match(pattern, url):
                return url
            else:
                take_user_input("Enter a valid URL..\nPress Enter to continue")


def display_edit_token_banner():
    print("===================")
    print("[1] Edit the header")
    print("[2] Edit the playload")
    print("[3] Edit the signature")
    print("[0] to go back")
    print("===================")


def edit_token(header, payload, signature): #only expects 'header' or 'payload'
    new_header_json = header
    new_payload_json = payload
    new_signature = signature

    while True:
        clear()
        display_banner()
        display_edit_token_banner()
        print('Use {"key":"value"} format and double inverted commas\n')
        user_input_chr = take_user_input("Select an option: ")
        if user_input_chr in [i for i in '0123']:
            user_input = int(user_input_chr)
            break
        print("Select a valid option, press Enter to continue")

    if user_input == 1: # edit header
        while True:
            clear()
            display_banner()
            print(f"Current Header: {header}")
            new_header = take_user_input("Enter the new header: ")
            try:
                new_header_json = json.loads(new_header)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("Use the specified format!")
                continue
            break

    elif user_input == 2: # payload
        while True:
            clear()
            display_banner()
            print(f"Current Payload: {payload}")
            new_payload = take_user_input("Enter the new payload: ")
            try:
                new_payload_json = json.loads(new_payload)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("Use the specified format!")
                continue
            break

    elif user_input == 3:
        new_signature = take_user_input("Enter the signature you want to replace with current signature: ")

    else:
        return new_header_json, new_payload_json, new_signature

    return new_header_json, new_payload_json, new_signature


def encode_dict_to_base64_string(dict):
    json_string = json.dumps(dict) # to string
    json_bytes = json_string.encode('utf-8') # to bytes
    base64_bytes = base64.urlsafe_b64encode(json_bytes) # to base64 encoded bytes 
    b64_str = base64_bytes.decode('utf-8') # to string

    return b64_str


def update_token(header, payload, signature): # Update the global token 
    header_b64 =  encode_dict_to_base64_string(header)
    payload_b64 =  encode_dict_to_base64_string(payload)
    
    config.token = '.'.join([header_b64.rstrip('='), payload_b64.strip('='), signature])


def forge_jwt(header, payload):
    if config.secret_value == "":
        config.secret_value = take_user_input("Enter the known secret or press Enter to go back: ")
        if config.secret_value == "":
            return

    config.token = jwt.encode(payload, config.secret_value, algorithm="HS256", headers=header)
    print(f"The new token: {config.token}")

    signature = config.token.split(".")[2]

    return signature    


# def no_signature_verification_attack(): #I will place this in attacking_url.py
#     print("checking for no signature verification attack")


# def downgrade_attack(): # I will plcae this in attacking_url.py
#     print("checking for downgrade attack")


def display_bruteforce_banner():
    print("===================")
    print("[1] Use the default wordlist")
    print("[2] Provide another wordlist")
    print("[3] Go Back")
    print("===================")


def bruteforce_jwt_for_secrets(user_input): #only expect '1' or '2' here
    if user_input == '1':
        print("Bruteforcing JWT fot secrets")
        #Using default wl
    else:
        take_user_input("Enter the custom wordlist path")
        #Using a custom wordlist


def main():

    while True: # loop to get a valid token
        clear()
        display_banner()
        
        config.token = take_user_input("Enter a valid JWT Token: ")
        header, payload, signature, result = process_jwt(config.token) #returns dict data type json.loads() used
        if (result):
            print("valid Token")
            break
        else:
            take_user_input("\n\nPress Enter to use continue..")
            
    while True: #loop to remove to config.token input by user and take input for menu
        clear()
        display_banner()
        display_menu()
        user_input_chr = take_user_input("Select an Option: ")

        if user_input_chr not in [i for i in '012345678']:
            print("Enter a valid option!")
            take_user_input("press Enter to continue..")
            continue

        user_input = int(user_input_chr)

        match user_input:
            case 1: # decode config.token
                show_decoded_token(header, payload, signature)
            case 2: # Enter URL
                #config.target_url = take_user_input("Enter URL to be tested against: ")
                config.target_url = get_url_from_user()
            case 3: # Edit config.token
                header, payload, signature = edit_token(header, payload, signature)
                #update config.token here
                update_token(header, payload, signature)
            case 4: # Forge Token
                print("coming soon")
                signature = forge_jwt(header, payload)
                update_token(header, payload, signature)
            case 5: # not verifying
                attacking_url.no_signature_verification_attack()
            case 6: # downgrade attack
                attacking_url.downgrade_attack()
            case 7:
                while True: # Loop to take valid option
                    clear()
                    display_banner()
                    display_bruteforce_banner()

                    user_input = take_user_input("Enter a valid option: ")

                    if user_input not in ['1','2','0']:
                        print("Enter a valid option..")
                        continue
                    elif user_input == '0':
                        break
                    else:
                        bruteforce_jwt_for_secrets(user_input)
            case 8:
                config.secret_value = take_user_input("Enter the secret value: ")
                # verify and forge the config.token
            case 0:
                print("Good Bye..")
                exit()

        take_user_input("\n\nPress Enter to use continue..")


if __name__ =="__main__":
    if len(sys.argv) == required_arguments + 1 and sys.argv[1] == "-h":
        print("Usage: python3 JWT_machine.py <flags>")
    elif len(sys.argv) == (required_arguments + 1) and sys.argv[1] == "-v":
        print("JWT_machine version 1.0 \n   --Samyak Katiyar")
    else:
        main()