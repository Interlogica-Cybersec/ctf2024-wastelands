#!/usr/bin/env python3
import socket
import argparse
import time
import threading
import re
from messages import messages

# https://www.waveshare.com/wiki/Template:SIM800C_GSM/GPRS_HAT_User_Manual
connected_address = []

class SIM(object):
    _pin_ok = False
    _pin = 4321
    _pin_remaining = 4
    _wanted_apn = "apn.snadophone.domain"
    _apn_ok = False
    _gprs_ok = False
    _gprs_connected = False
    _wanted_smtp = ("smtp.snadophone.domain",25)
    _smtp_ok = False
    _wanted_smtp_user = ("john@groundstation.gov", "ILikeMyPeninsula32")
    _smtp_user_ok = False
    _wanted_smtp_recipient = "officedoor@groundstation.gov"
    _smtp_recipient_ok = False
    _door_pass_ok = False
    _ip_whitelisted = False
    _http_init = False
    _http_cid = False
    _http_url = False
    _http_wanted_endpoint = "officedoor.groundstation.gov"
    _http_endpoint_ok = False
    _unlocked = False
    _key = "NTRLGC{D00R_0P3N3D_4_Y0U}"

    def mapper(self, command:str) -> str:
        if not command.startswith("AT"):
            return ""
        print(command)
        commands = {
            "AT":{"f":self.return_ok},
            "AT+CPIN?":{"f":self.at_cpin_ask},
            "AT+CGATT?":{"f":self.at_cgatt},
            "AT+CSQ":{"f":self.at_csq},
            "AT+CGMR":{"f":self.at_cgmr},
            r"^AT\+CPIN=[\"']?(?P<pin>\d+)[\"']?$":{"f":self.at_cpin_set,"reg":True},
            r"^AT\+CMGL=[\"']?(?P<status>[A-Z0-9]+)[\"']?$":{"f":self.at_cmgl,"reg":True},
            r"^AT\+SAPBR=3,1,[\"']?(?P<ptype>[A-Z]+)[\"']?,[\"']?(?P<value>[A-Z\.]+)[\"']?$":{"f":self.at_sapbr_set,"reg":True},
            r"^AT\+SAPBR=(?P<context>\d+),(?P<profile>\d+)$":{"f":self.at_sapbr,"reg":True},
            r"^AT\+(?P<cmd>CSTT|CIP)":{"f":self.at_notenabled,"reg":True},
            r"^AT\+EMAIL(?P<cmd>CID|TO)=\d+":{"f":self.return_ok,"reg":True},
            r"^AT\+SMTPSRV=[\"']?(?P<smtp>[A-Z\.]+)[\"']?,(?P<port>\d+)":{"f":self.at_smtpsrv,"reg":True},
            r"^AT\+SMTPAUTH=1,[\"']?(?P<email>[A-Z\.@]+)[\"']?,[\"']?(?P<password>[A-Z0-9]+)[\"']?":{"f":self.at_smtpauth,"reg":True},
            r"^AT\+SMTPFROM=(?P<cmd>.*)":{"f":self.return_ok,"reg":True},
            r"^AT\+SMTPRCPT=0,0,[\"']?(?P<email>[A-Z\.@]+)[\"']?,[\"']?(?P<name>[A-Z0-9]+)[\"']?$":{"f":self.at_smtprcpt,"reg":True},
            r"^AT\+SMTPRCPT=1,0,(?P<cmd>.*)":{"f":self.return_ok,"reg":True},
            r"^AT\+SMTPSUB=[\"']?(?P<password>[A-Z0-9]+)[\"']?$":{"f":self.at_smtpsub,"reg":True},
            r"^AT\+SMTPBODY=(?P<cmd>.*)":{"f":self.return_ok,"reg":True},
            "AT+SMTPSEND":{"f":self.at_smtpsend},
            "AT+HTTPINIT":{"f":self.at_httpinit},
            r"^AT\+HTTPPARA=[\"']?(?P<param>[A-Z0-9]+)[\"']?,[\"']?(?P<value>[A-Z0-9\.]+)[\"']?$":{"f":self.at_httpara,"reg":True},
            "AT+HTTPACTION=0":{"f":self.at_httpaction},
            "AT+HTTPREAD":{"f":self.at_httpread},
            "AT+HTTPTERM":{"f":self.at_httpterm}
        }
        for c in commands:
            if "reg" in commands[c]:
                m = re.match(c, command)
                if m:
                    print(c,command)
                    print(m.groupdict())
                    return commands[c]["f"](**m.groupdict())
            elif command == c:
                print(c)
                return commands[c]["f"]()
        return "ERROR"
    
    def at_csq(self):
        return "+CSQ: 25,0\n\nOK"
    
    def at_cgmr(self):
        return "Revision:13377331SIM800C\n\nOK"

    def at_httpterm(self):
        if not self._http_init:
            return "+CME ERROR: HTTP not initialized!"
        self._http_init = False
        return "OK"

    def at_httpread(self):
        if not self._http_init:
            return "+CME ERROR: HTTP not initialized!"
        if not self._unlocked:
            return "\n\nOK"
        return f"{self._key}\nOK"

    def at_httpaction(self):
        if not self._http_init:
            return "+CME ERROR: HTTP not initialized!"
        if self._http_endpoint_ok:
            if self._ip_whitelisted:
                self._unlocked = True
                return f"OK\n\n+HTTPACTION: 0,200,{len(self._key)}"
            return "OK\n\n+HTTPACTION: 0,401,0"
        return "OK\n\n+HTTPACTION: 0,504,0"

    def at_httpara(self, param:str, value:str) -> str:
        if not self._http_init:
            return "+CME ERROR: HTTP not initialized!"
        if param == "CID" and int(value) == 1:
            self._http_cid = True
            return "OK"
        elif param == "URL":
            if self._http_wanted_endpoint.upper() in value:
                self._http_endpoint_ok = True
            else:
                self._http_endpoint_ok = False
            return "OK"
        return "ERROR"
    
    def at_httpinit(self) -> str:
        if not self._gprs_connected:
            return "+CME ERROR: GPRS needs to be connected!"
        self._http_init = True
        return "OK"

    def at_smtpsend(self) -> str:
        if not self._gprs_connected:
            return "+CME ERROR: GPRS needs to be connected!"
        if self._door_pass_ok and self._smtp_ok and self._smtp_recipient_ok and self._smtp_user_ok:
            self._ip_whitelisted = True
            return "+SMTPSEND: IP WHITELISTED\n\nOK"
        return "+CME ERROR: Something went wrong! (Invalid data?)"

    def at_smtpsub(self, password:str) -> str:
        if not self._gprs_connected:
            return "+CME ERROR: GPRS needs to be connected!"
        if password == self._wanted_smtp_user[1].upper():
            self._door_pass_ok = True
        else:
            self._door_pass_ok = False
        return "OK"

    def at_smtprcpt(self, email:str, name:str = "") -> str:
        if not self._gprs_connected:
            return "+CME ERROR: GPRS needs to be connected!"
        if email == self._wanted_smtp_recipient.upper():
            self._smtp_recipient_ok = True
            return "OK"
        else:
            self._smtp_recipient_ok = False
        return "+CME ERROR: Unexistent email!"

    def at_smtpauth(self, email:str, password:str) -> str:
        if not self._gprs_connected:
            return "+CME ERROR: GPRS needs to be connected!"
        if email == self._wanted_smtp_user[0].upper():
            if password == self._wanted_smtp_user[1].upper():
                self._smtp_user_ok = True
                return "OK"
        self._smtp_user_ok = False
        return "+CME ERROR: LOGIN FAILED!"

    def at_smtpsrv(self, smtp:str, port:str) -> str:
        if not self._gprs_connected:
            return "+CME ERROR: GPRS needs to be connected!"
        if smtp == self._wanted_smtp[0].upper():
            if int(port) == self._wanted_smtp[1]:
                self._smtp_ok = True
                return "OK"
        self._smtp_ok = False
        return "+CME ERROR: OFFICIAL SNADOPHONE SMTP ONLY!"

    def return_ok(self, cmd:str = "") -> str:
        if not self._pin_ok:
            return "+CME ERROR: SIM PIN required"
        return "OK"

    def at_notenabled(self, cmd:str) -> str:
        if cmd == "CSTT":
            return "+CME ERROR: not supported. Check alternative: SAPBR"
        elif cmd == "CIP":
            return "+CME ERROR: not supported. Check alternative: HTTP"
        return "ERROR"

    def at_cgatt(self) -> str:
        val = int(self._gprs_connected)
        return f"+CGATT: {val}"

    def at_cpin_ask(self) -> str:
        if not self._pin_ok:
            if self._pin_remaining:
                return "+CPIN: SIM PIN"
            else:
                return "+CPIN: SIM PUK"
        return "OK"
    
    def at_cpin_set(self, pin:int) -> str:
        pin = int(pin)
        if not pin == self._pin or not self._pin_remaining:
            if self._pin_remaining:
                self._pin_remaining -= 1
                return "+CME ERROR: 16"
            return "+CME ERROR: 16 SIM LOCKED"
        self._pin_remaining = 3
        self._pin_ok = True
        return "OK"
        
    def at_sapbr_set(self, ptype:str, value:str) -> str:
        if not self._pin_ok:
            return "+CME ERROR: SIM PIN required"
        if not ptype in ["CONTYPE","APN"]:
            return "ERROR"
        if ptype == "CONTYPE":
            if value == "GPRS":
                self._gprs_ok = True
                return "OK"
            self._gprs_ok = False
        elif ptype == "APN":
            if value == self._wanted_apn.upper():
                self._apn_ok = True
            else:
                self._apn_ok = False
            return "OK"
        return "ERROR"

    def at_sapbr(self, context:int, profile:int):
        if not self._pin_ok:
            return "+CME ERROR: SIM PIN required"
        context = int(context)
        if context not in [0,1,2]:
            return "ERROR"
        profile = int(profile)
        if profile != 1:
            return "ERROR"
        if context == 1:
            if self._gprs_ok and self._apn_ok:
                self._gprs_connected = True
                return "OK"
            return "ERROR"
        elif context == 2:
            if self._gprs_connected:
                return "+SAPBR: 1,1,\"10.69.96.10\"\n\nOK"
        elif context == 0:
            self._gprs_connected = False
        return "ERROR"
        

    def at_cmgl(self, status:str) -> str:
        if not self._pin_ok:
            return "+CME ERROR: SIM PIN required"
        msgid = 0
        toreturn = []
        if status.isnumeric():
            msgid = int(status)
            if msgid <= 0 or msgid > len(messages):
                return "ERROR"
            msg = messages[msgid]
            msg["id"] = msgid
            toreturn.append(msg)
        else:
            if not status in ["ALL","READ","UNREAD","SENT"]:
                return "ERROR"
            x = 0
            for msg in messages:
                if status == "ALL" or msg["status"].upper() == status:
                    msg["id"] = x
                    toreturn.append(msg)
                x += 1
        data = ""
        for msg in toreturn:
            data += f'+CMGL: {msg["id"]},"REC {msg["status"].upper()}","{msg["from"]}","",{msg["date"]},{msg["time"]}\n{msg["msg"]}\n\n'
        return data

def worker(conn:socket.socket, addr:str, fast:bool = False):
    sim = SIM()
    rst = "+RST+SIM"
    header = "SIM800C GSM EMULATOR LOADING (System Powered by S.N.A.D.O. Technologies)"
    baud = "\n\t[+]ONLINE\nSETTING BAUD RATE TO 115200"
    subh = f"\n\t[+]CONNECTED\n[i]RESTORE SIM BACKUP WITH: {rst}\n"
    subh += "[!]Notice: this is an emulated console, commands may be limited.\n"
    try:
        with conn:
            if addr[0] in connected_address:
                conn.sendall(">Limited to 1 connection per IP!<\n".encode())
                conn.shutdown(socket.SHUT_RDWR)
                return
            connected_address.append(addr[0])
            conn.sendall(header.encode())
            for i in range(0,5):
                conn.sendall(".".encode())
                if not fast:
                    time.sleep(1)
            conn.sendall(baud.encode())
            for i in range(0,3):
                conn.sendall(".".encode())
                if not fast:
                    time.sleep(1)
            conn.sendall(subh.encode())
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                sdata = data.decode().strip().upper()
                if sdata == rst:
                    sim = SIM()
                    conn.sendall(f"\n\n[i]Sim restored!\n".encode())
                    continue
                r = sim.mapper(sdata)
                conn.sendall(f"{r}\n".encode())
            conn.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print(e)
        pass
    connected_address.remove(addr[0])
    print("Client disconnected ->",addr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host","-H",default="0.0.0.0")
    parser.add_argument("--port","-p",default=9000)
    parser.add_argument("--fast","-f",action="store_true")
    args = parser.parse_args()
    while True:
        try:
            with socket.socket() as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((args.host, args.port))
                print(f"Listening on {args.host}:{args.port} ...")
                s.listen(1000)
                while True:
                    sock, addr = s.accept()
                    print("New connection received ->",addr)
                    t = threading.Thread(target=worker, kwargs={"conn":sock,"addr":addr,"fast":args.fast})
                    t.daemon = True
                    t.start()
        except Exception as e:
            time.sleep(1)
            continue
if __name__ == "__main__":
    main()