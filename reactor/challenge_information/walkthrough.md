## Reactor

There is a login panel that uses the following parameters:

    username
    password
    systemId

where the hidden `systemId` parameter is hardcoded to the value `1337`.
By trying different characters we see that the following characters are prohibited:
`'`, ` `, `\t`, `-`, `;`, `/`, `*`.

Let's try to infer the sql query behind the login page. It might look like one of the following:

    SELECT id FROM users WHERE username = 'xxx' AND password = 'yyy' AND system_id = {system_id}
    SELECT id FROM users WHERE (username = 'xxx') AND (password = 'yyy') AND (system_id = {system_id})
    SELECT id FROM users WHERE (username = 'xxx') AND (password = 'yyy') AND (system_id is null or system_id = {system_id})

The `systemId` is the most promising parameter, since there's a high chance that it's numeric on the database, and for this reason the `'` character might not be necessary for a successful injection. The other two parameters might be used as well with more advanced attacks (such as by putting a`\` character in front of the closing `'` and by using `"` to poison the query), but let's see if a simpler way is possible.

Let's suppose the query looks like the first one we inferred. The following payload would work for the `systemId` parameter:

    1or1

because the query would then look like this:

    SELECT id FROM users WHERE username = 'xxx' AND password = 'yyy' AND system_id = 1or1

which returns all the users and allows for a successful login. This unfortunately does not work.

Let's see if the query looks like one of the other two we inferred. In that case the following payload would work:

    1)or(1

which would make the query look like one of the following two:

    SELECT id FROM users WHERE (username = 'xxx') AND (password = 'yyy') AND (system_id = 1)or(1)
    SELECT id FROM users WHERE (username = 'xxx') AND (password = 'yyy') AND (system_id is null or system_id = 1)or(1)

and both would return all the users in the table and allow for a successful login. This time it works.

The control panel requires an otp to be inserted by the user and we need to find its value.

We can now dirbust a little: we will find that a `logs` folder exists inside `/control-panel`, which contains a `debug.log` file. We can use that log file to see the otp sent to the user: with that information we can now start the activation sequence.