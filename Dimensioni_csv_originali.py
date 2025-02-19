import csv
import os

# Percorsi dei file CSV di input
input_crashes_file = "D:/LDS_MODIFICATO/2_step/Crashes_updated.csv"
input_people_file = "D:/LDS_MODIFICATO/2_step/People_updated.csv"
input_vehicles_file = "D:/LDS_MODIFICATO/2_step/Vehicle_updated.csv"

# Percorso della cartella di output
output_folder = "D:/LDS_MODIFICATO/step_4/"
os.makedirs(output_folder, exist_ok=True)

# Dizionario con le colonne per ciascuna tabella del data warehouse
tables = {
    
    "Dimension_Person": ["PERSON_ID", "PERSON_TYPE", "VEHICLE_ID", "INJURY_CLASSIFICATION", 
                         "CITY", "STATE", "SEX", "AGE", "SAFETY_EQUIPMENT", 
                         "AIRBAG_DEPLOYED", "EJECTION", "DAMAGE_CATEGORY",  "DRIVER_ACTION", "DRIVER_VISION", "PHYSICAL_CONDITION", "BAC_RESULT"], 
    
    "Dimension_Vehicle": ["CRASH_UNIT_ID", "UNIT_NO", "UNIT_TYPE", "VEHICLE_ID", "MAKE", 
                          "MODEL", "LIC_PLATE_STATE", "VEHICLE_YEAR", "VEHICLE_DEFECT", 
                          "VEHICLE_TYPE", "VEHICLE_USE", "TRAVEL_DIRECTION", "MANEUVER", "OCCUPANT_CNT", 'FIRST_CONTACT_POINT'],
   
    "Dimension_Crash": [
        "RD_NO", "TRAFFICWAY_TYPE", "POSTED_SPEED_LIMIT", "FIRST_CRASH_TYPE",
        "TRAFFIC_CONTROL_DEVICE", "REPORT_TYPE", "CRASH_TYPE", 
        "BEAT_OF_OCCURRENCE", "ALIGNMENT" ],
    
}


# Funzione per filtrare e scrivere in un nuovo file CSV senza duplicati basati su una chiave primaria
def csv_no_duplicates(input_file, columns, output_file, primary_key):
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Controlla se tutte le colonne richieste sono presenti nel file
            missing_columns = [col for col in columns if col not in reader.fieldnames]
            if missing_columns:
                print(f"Attenzione: Le seguenti colonne mancano nel file {input_file}: {', '.join(missing_columns)}")
                return
            
            # Insieme per tracciare i valori già elaborati della chiave primaria
            seen_keys = set()
            filtered_data = []

            for row in reader:
                key_value = row.get(primary_key)
                if key_value is None:
                    print(f"Attenzione: Record senza valore per la chiave primaria {primary_key} saltato.")
                    continue
                if key_value in seen_keys:
                    print(f"Duplicato rilevato per {primary_key}={key_value}. Record ignorato.")
                    continue
                
                seen_keys.add(key_value)
                filtered_data.append({col: row[col] for col in columns if col in row})
        
        # Scrivi nel file di output
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(filtered_data)
        print(f"Elaborazione completata: file salvato in {output_file}")
    
    except Exception as e:
        print(f"Errore nell'elaborazione del file {input_file}: {e}")

# Elaborazione dei file con chiavi primarie specifiche
csv_no_duplicates(input_vehicles_file, tables["Dimension_Vehicle"], f"{output_folder}Dimension_Vehicle.csv", primary_key="CRASH_UNIT_ID")
csv_no_duplicates(input_crashes_file, tables["Dimension_Crash"], f"{output_folder}Dimension_Crash.csv", primary_key="RD_NO")
csv_no_duplicates(input_people_file, tables["Dimension_Person"], f"{output_folder}Dimension_Person.csv", primary_key="PERSON_ID")