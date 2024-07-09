## Unauthorized

By dirbusting the web application with the provided wordlist, we discover that the `/status` endpoint is accessible.
From there we can see the logs of the previous requests.
There is a particularly interesting header, `X-Role`, which we can leverage if we can manage to guess the role for admins.
Let's try to do header injection via the value of the username sent to the `/verify` endpoint, which appears in the `x-Username` header.
If it works, the new `X-Role` line we inject will overwrite the value for the old one.

The first role we can try is the `admin` role. We can do this by injecting a new-line character (`%0a`) in the username and rewriting the `X-Role` header:

    /verify?username=himom%0aX-Role:+admin

Cool, it worked. At the beginning of the status page we can now see the message `Access granted` and an auth link.
That link will contain the flag.

As a bonus vuln, we can craft the following payload to trigger a reflected xss:

    /verify?username=%0aContent-type:+text/html%0a%0a<img+src=x+onerror=alert(1)>