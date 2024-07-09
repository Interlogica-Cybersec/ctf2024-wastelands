## Medpod

We need to start the therapy, but the feature is disabled for our user.

When we open the webpage, an automatic login is performed and the server returns a JWT token, which the frontend application stores in the browser's session storage.
It turns out that this token has a weak secret. Let's crack it using hashcat and the rockyou wordlist:

```shell
hashcat -m 16500 -a 0 jwt_token.txt rockyou.txt
```
Ah wow, the secret is `NUKENUKE`.

The user id is represented by the `sub` claim in the token. The server will most surely use that value to check for permissions or to perform various database queries. Let's see if we can perform a SQL injection. We can leverage https://jwt.io to edit, sign again the token and put it into the session storage.
It turns out that the following payload, when used against the `sub` claim works:

```sql
' or '1'='1
```
The therapies list now shows a new entry linked to another doctor, of which we can retrieve the uuid by inspecting the data sent from the server.
Let's put that uuid as the value of the `sub` claim, sign and put the new token in the browser's session token.

We are finally able to start the therapy and retrieve the flag.