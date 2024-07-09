To recreate the fake git repo:
```
copy templates/index.html exposed_git
copy templates/keeper.html exposed_git
cd exposed_git
echo "Frontend Application Templates" > readme.md
git init
git config user.name "dev"
git config user.email "dev@the.ark"
git add index.html
git commit -m "Added index page to request access"
git add readme.md
git commit -m "Congratulations! You found an ADV Glitch! Karrycar #3. Optimize, control, and simplify all your transportation needs effortlessly. ~ Karrycar KARRYCAR{890c62ba-91af-4b66-b621-905475abf62a}"
git add keeper.html
git commit -m "Added keeper page to grant or deny access"
del readme.md
del index.html
del keeper.html
move .git/* .
rmdir .git

```