import os
import uuid

# Cartella in cui verranno creati i file
folder_path = "../requests"

# Creazione della cartella se non esiste già
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Numero totale di file da creare
num_files = 50

# Frase da inserire all'interno dei file
phrase = "\n\nHey there! \n\nLooks like you're trying to access some top-secret data.\n\nThe funny thing is, all the administrators (our dear Dave included) have been gone for ages! So, it seems like you're an intruder.\n\nInitiating threat removal procedure... Please wait and stand still!\n\nhttps://ctfdemo.interlogica.ninja/video/security-countermeasures-activated/\n\n"

# Creazione dei file
for i in range(num_files):
    # Genera un UUID univoco come nome del file
    file_name = os.path.join(folder_path, str(uuid.uuid4()))
    with open(file_name, "w") as file:
        # Scrive la frase all'interno del file
        file.write(phrase)

print(f"{num_files} files have been successfully created in the {folder_path} folder.")
