
# smuggler.py

### # Summary

This tool is that send request to target server using simple payload for detecting http request smuggling.

But.. It is not finished yet, and is developing.


### # How to use

```
  -h, --help         show this help message and exit
  --url URL          Input url. --url http://test.com
  --agent            Generating random User-Agent. --agent
  --timeout TIMEOUT  Set timeout. Default: 7s. --timeout [time]
```


### # Result

##### # CL.TE timing tech
If CL.TE case, tool sends a payload like below.

```
POST {} HTTP/1.1\r\n
Host: {}\r\n
Content-Length: 4\r\n
Transfer-Encoding: chunked\r\n
\r\n
```

When server's response is timeout, server is vulnerable to http request smuggling.

Tool will show the result like below.
```
ubuntu:~/environment/git/smuggler.py (master) $ python3 smuggler.py --url https://ac9f1faa1f71d93b807b054000660013.web-security-academy.net/ --agent

                                         _                             
         ___ _ __ ___  _   _  __ _  __ _| | ___ _ __       _ __  _   _ 
        / __| '_ ` _ \| | | |/ _` |/ _` | |/ _ \ '__|     | '_ \| | | |
        \__ \ | | | | | |_| | (_| | (_| | |  __/ |     _  | |_) | |_| |
        |___/_| |_| |_|\__,_|\__, |\__, |_|\___|_|    (_) | .__/ \__, |
                             |___/ |___/                  |_|    |___/ 
                        by universe 

[*] Generating fake user-agent...
[*] Done.
[*] Sending to https://ac9f1faa1f71d93b807b054000660013.web-security-academy.net/
[*] Testing CL.TE...
     └───> HTTP/1.1 500 Internal Server Error
[*] Server using CLTE
>> 
====== payload ======
POST / HTTP/1.1
Host: ac9f1faa1f71d93b807b054000660013.web-security-academy.net
Content-Length: 4
Transfer-Encoding: chunked

0


======================

```

### # Update

 #### - v0.2

Fixed an error when user don't input url including http:// or https://.

Fixed an bug not including fake user agent.

Added function that subdomain is scanned.

Added option for importing list. [(Issue 1)](https://github.com/Lactea98/smuggler.py/issues/1)

### # Reference 
https://portswigger.net/web-security/request-smuggling

https://github.com/gwen001/pentest-tools/blob/master/smuggler.py
