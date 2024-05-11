import json
import os

# Funzione per rimuovere un campo specifico da un JSON        
def rimuovi_campo(json_data, campo_da_rimuovere):
    if campo_da_rimuovere in json_data:
        del json_data[campo_da_rimuovere]
    return json_data
            
if __name__ == "__main__":


    # Percorso della cartella contenente i file JSON
    cartella = "./dataset/json"

    # Campo da rimuovere
    campo_da_rimuovere = ["amenities", "bedrooms"]

    # Itera attraverso tutti i file nella cartella
    for filename in os.listdir(cartella):
        # Verifica se il file è un file JSON
        if filename.endswith('.json'):
            # Percorso completo del file JSON
            percorso_file = os.path.join(cartella, filename)
            
            # Apre il file JSON e carica i dati
            with open(percorso_file, 'r') as file:
                data = json.load(file)
            
            # Rimuove il campo specificato dal JSON
            for elem in campo_da_rimuovere:
                nuovo_data = rimuovi_campo(data, elem)
            
            # Sovrascrive il file con i nuovi dati
            with open(percorso_file, 'w') as file:
                json.dump(nuovo_data, file, indent=4)  # indent=4 per formattare il JSON in modo leggibile