# STEP 2

import csv
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def is_null(value):
    """Verifica se un valore è considerato nullo."""
    return value in ('', None) or str(value).lower() == 'nan'

def replace_nulls(dataset, column_name, replacement_value):
    """Sostituisce i valori nulli in una colonna specifica."""
    for row in dataset:
        if column_name in row and is_null(row[column_name]):
            row[column_name] = replacement_value
    return dataset

def load_csv(file_path, encoding='UTF-8'):
    """Carica un file CSV in una lista di dizionari."""
    with open(file_path, mode='r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def count_missing_values(dataset, columns=None):
    """Conta i valori mancanti in un dataset."""
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

def get_lat_long(address, city="Chicago, IL", retries=3):
    """Ottiene latitudine e longitudine per un indirizzo."""
    full_address = f"{address}, {city}"
    geolocator = Nominatim(user_agent="crash_data_geocoder/1.0 (gnsantoro01@gmail.com)")
    attempts = 0
    while attempts < retries:
        try:
            location = geolocator.geocode(full_address, timeout=20)
            return (location.latitude, location.longitude) if location else (None, None)
        except GeocoderTimedOut:
            attempts += 1
            time.sleep(2)
    print(f"Errore: impossibile ottenere coordinate per '{address}' dopo {retries} tentativi.")
    return (None, None)


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

# Esempio di utilizzo
file_path = r'C:/Users/pietro/OneDrive/Desktop/LDS/Crashes.csv'

# Carica il dataset senza modificare il file originale
dataset = load_csv(file_path)


# Sostituisci i valori nulli nella colonna 'REPORT_TYPE' con un valore predefinito
updated_dataset = replace_nulls(dataset, 'REPORT_TYPE', 'NOT ON SCENE (DESK REPORT)')


#STREET NAME
updated_dataset = replace_nulls(dataset, 'STREET_NAME', '76TH ST') 

#STREET DIRECTION, 2 ne mancano facendo un controllo incrociato con nome della strada e direzione 
for row in dataset:
    if is_null(row.get('STREET_DIRECTION')):  # Aggiorna solo se STREET_DIRECTION è mancante
        if row.get('STREET_NAME') == 'BESSIE COLEMAN DR':
            row['STREET_DIRECTION'] = 'N'
        else:
            row['STREET_DIRECTION'] = 'S'


# BEAT_OF_OCCURRENCE
'''
BEAT_OF_OCCURRENCE== 312.0 se  STREET_NAME == 63RD ST
BEAT_OF_OCCURRENCE== 712.0 se STREET_NAME == MAY ST
BEAT_OF_OCCURRENCE== 1654.0 se STREET_NAME  == BESSIE COLEMAN DR
BEAT_OF_OCCURRENCE= 1711.0 se STREET_NAME  == LINCOLL AVE
'''

# Eseguiamo la sostituzione in base alla STREET_NAME, abbiamo visto con pandas che queste strade corrispondono sempre con questi numeri di distretto
for row in dataset:
    if row['STREET_NAME'] == '63RD ST' and row['BEAT_OF_OCCURRENCE'] == '':
        updated_dataset = replace_nulls(dataset, 'BEAT_OF_OCCURRENCE', '312.0')
    elif row['STREET_NAME'] == 'MAY ST' and row['BEAT_OF_OCCURRENCE'] == '':
        updated_dataset = replace_nulls(dataset, 'BEAT_OF_OCCURRENCE', '712.0')
    elif row['STREET_NAME'] == 'BESSIE COLEMAN DR' and row['BEAT_OF_OCCURRENCE'] == '':
        updated_dataset = replace_nulls(dataset, 'BEAT_OF_OCCURRENCE', '1654.0')
    elif row['STREET_NAME'] == 'LINCOLL AVE' and row['BEAT_OF_OCCURRENCE'] == '':
        updated_dataset = replace_nulls(dataset, 'BEAT_OF_OCCURRENCE', '1711.0')


# MOST_SEVERE_INJURY
updated_dataset = replace_nulls(dataset, 'MOST_SEVERE_INJURY', 'NO INDICATION OF INJURIES')



# LAT, LONG E LOCATION
# Funzione per ottenere latitudine e longitudine
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Funzione per ottenere latitudine e longitudine
def get_lat_long(address, city="Chicago, IL"):
    full_address = f"{address}, {city}"  # Aggiungi la città all'indirizzo
    geolocator = Nominatim(user_agent="crash_data_geocoder/1.0 (gnsantoro01@gmail.com)")
    try:
        location = geolocator.geocode(full_address, timeout=20)
        return (location.latitude, location.longitude) if location else (None, None)
    except GeocoderTimedOut:
        return get_lat_long(address, city)  # Ritenta con la città

# Funzione per aggiornare tutte le coordinate mancanti
def update_missing_coordinates(updated_dataset):
    # Loop per aggiornare le righe con valori mancanti di latitudine o longitudine
    for row in updated_dataset:
        if not row.get('LATITUDE') or not row.get('LONGITUDE'):  # Controlla i valori mancanti
            lat, long = get_lat_long(row['STREET_NAME'])
            row['LATITUDE'] = lat
            row['LONGITUDE'] = long

            # Aggiungi un ritardo per evitare di superare il rate limit
            time.sleep(1)

    return updated_dataset

lat_long_geopy = update_missing_coordinates(updated_dataset)


#258 MISSING VALUE, recuero con media (sono autostrade)
from collections import defaultdict
from difflib import get_close_matches

def calculate_average_coordinates_by_similar_street(dataset, threshold=0.6):
    """
    Calcola le coordinate medie raggruppate per nomi di strada simili nel dataset.
    Due strade sono considerate "simili" se il loro nome soddisfa un certo grado di somiglianza.

    :param dataset: Lista di dizionari, dove ogni dizionario rappresenta una riga del dataset.
    :param threshold: Soglia di similarità per considerare due nomi di strada simili (0.0 - 1.0).
    :return: Dizionario con STREET_NAME come chiave e tuple (media_latitudine, media_longitudine) come valori.
    """
    street_coords = defaultdict(list)
    street_names = set(row['STREET_NAME'] for row in dataset if row.get('STREET_NAME'))

    # Raggruppa le coordinate per nomi di strada simili
    for row in dataset:
        street_name = row.get('STREET_NAME')
        latitude = row.get('LATITUDE')
        longitude = row.get('LONGITUDE')

        if street_name and latitude is not None and longitude is not None:
            try:
                latitude = float(latitude)
                longitude = float(longitude)

                # Trova il nome di strada più simile nel dataset
                similar_street = get_close_matches(street_name, street_names, n=1, cutoff=threshold)
                if similar_street:
                    # Usa il nome della strada più simile trovato
                    street_coords[similar_street[0]].append((latitude, longitude))
                else:
                    # Se non ci sono corrispondenze, usa il nome originale
                    street_coords[street_name].append((latitude, longitude))
            except (ValueError, TypeError):
                continue

    # Calcola la media delle coordinate per ogni gruppo
    average_coords = {}
    for street_name, coords in street_coords.items():
        if coords:
            avg_lat = sum(lat for lat, lon in coords) / len(coords)
            avg_lon = sum(lon for lat, lon in coords) / len(coords)
            average_coords[street_name] = (avg_lat, avg_lon)

    return average_coords


def fill_missing_coordinates_with_similarity(dataset, average_coords, threshold=0.7):
    """
    Riempie i valori mancanti di LATITUDE e LONGITUDE nel dataset usando la media
    delle coordinate calcolate per nomi di strada simili.

    :param dataset: Lista di dizionari, dove ogni dizionario rappresenta una riga del dataset.
    :param average_coords: Dizionario con STREET_NAME come chiave e tuple (media_latitudine, media_longitudine) come valori.
    :param threshold: Soglia di similarità per considerare due nomi di strada simili (0.0 - 1.0).
    :return: Dataset aggiornato con i valori mancanti riempiti.
    """
    street_names = list(average_coords.keys())
    updated_dataset = []

    for row in dataset:
        latitude = row.get('LATITUDE')
        longitude = row.get('LONGITUDE')
        street_name = row.get('STREET_NAME')

        # Se ci sono valori mancanti
        if (latitude is None or longitude is None) and street_name:
            # Trova il nome della strada più simile
            similar_street = get_close_matches(street_name, street_names, n=1, cutoff=threshold)
            if similar_street:
                avg_lat, avg_lon = average_coords[similar_street[0]]
                row['LATITUDE'] = avg_lat if latitude is None else latitude
                row['LONGITUDE'] = avg_lon if longitude is None else longitude

        updated_dataset.append(row)

    return updated_dataset


# Esempio di utilizzo
# Calcola la media delle coordinate per nomi di strada simili
average_coords = calculate_average_coordinates_by_similar_street(updated_dataset, threshold=0.7) #0.6 è valore di similarità che deve avere STREET_NAME (se metto 0.8 significhe che deve essere quasi identico)

# Riempie i valori mancanti nel dataset basandosi sulla similarità
updated_dataset = fill_missing_coordinates_with_similarity(updated_dataset, average_coords, threshold=0.7)



##ora uso BEAT_OF_OCCURENCE 
def custom_median(values):
    """Calculate the median of a list of values without using the statistics module."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 1:
        return sorted_values[n // 2]  # If odd, return middle value
    else:
        return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2.0  # If even, return average of two middle values

def calculate_medians(data):
    """Calculates medians for latitude and longitude based on a unique address."""
    coords_by_address = defaultdict(list)
    for row in data:
        if row['LATITUDE'] and row['LONGITUDE']:  # Ensure we only use rows with valid coordinates
            unique_address = f"{row['STREET_NAME']}{row['BEAT_OF_OCCURRENCE']}{row['STREET_DIRECTION']}"
            coords_by_address[unique_address].append((float(row['LATITUDE']), float(row['LONGITUDE'])))

    median_coords = {}
    for address, coords in coords_by_address.items():
        latitudes, longitudes = zip(*coords)
        median_coords[address] = (custom_median(latitudes), custom_median(longitudes))
    return median_coords

median_coords = calculate_medians(updated_dataset)



### LOCATION
for row in updated_dataset:
    if 'LATITUDE' in row and 'LONGITUDE' in row and row['LATITUDE'] and row['LONGITUDE']:
        # Format LOCATION as "POINT (LONGITUDE LATITUDE)"
        row['LOCATION'] = f"POINT ({row['LONGITUDE']} {row['LATITUDE']})"
    else:
        # If LATITUDE or LONGITUDE is missing, you can handle it here if necessary
        row['LOCATION'] = None

# Print out the modified dataset (optional)
for row in updated_dataset:
    print(row)


# MOST_SEVERE_INJURY
updated_dataset = replace_nulls(dataset, 'LATITUDE', 0.0)

# MOST_SEVERE_INJURY
updated_dataset = replace_nulls(dataset, 'LONGITUDE', 0.0)

updated_dataset = replace_nulls(dataset, 'LOCATION', "POINT (0.0, 0.0)")

# Conta i valori mancanti
missing_counts = count_missing_values(updated_dataset)




# Esempio di utilizzo
output_file_path = r'C:/Users/pietro/OneDrive/Desktop/LDS/Crashes_updated.csv'
save_csv(updated_dataset, output_file_path)




