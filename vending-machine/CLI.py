#!/usr/bin/env python3

import os
from colorama import init, Fore, Style

init()  # colorama

def welcome():
    print(f"\n  {Fore.YELLOW}local console{Style.RESET_ALL}\n")
    
products_content = [
    {
        "name": "Syntho-Meat Burger",
        "price": 4.99
    },
    {
        "name": "Neon Energy Drink",
        "price": 3.49
    },
    {
        "name": "Crispy Insect Protein Bar",
        "price": 3.99
    },
    {
        "name": "Artificial Oxygen Canister",
        "price": 8.5
    },
    {
        "name": "Dehydrated Pizza Slice",
        "price": 3.25
    },
    {
        "name": "Vitamin D Capsules",
        "price": 6.49
    },
    {
        "name": "Noodles",
        "price": 5.75
    },
    {
        "name": "Adrenaline Injector",
        "price": 19.99
    },
    {
        "name": "Popcorn with chocolate",
        "price": 2.75
    },
    {
        "name": "Psychoactive Mushroom Capsules",
        "price": 11.49
    },
    {
        "name": "Protein Shake",
        "price": 5.99
    },
    {
        "name": "Sushi Rolls",
        "price": 4.75
    },
    {
        "name": "Protein Snack Bar",
        "price": 3.99
    },
    {
        "name": "Cheap veg Soup",
        "price": 3.49
    },
    {
        "name": "Ramen Cup",
        "price": 3.75
    },
    {
        "name": "Bioluminescent Jelly",
        "price": 6.49
    },
    {
        "name": "SARS-COV-2 swab test",
        "price": 24.99
    },
    {
        "name": "Hydroponic Algae Snack",
        "price": 3.25
    },
    {
        "name": "Sonic Boom Energy Drink",
        "price": 4.49
    },
    {
        "name": "Chaos Theory Chocolate",
        "price": 3.99
    },
    {
        "name": "Classic Tomato Soup",
        "price": 3.49
    },
    {
        "name": "Chunky Vegetable Stew",
        "price": 4.99
    },
    {
        "name": "Tuna Salad",
        "price": 5.25
    },
    {
        "name": "Chicken Noodle Soup",
        "price": 3.99
    },
    {
        "name": "Beef Ravioli",
        "price": 4.75
    },
    {
        "name": "Spaghetti and Meatballs",
        "price": 6.49
    },
    {
        "name": "Macaroni and Cheese",
        "price": 3.75
    },
    {
        "name": "Green Beans",
        "price": 2.99
    },
    {
        "name": "Corn",
        "price": 2.49
    },
    {
        "name": "Peaches",
        "price": 3.25
    }
]

def version():
    print(f"\n  product: SND0 - secured vending machine\n"
             "  firmware:  v.2.8.0.1\n"
             "  written by: Danny 'the dog' Hogan\n\n"
             "  Congratulations!\n"
             "  You found and adv glitch! 4ISP #3\n\n"
             "  For years, we have been supporting SMEs by implementing and managing corporate networks and systems, from technical analysis to solutions.\n\n"
             "  https://www.4isp.it\n\n"
            f"  {Fore.CYAN}4ISP{{018c125b-7519-4ad7-b895-5b53cb4a817e}}{Style.RESET_ALL}\n"
             "")

def show_products():
    if products_content:
        print(f"\n  {Fore.YELLOW}Products{Style.RESET_ALL}\n")
        for idx, product in enumerate(products_content, start=1):
            print(f"  {idx}. {Fore.CYAN}{product['name']}{Style.RESET_ALL} - {product['price']} credits")
        print()
    else:
        print(f"\n  {Fore.RED}no products available{Style.RESET_ALL}\n")
        init = input(f"\n  {Fore.YELLOW}does the vending machine need initialization (y/n)?{Style.RESET_ALL}: ")
        if init == "y":
            installation_mode()
        elif init == "n":
            main()
        else:
            print("\n  Invalid input. Please enter 'y' or 'n'.\n")
            show_products()

def add_product():
    print(f"\n  {Fore.YELLOW}add Product{Style.RESET_ALL}\n")
    name = input("\n  enter product name: ")
    price = input("\n  enter product price: ")

    if len(name) > 10:
        print(f"\n  {Fore.RED}product name must be 10 characters or less{Style.RESET_ALL}\n")
        return

    try:
        price = float(price)
    except ValueError:
        print(f"\n  {Fore.RED}price must be a valid number{Style.RESET_ALL}\n")
        return

    products_content.append({"name": name, "price": price})
    print(f"\n  {Fore.GREEN}product added successfully{Style.RESET_ALL}\n")
    show_products()

def remove_product():
    print(f"\n  {Fore.YELLOW}remove product{Style.RESET_ALL}\n")
    show_products()
    
    if not products_content:
        print(f"\n  {Fore.RED}No products available to remove{Style.RESET_ALL}\n")
        return
    
    while True:
        try:
            index = int(input("  index of the product to remove: "))
            if 1 <= index <= len(products_content):
                removed_product = products_content.pop(index - 1)
                print(f"\n  {Fore.GREEN}Product removed successfully{Style.RESET_ALL}\n")
                show_products()
                break
            else:
                print(f"\n  {Fore.RED}Invalid product index. Please enter a valid index.{Style.RESET_ALL}\n")
        except ValueError:
            print(f"\n  {Fore.RED}Invalid input. Please enter a valid index.{Style.RESET_ALL}\n")

def installation_mode():
    print(f"\n  {Fore.YELLOW}initialization mode{Style.RESET_ALL}\n")
    
    machine_name = None
    location = None
    ssid = None
    password = None

    while True:
        print("  1. machine name")
        print("  2. location")
        print("  3. wifi ssid")
        print("  4. wifi password")
        print("  5. create vmachine.conf")
        print("  6. deploy settings")
        choice = input(f"\n  {Fore.YELLOW}select{Style.RESET_ALL}: ")
        if choice == "1":
            machine_name = input("  enter vending machine name: ")
        elif choice == "2":
            location = input("  location: ")
        elif choice == "3":
            ssid = input("  wifi ssid: ")
        elif choice == "4":
            password = input("  wifi password: ")
        elif choice == "5":
            os.system("vim -Z vmachine.conf")
        elif choice == "6":
            if machine_name and location and ssid and password:
                confirmation = input("\n  deploy settings now? (y/n): ")
                if confirmation.lower() == "y":
                    print("\n  starting vending machine...")
                    os._exit(0)
                else:
                    continue
            else:
                print(f"\n  {Fore.RED}Please fill out all required fields before deploying.{Style.RESET_ALL}\n")
        else:
            print(f"\n  {Fore.RED}Invalid option{Style.RESET_ALL}\n")

def maintenance():
    while True:
        print(f"\n  {Fore.YELLOW}maintenance mode{Style.RESET_ALL}\n")
        print("  1. add product")
        print("  2. remove product")
        print("  3. exit maintenance mode")
        print()
        choice = input("Select an option: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            remove_product()
        elif choice == "3":
            print(f"\n  {Fore.YELLOW}exiting maintenance mode{Style.RESET_ALL}\n")
            return
        else:
            print(f"\n  {Fore.RED}invalid option{Style.RESET_ALL}\n")

def safe(command):
    toreplace = [';','&','|','$']
    for i in toreplace:
        command = command.replace(i, '')
    return os.system(command)
         
def monitoring():
    print(f"\n  {Fore.YELLOW}monitoring mode{Style.RESET_ALL}\n")
    print("\n  list of log files: last24h.log, err.log, auth.log\n")
    choice = input("\n  your choice: ")

    try:
        print(choice)
        safe(f"tail -f /log/{choice}")
    except FileNotFoundError:
        print(f"\n  {Fore.RED}invalid choice{Style.RESET_ALL}\n")
           
def main():
    try:

        welcome()

        restricted_commands = {
            "maintenance": True,
            "vmonitoring": True
        }

        if not products_content:
            installation_mode()
        else:
            while True:
                action = input("+> ")
                if action in restricted_commands:
                    operator_pin = input("\n  restricted command. enter operator id (uuid): ")
                    if operator_pin == "282470aa-52e9-42ca-9dc5-30d7b746ac97":
                        continue
                    else:
                        print(f"\n  {Fore.RED}incorrect uuid{Style.RESET_ALL}\n")    
                elif action.lower() == "maintenance":
                    maintenance()
                elif action.lower() == "vmonitoring":
                    monitoring()
                elif action.lower() == "buy":
                    product_index = input("\n  index of the product you want to buy: ")
                    print(f"\n  {Fore.RED}vending cart jam{Style.RESET_ALL}\n")
                elif action.lower() == "list":
                    show_products()
                elif action.lower() == "version":
                    version()
                elif action.lower() == "exit":
                    print(f"\n  {Fore.YELLOW}session closed{Style.RESET_ALL}\n")
                    os._exit(0)
                elif action.lower() == "help":
                    print(f"\n  {Fore.YELLOW}help{Style.RESET_ALL}\n")
                    print(f"  buy list maintenance exit\n")
                else:
                    print(f"\n  {Fore.RED}invalid action{Style.RESET_ALL}\n")
    except KeyboardInterrupt:
        print(f"\n  {Fore.YELLOW}exiting...{Style.RESET_ALL}")
        os._exit(0)

if __name__ == "__main__":
    main()



       
