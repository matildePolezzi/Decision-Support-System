#STEP 2

import csv

def replace_nulls(dataset, column_name, replacement_value, condition_fn=None):
    """
    Sostituisce i valori nulli in una colonna specifica di un dataset rappresentato come un dizionario,
    """
    for row in dataset:
        # Verifica se il valore è mancante e la condizione (se fornita) è soddisfatta
        if (row[column_name] == '' or row[column_name] is None or str(row[column_name]).lower() == 'nan') and \
           (condition_fn is None or condition_fn(row)):
            row[column_name] = replacement_value
    return dataset



def load_csv(file_path, encoding='UTF-8'):
    """
    Carica un file CSV in una lista di dizionari.
    """
    with open(file_path, mode='r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def is_null(value):
    """Verifica se un valore è considerato nullo."""
    return value in ('', None) or str(value).lower() == 'nan'

def count_missing_values(dataset, columns=None):
    """
    Conta i valori mancanti in un dataset per ciascuna colonna specificata.
    """
    if not columns:
        columns = dataset[0].keys()
    missing_counts = {column: 0 for column in columns}
    for row in dataset:
        for column in columns:
            if is_null(row.get(column)):
                missing_counts[column] += 1

    for column, count in missing_counts.items():
        print(f"Colonna '{column}' - Valori mancanti: {count}")
    return missing_counts

def save_csv(dataset, file_path, encoding='UTF-8'):
    """Salva un dataset (lista di dizionari) in un file CSV."""
    if not dataset:
        print("Il dataset è vuoto. Nulla da salvare.")
        return
    
    # Estrai le colonne dai dizionari del dataset
    fieldnames = dataset[0].keys()
    
    with open(file_path, mode='w', encoding=encoding, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Scrivi l'intestazione
        writer.writeheader()
        
        # Scrivi le righe
        writer.writerows(dataset)
    
    print(f"Dataset salvato correttamente in {file_path}")


# Percorsi dei file
vehicle_file = r'C:/Users/pietro/OneDrive/Desktop/LDS/Vehicles.csv' 


# Carica il dataset senza modificare il file originale
new_df = load_csv(vehicle_file)

# UNIT_TYPE, l'abbiamo controllato per RD_NO
new_df = [row for row in new_df if row['UNIT_TYPE'] != '']
#dataset

#VEICHLE_ID
for row in new_df:
    if is_null(row['VEHICLE_ID']) and row['UNIT_TYPE'] == 'DRIVER':
        row['VEHICLE_ID'] = 0.0


# Condizione per 'UNIT_TYPE' uguale a 'DRIVER', correggiamo solo i veicoli i non veicoli non ci interessano
is_driver = lambda row: row.get('UNIT_TYPE') == 'DRIVER'

new_df = replace_nulls(new_df, 'MAKE', 'UNKNOWN', condition_fn=is_driver)

new_df = replace_nulls(new_df, 'MODEL', 'UNKNOWN', condition_fn=is_driver)

new_df = replace_nulls(new_df, 'VEHICLE_DEFECT', 'UNKNOWN', condition_fn=is_driver)

new_df = replace_nulls(new_df, 'VEHICLE_TYPE', 'UNKNOWN / Na', condition_fn=is_driver)

new_df = replace_nulls(new_df, 'VEHICLE_USE', 'UNKNOWN', condition_fn=is_driver)

new_df = replace_nulls(new_df, 'LIC_PLATE_STATE', 'XX', condition_fn=is_driver) #XX non è codice stato ma è un 'UNKNOWN'


#VEHICLE_YEAR, lasciamo vuoto 
# eistono VEHICLE_YEAR > 2019, macchine del 1900 ma con modelli che non esistevano ancora 
# abbiamo controllato e per non veicoli giustamente il valore è vuoto
# abbiamo valori nulli solo per DRIVERLESS / pedestrian / PARKED e non correggiamo
new_df = replace_nulls(new_df, 'VEHICLE_YEAR', 0.0, condition_fn=is_driver)


# TRAVEL_DIRECTION
new_df = replace_nulls(new_df, 'TRAVEL_DIRECTION', 'UNKNOWN') #possiamo recuperare con merge in Crashes?



# MANEUVER 
new_df = replace_nulls(new_df,'MANEUVER', 'UNKNOWN / NA', condition_fn=is_driver)

# OCCUPANT_CNT, lasciamo vuoto per non condizionare le query

# FIRST_CONTACT_POINT
# creo associazione con valori RD_NO a FIRST_CONTACT_POINT
contact_point_map = {
    'JB376407': 'REAR',
    'JB374941': 'SIDE_RIGHT',
    'JB374667': 'UNKNOWN',
    'JB374571': 'FRONT',
    'JB374559': 'UNKNOWN',
}

# Iterazione sulle righe del dataset per aggiornare FIRST_CONTACT_POINT
for row in new_df:
    rd_no = row.get('RD_NO')
    if rd_no in contact_point_map:
        row['FIRST_CONTACT_POINT'] = contact_point_map[rd_no]



# Conta i valori mancanti
missing_counts = count_missing_values(new_df)
        

# Esempio di utilizzo
output_file_path = r'C:/Users/pietro/OneDrive/Desktop/LDS/Vehicle_updated.csv'
save_csv(new_df, output_file_path)