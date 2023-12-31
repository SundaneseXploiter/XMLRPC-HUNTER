import requests
import sys
import threading
import os
import socket
from termcolor import colored
from colorama import Fore 

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')
        
def banners():
    clear_screen()
    # Display the ASCII art banner
    print("                                                                                         ")
    print(Fore.RED + "_______ _______ _______ _____  _______ _______ _______ _______ _______  ")
    print(Fore.RED + "|     __|   |   |    |  |     \|   _   |    |  |    ___|     __|    ___|")
    print(Fore.WHITE + "|__     |   |   |       |  --  |       |       |    ___|__     |    ___|")
    print(Fore.WHITE + "|_______|_______|__|____|_____/|___|___|__|____|_______|_______|_______|")
    print(Fore.RED + f"════════════╦══════════════════════════════════════════════╦════════════")
    # Display additional information about the host/device
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print(Fore.RED + f"╔═══════════╩══════════════════════════════════════════════╩═══════════╗")
    print(Fore.LIGHTGREEN_EX + f"                           [ XMLRPC HUNTER ]            ")
    print(Fore.RED + f"╚══════════════════════════════════════════════════════════════════════╝")
    print(Fore.RED + f"[ ! ]{Fore.RESET} Author: {Fore.LIGHTRED_EX}SUSUDOSU {Fore.LIGHTGREEN_EX}EST - 2023")
    print(f"{Fore.GREEN}[ {Fore.RED}! {Fore.GREEN}]{Fore.RESET} Device: {host_name}")
    print(f"{Fore.GREEN}[ {Fore.RED}! {Fore.GREEN}]{Fore.RESET} Host  : {ip_address}")
    print(Fore.RED + f"════════════════════════════════════════════════╝")

def check_xmlrpc_enabled(url):
    xmlrpc_endpoint = url + '/xmlrpc.php'
    
    try:
        response = requests.post(xmlrpc_endpoint, data="", timeout=15)
        if response.status_code == 200:
            return (url, "YES", "XML-RPC server accepts POST requests only.")
        else:
            return (url, "NO", "XML-RPC server doesn't accept POST requests.")
    except requests.exceptions.RequestException:
        return (url, "NO", "XML-RPC server doesn't accept POST requests.")

def process_domain(domain, save_file, lock):
    result = check_xmlrpc_enabled(domain)
    if result and result[1] == "YES":
        with lock:
            with open(save_file, "a") as f:
                f.write(domain + "\n")
    
    if result:
        status = result[1]
        message = result[2]
        color = "green" if status == "YES" else "red"
        message_color = "blue" if status == "YES" else "yellow"
        if status == "NO":
            message_color = "red"
        if status == "TIMEOUT":
            message_color = "magenta"
        result_line = f"- {colored(result[0], color)} [ {colored(status, color)} ] {colored(message, message_color)}"
        print(result_line)

def main():
    banners()
    input_file = input(f"{Fore.LIGHTGREEN_EX}[ + ]{Fore.LIGHTWHITE_EX} List? : ")
    save_file = "good_xmlrpc.txt"
    
    with open(input_file, "r") as f:
        raw_domains = f.read().splitlines()

    domains = ["http://" + domain if not domain.startswith("http://") and not domain.startswith("https://") else domain for domain in raw_domains]
    
    num_threads = min(len(domains), os.cpu_count() * 2)  # Auto threads
    lock = threading.Lock()
    
    threads = []
    for domain in domains:
        thread = threading.Thread(target=process_domain, args=(domain, save_file, lock))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
