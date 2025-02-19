import csv

# Percorsi dei file CSV di input
input_crashes_file = "D:/LDS_MODIFICATO/2_step/Crashes_updated.csv"

def create_dimension_from_multiple_sources(input_files, columns, output_file, dimension_id_name):
    """
    Crea una dimensione univoca combinando dati da più file sorgente.

    Args:
        input_files (list): Lista di file CSV di input.
        columns (list): Colonne da includere nella dimensione.
        output_file (str): Percorso del file CSV di output.
        dimension_id_name (str): Nome della colonna ID univoco della dimensione.
    """
    unique_rows = {}  # Dizionario per garantire unicità delle combinazioni di attributi
    dimension_table = []  # Lista per memorizzare la tabella finale
    dimension_id = 1  # Contatore per l'ID univoco della dimensione

    for input_file in input_files:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Verificare che tutte le colonne necessarie siano presenti
            missing_cols = [col for col in columns if col not in reader.fieldnames]
            if missing_cols:
                print(f"Avviso: Le seguenti colonne non sono presenti in {input_file}: {missing_cols}")
                continue  # Salta il file corrente se mancano colonne

            for row in reader:
                # Creare una chiave unica per la combinazione degli attributi
                row_key = tuple(row[col] for col in columns if col in row)
                if row_key not in unique_rows:
                    unique_rows[row_key] = dimension_id
                    dimension_table.append(
                        {dimension_id_name: dimension_id, **{col: row[col] for col in columns if col in row}}
                    )
                    dimension_id += 1

    # Scrivere i dati univoci in un nuovo file CSV
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=[dimension_id_name] + columns)
        writer.writeheader()
        writer.writerows(dimension_table)

    print(f"Tabella {dimension_id_name} creata e salvata in '{output_file}'.")


# WEATHER
create_dimension_from_multiple_sources(
    input_files=[input_crashes_file],
    columns=['WEATHER_CONDITION', 'LIGHTING_CONDITION'],
    output_file='D:/LDS_MODIFICATO/step_4/Dimension_Weather.csv',
    dimension_id_name='WEATHER_ID'
)

# CAUSE
create_dimension_from_multiple_sources(
    input_files=[input_crashes_file],
    columns=[
        'PRIM_CONTRIBUTORY_CAUSE', 
        'SEC_CONTRIBUTORY_CAUSE',
        'DEVICE_CONDITION',
        'ROAD_DEFECT',
        'ROADWAY_SURFACE_COND'
    ],
    output_file='D:/LDS_MODIFICATO/step_4/Dimension_Cause.csv',
    dimension_id_name='CAUSE_ID'
)

# GEOGRAPHY
create_dimension_from_multiple_sources(
    input_files=[input_crashes_file],
    columns=[
        'STREET_NO',
        'STREET_DIRECTION',
        'STREET_NAME',
        'LATITUDE',
        'LONGITUDE',
        'LOCATION'
    ],
    output_file='D:/LDS_MODIFICATO/step_4/Dimension_Geography.csv',
    dimension_id_name='GEOGRAPHY_ID'
)

# INJURY
create_dimension_from_multiple_sources(
    input_files=[input_crashes_file],
    columns=[
        'INJURIES_FATAL',
        'INJURIES_INCAPACITATING',
        'INJURIES_NON_INCAPACITATING',
        'INJURIES_REPORTED_NOT_EVIDENT',
        'INJURIES_NO_INDICATION',
        'INJURIES_UNKNOWN',
        'MOST_SEVERE_INJURY',
        'INJURIES_TOTAL'
    ],
    output_file='D:/LDS_MODIFICATO/step_4/Dimension_Injury.csv',
    dimension_id_name='INJURIES_ID'
)


#DATE
create_dimension_from_multiple_sources(
    input_files=[input_crashes_file],
    columns=[
            "CRASH_DATE", "CRASH_DAY_OF_WEEK", "CRASH_HOUR", "CRASH_MONTH", "DATE_POLICE_NOTIFIED"
    ],
    output_file='D:/LDS_MODIFICATO/step_4/Dimension_Date.csv',
    dimension_id_name='DATE_ID'
)



from datetime import datetime

def add_crash_year_and_quarter(input_file, output_file):
    """
    Aggiunge le colonne CRASH_YEAR e QUARTER basandosi su CRASH_DATE senza modificare le altre colonne.
    """
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = reader.fieldnames + ['CRASH_YEAR', 'QUARTER']
        
        for row in rows:
            try:
                # Converti CRASH_DATE in formato datetime
                crash_date = datetime.strptime(row['CRASH_DATE'], "%m/%d/%Y %I:%M:%S %p")
                row['CRASH_YEAR'] = crash_date.year
                row['QUARTER'] = (crash_date.month - 1) // 4 + 1
            except ValueError:
                # Gestisci errori di parsing del formato data
                row['CRASH_YEAR'] = 0
                row['QUARTER'] = 0

    # Scrivi il dataset aggiornato con le nuove colonne
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Colonne CRASH_YEAR e QUARTER aggiunte e salvate in '{output_file}'.")

# File di input e output
input_file = "D:/LDS_MODIFICATO/step_4/Dimension_Date.csv"
output_file = "D:/LDS_MODIFICATO/step_4/Dimension_Date.csv"

# Aggiungi le colonne CRASH_YEAR e QUARTER
add_crash_year_and_quarter(input_file, output_file)
