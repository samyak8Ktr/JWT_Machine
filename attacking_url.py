from JWT_machine import take_user_input, get_url_from_user, clear, display_banner
import requests
import config


# These global variables will be the default setting for request
request_headers = {
    "Authorization": config.token,
    "User-Agent": "JWT-Machine/1.0"
}
method = "GET"
payload = ""


def display_web_request_banner():
    print("===================")
    print("[1] Enter the type of request (default 'GET')")
    print("[2] Enter the payload + content-type (only if the request is 'POST')")
    print("[3] Set the jwt header cookie or token")
    print("[4] Enter a custom user agent (default is JWT-Machine/1.0)")
    print("[5] Send the request!")
    print("[0] Go back")
    print("===================")


def display_request():
    print("The current request: ")
    print(method)
    print(request_headers)
    if method == "POST":
        print(payload)


def get_request_type():        
    print("===================")
    print("[1] attack")
    print("[2] Edit the web request")
    print("===================")

    while True:
        clear()
        display_banner()
        display_request()
        request_method = (take_user_input("Enter the request type: ")).upper()
        if request_method not in ["GET","PUT","DELETE","POST"]:
            print("Unsupported request type!")
            take_user_input("Press ENTER to continue..")
    
    return request_method


def make_a_web_request():
    global request_headers
    global method
    global payload

    if config.target_url == "":
        config.target_url = get_url_from_user()

    try:
        if method == "GET":
            response = requests.get(config.target_url, headers=request_headers)
        elif method() == "POST":
            response = requests.post(config.target_url, headers=request_headers, json=payload)
        elif method() == "PUT":
            response = requests.put(config.target_url, headers=request_headers, json=payload)
        elif method() == "DELETE":
            response = requests.delete(config.target_url, headers=request_headers)

    # Output 
        print(f"[{response.status_code}] {response.reason}")
        print("Response Body:\n", response.text)

    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


def edit_web_request():
    while True:
        clear()
        display_banner()
        display_request()
        display_web_request_banner()
        user_input_chr = take_user_input("Select an option: ")
        if user_input_chr in [i for i in ["01234"]]:
            break
    
    user_input = int(user_input_chr)

    while True:
        match user_input:
            case 1: #request type
                print("coming soon")
            case 2: #POST payload
                print("coming soon")            
            case 3: #JWT Header
                print("coming soon")
            case 4: #custom user agent
                print("coming soon")
            case 5: #send request
                make_a_web_request() 
            case 0: #go back
                break

        take_user_input("Press Enter to continue..")


def no_signature_verification_attack():
    while True:
        clear()
        display_banner()
        display_request()
        print("===================")
        print("[1] attack")
        print("[2] Edit the web request")
        print("===================")
        user_input = take_user_input("Making request..")

        if user_input == '1' or user_input == '2':
            break
    
    make_a_web_request()


def downgrade_attack():
    while True:
        clear()
        display_banner()
        display_request()
        print("===================")
        print("[1] attack")
        print("[2] Edit the web request")
        print("===================")
        user_input = take_user_input("")
        
        if user_input == '1' or user_input == '2':
            break
        
    make_a_web_request()