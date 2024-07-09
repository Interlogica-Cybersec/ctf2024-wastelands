def execute():
    with open('/root/flag.txt', 'r') as flag_file:
        flag_content = flag_file.read().strip()
        print("Remote control authorized. Loading " + flag_content + " module")