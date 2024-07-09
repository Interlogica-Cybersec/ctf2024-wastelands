## Keeper

By dirbusting using the provided wordlist we see that the `.git` folder is exposed. We can then use the [git dumper](https://github.com/arthaud/git-dumper) tool to dump the repo.

```shell
python git_dumper.py http://[IP]:5020/.git ./dump
```
From the keeper.html template file we can see that a XSS is possible.
Another thing we notice is that the form points to the very same page and uses the GET method.
For this reason we just need to add the confirmation message as the `msg` query parameter to the current URL.
We need to do this in very few characters, so we leverage a regex applied on the inner text of the element with id `wrapper` which we can access directly via dom clobbering (some hints on dom clobbering can be seen in the page, since other elements are accessed in the very same way).
Knowing these things, one possible way to do what we need is to update the `location` variable like this:

```html
<svg/onload=location+='&msg='+wrapper.innerText.split`"`[1]>
```

which is 60 chars long.