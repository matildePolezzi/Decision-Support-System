import csv

def replace_nulls(dataset, column_name, replacement_value):
    """Sostituisce i valori nulli in una colonna specifica."""
    for row in dataset:
        if column_name in row and is_null(row[column_name]):
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
people_file = r'D:/1_LDS/People.csv'
crashes_file = r'D:/1_LDS//Crashes.csv'  

# copia dataset per lavorare in locale
new_df = load_csv(people_file)



# VEHICLE_ID, Lasciamo missing valuesperchè sono solo passenger e bicilette.
replace_nulls(new_df, 'VEHICLE_ID', 0.0)


# CITY
replace_nulls(new_df, 'CITY', 'UNKNOWN')

# STATE
new_df = replace_nulls(new_df, 'STATE', 'XX')


### SEX
replace_nulls(new_df, 'SEX', 'U')



#AGE
for row in new_df:
    try:
        age = float(row['AGE']) if row['AGE'].replace('.', '', 1).isdigit() else None
        driver = row.get('PERSON_TYPE') 
        if age is not None and age < 14 and age > 0.0 and driver == 'DRIVER':
            row['AGE'] = 0.0  
    except ValueError:
        # Se 'AGE' non è un numero valido, ignora quella riga
        continue

## SAFETY_EQUIPMENT
replace_nulls(new_df, 'SAFETY_EQUIPMENT', "USAGE UNKNOWN" )


# AIRBAG_DEPLOY
for row in new_df:
    person_type = row.get('PERSON_TYPE', '').upper()  # Ottieni 'PERSON_TYPE' da new_df

for row in new_df:
    # Verifica il valore di 'PERSON_TYPE' per assegnare 'AIRBAG_DEPLOYED'
    if person_type in ['BICYCLE', 'NON-MOTOR VEHICLE', 'PEDESTRIAN']:
        row['AIRBAG_DEPLOYED'] = 'NOT APPLICABLE'
    elif person_type == 'NON-CONTACT VEHICLE':
        row['AIRBAG_DEPLOYED'] = 'DID NOT DEPLOY'
    elif person_type in ['DRIVER', 'PASSENGER']:
        row['AIRBAG_DEPLOYED'] = 'DEPLOYMENT UNKNOWN'



# EJECTION
for row in new_df:
    # Se 'EJECTION' è vuoto
    if row['EJECTION'] == '':
        if row['PERSON_TYPE'] in ['PEDESTRIAN', 'BICYCLE', 'NON-MOTOR VEHICLE']:
            row['EJECTION'] = ''  
        else:
            row['EJECTION'] = 'UNKNOWN'  
            
        
# INJURY_CLASSIFICATION
replace_nulls(new_df, 'INJURY_CLASSIFICATION', "NO INDICATION OF INJURY" )
        


# DRIVEN VISION
def update_driver_vision(dataset, crashes_file, weather_default_mapping, vision_mapping):
    """
    Aggiorna la colonna DRIVER_VISION in base alle informazioni dei crash.
    """
    crash_info = {}
    
    # Carica le informazioni sui crash
    with open(crashes_file, mode='r', newline='', encoding='utf-8') as crashes_csv:
        reader = csv.DictReader(crashes_csv)
        for row in reader:
            rd_no = row['RD_NO']
            weather = row.get('WEATHER_CONDITION')
            lighting_condition = row.get('LIGHTING_CONDITION')

            # Se WEATHER_CONDITION è mancante, riempilo in base a LIGHTING_CONDITION
            if not weather and lighting_condition:
                weather = weather_default_mapping.get(lighting_condition, 'UNKNOWN')

            # Salva solo se LIGHTING_CONDITION è presente
            if lighting_condition:
                crash_info[rd_no] = (weather, lighting_condition)

    # Aggiorna DRIVER_VISION in base alle informazioni dei crash
    for row in dataset:
        if row['DRIVER_VISION'] == '' or row['DRIVER_VISION'] is None:
            rd_no = row['RD_NO']
            if rd_no in crash_info:
                weather, lighting = crash_info[rd_no]
                row['DRIVER_VISION'] = vision_mapping.get((weather, lighting), 'UNKNOWN')

    return dataset

# Dizionario per mappare combinazioni di WEATHER e LIGHTING_CONDITION a DRIVER_VISION
vision_mapping = {
    ('Clear', 'Daylight'): 'Unobstructed',
    ('Rain', 'Darkness'): 'Obstructed',
    ('Fog', 'Dawn'): 'Limited',
}

# Mappatura di default per WEATHER_CONDITION basata su LIGHTING_CONDITION
weather_default_mapping = {
    'DARKNESS': 'Overcast',
    'DARKNESS, LIGHTED ROAD': 'Overcast',
    'DAWN': 'Clear',
    'DAYLIGHT': 'Clear',
    'DUSK': 'Clear',
    'UNKNOWN': 'Unknown'
}

new_df = update_driver_vision(new_df, crashes_file, weather_default_mapping, vision_mapping)



# DAMAGE
for row in new_df:
    if row['DAMAGE_CATEGORY'] == '$500 OR LESS' and (row['DAMAGE'] == '' or row['DAMAGE'] is None):  # Se DAMAGE è mancante
        row['DAMAGE'] = 500  


#DRIVER_ACTION
replace_nulls(new_df, 'DRIVER_ACTION', 'UNKNOWN')


#PHYSICAL_CONDITION
replace_nulls(new_df, 'PHYSICAL_CONDITION', 'UNKNOWN')


### BAC_RESULT, I valori nulli sono tutti passenger quindi lasciamo NaN

# Conteggio missing values
missing_counts = count_missing_values(new_df)


def remove_duplicates_by_damage(dataset, id_column, damage_column):
    """
    Rimuove duplicati basati sull'id_column, mantenendo i record con damage_column massimo.
    """
    unique_records = {}
    
    for row in dataset:
        person_id = row[id_column]
        damage = float(row.get(damage_column, 0))
        
        if person_id not in unique_records or damage > float(unique_records[person_id].get(damage_column, 0)):
            unique_records[person_id] = row
    
    return list(unique_records.values())

# Rimuovere duplicati dal dataset
new_df = remove_duplicates_by_damage(new_df, 'PERSON_ID', 'DAMAGE')

# Salva il dataset aggiornato
updated_file_path = r'D:/LDS_MODIFICATO/2_step/People_updated.csv'
save_csv(new_df, updated_file_path)

print(f"Dataset aggiornato e salvato in: {updated_file_path}")


