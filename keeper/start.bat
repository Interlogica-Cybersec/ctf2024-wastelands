pip install -r requirements.txt
start /B python app.py
start /B python browser.py
echo ""
sleep 2
start explorer "http://127.0.0.1:5000"