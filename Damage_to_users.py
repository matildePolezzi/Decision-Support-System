import csv

# Passo 1: Aprire il file Person_updates e copiare RD_NO e PERSON_ID
with open("D:/LDS_MODIFICATO/2_step/People_updated.csv", mode='r') as person_file:
    csv_reader = csv.DictReader(person_file)
    fact_table_data = [{'RD_NO': row['RD_NO'], 'PERSON_ID': row['PERSON_ID'], 'CRASH_UNIT_ID': '', 'DATE_ID': ''} for row in csv_reader]

# Passo 2: Creare una mappa RD_NO -> CRASH_UNIT_ID da Vehicle_updated
with open('D:/LDS_MODIFICATO/2_step/Vehicle_updated.csv', mode='r') as vehicle_file:
    vehicle_reader = csv.DictReader(vehicle_file)
    crash_unit_map = {row['RD_NO']: row['CRASH_UNIT_ID'] for row in vehicle_reader}

# Passo 3: Creare una mappa RD_NO -> CRASH_DATE da Crashes_updated
with open('D:/LDS_MODIFICATO/2_step/Crashes_updated.csv', mode='r') as crashes_file:
    crashes_reader = csv.DictReader(crashes_file)
    rd_no_to_crash_date = {row['RD_NO']: row['CRASH_DATE'] for row in crashes_reader}

# Passo 4: Creare una mappa CRASH_DATE -> Date_ID da Dimension_Date
with open('D:/LDS_MODIFICATO/step_4/Dimension_Date.csv', mode='r') as dimension_date_file:
    dimension_reader = csv.DictReader(dimension_date_file)
    crash_date_to_date_id = {row['CRASH_DATE']: row['DATE_ID'] for row in dimension_reader}

# Aggiornare fact_table_data con CRASH_UNIT_ID e Date_ID
for row in fact_table_data:
    rd_no = row['RD_NO']
    
    # Aggiornare CRASH_UNIT_ID
    if rd_no in crash_unit_map:
        row['CRASH_UNIT_ID'] = crash_unit_map[rd_no]
    
    # Aggiornare Date_ID
    if rd_no in rd_no_to_crash_date:
        crash_date = rd_no_to_crash_date[rd_no]
        if crash_date in crash_date_to_date_id:
            row['DATE_ID'] = crash_date_to_date_id[crash_date]

# Scrivere i dati aggiornati nella fact_table
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='w', newline='') as fact_table_file:
    fieldnames = ['RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID']
    csv_writer = csv.DictWriter(fact_table_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table_data)
    
    

###################################################################################################
#CAUSE

# Creare una mappa RD_NO -> Cause attributi da Crashes_updated
with open('D:/LDS_MODIFICATO/2_step/Crashes_updated.csv', mode='r') as crashes_file:
    crashes_reader = csv.DictReader(crashes_file)
    rd_no_to_cause_attributes = {
        row['RD_NO']: (
            row['PRIM_CONTRIBUTORY_CAUSE'],
            row['SEC_CONTRIBUTORY_CAUSE'],
            row['DEVICE_CONDITION'],
            row['ROAD_DEFECT'],
            row['ROADWAY_SURFACE_COND']
        )
        for row in crashes_reader
    }

# Passo 2: Creare una mappa Cause attributi -> Cause_ID da Dimension_Cause
with open('D:/LDS_MODIFICATO/step_4/Dimension_Cause.csv', mode='r') as dimension_cause_file:
    dimension_reader = csv.DictReader(dimension_cause_file)
    cause_to_cause_id = {
        (
            row['PRIM_CONTRIBUTORY_CAUSE'],
            row['SEC_CONTRIBUTORY_CAUSE'],
            row['DEVICE_CONDITION'],
            row['ROAD_DEFECT'],
            row['ROADWAY_SURFACE_COND']
        ): row['CAUSE_ID']
        for row in dimension_reader
    }

# Passo 3: Leggere la fact table per aggiornare Cause_ID
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='r') as fact_table_file:
    fact_table_reader = csv.DictReader(fact_table_file)
    fact_table_rows = list(fact_table_reader)  # Copiare i dati per modificarli successivamente

# Aggiornare la fact table con Cause_ID
for row in fact_table_rows:
    rd_no = row['RD_NO']
    if rd_no in rd_no_to_cause_attributes:
        cause_attributes = rd_no_to_cause_attributes[rd_no]
        if cause_attributes in cause_to_cause_id:
            row['CAUSE_ID'] = cause_to_cause_id[cause_attributes]

# Scrivere la fact table aggiornata
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='w', newline='') as fact_table_file:
    fieldnames = ['RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID', 'CAUSE_ID']
    csv_writer = csv.DictWriter(fact_table_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table_rows)
    
 
    
######################################################################################
# GEOGRAPHY

# Passo 1: Creare una mappa RD_NO -> LOCATION da Crashes_updated
with open('D:/LDS_MODIFICATO/2_step/Crashes_updated.csv', mode='r') as crashes_file:
    crashes_reader = csv.DictReader(crashes_file)
    rd_no_to_location = {row['RD_NO']: row['LOCATION'] for row in crashes_reader}

# Passo 2: Creare una mappa LOCATION -> Geography_ID da Geography_Cause
with open('D:/LDS_MODIFICATO/step_4/Dimension_Geography.csv', mode='r') as geography_file:
    geography_reader = csv.DictReader(geography_file)
    location_to_geography_id = {row['LOCATION']: row['GEOGRAPHY_ID'] for row in geography_reader}

# Passo 3: Leggere la fact_table per aggiornare Geography_ID
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='r') as fact_table_file:
    fact_table_reader = csv.DictReader(fact_table_file)
    fact_table_rows = list(fact_table_reader)  # Copiare i dati per modificarli successivamente

# Aggiornare la fact table con Geography_ID
for row in fact_table_rows:
    rd_no = row['RD_NO']
    if rd_no in rd_no_to_location:
        location = rd_no_to_location[rd_no]
        if location in location_to_geography_id:
            row['GEOGRAPHY_ID'] = location_to_geography_id[location]

# Riscrivere la fact table con Geography_ID aggiornato
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='w', newline='') as fact_table_file:
    fieldnames = ['RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID', 'CAUSE_ID', 'GEOGRAPHY_ID']
    csv_writer = csv.DictWriter(fact_table_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table_rows)


##############################################################################################################à
# INJURY

# Passo 1: Creare una mappa RD_NO -> INJURIES_* da Crashes_updated
with open('D:/LDS_MODIFICATO/2_step/Crashes_updated.csv', mode='r') as crashes_file:
    crashes_reader = csv.DictReader(crashes_file)
    rd_no_to_injury_data = {
        row['RD_NO']: {
            'INJURIES_FATAL': row['INJURIES_FATAL'],
            'INJURIES_INCAPACITATING': row['INJURIES_INCAPACITATING'],
            'INJURIES_NON_INCAPACITATING': row['INJURIES_NON_INCAPACITATING'],
            'INJURIES_REPORTED_NOT_EVIDENT': row['INJURIES_REPORTED_NOT_EVIDENT'],
            'INJURIES_NO_INDICATION': row['INJURIES_NO_INDICATION'],
            'INJURIES_UNKNOWN': row['INJURIES_UNKNOWN'],
            'MOST_SEVERE_INJURY': row['MOST_SEVERE_INJURY']
        }
        for row in crashes_reader
    }

# Passo 2: Creare una mappa INJURIES_* -> INJURIES_ID da Dimension_Injury
with open('D:/LDS_MODIFICATO/step_4/Dimension_Injury.csv', mode='r') as dimension_injury_file:
    dimension_reader = csv.DictReader(dimension_injury_file)
    injury_data_to_injury_id = {
        (
            row['INJURIES_FATAL'],
            row['INJURIES_INCAPACITATING'],
            row['INJURIES_NON_INCAPACITATING'],
            row['INJURIES_REPORTED_NOT_EVIDENT'],
            row['INJURIES_NO_INDICATION'],
            row['INJURIES_UNKNOWN'],
            row['MOST_SEVERE_INJURY']
        ): row['INJURIES_ID']
        for row in dimension_reader
    }

# Passo 3: Leggere la fact table e aggiungere INJURIES_ID corrispondente
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='r') as fact_table_file:
    fact_table_reader = csv.DictReader(fact_table_file)
    fact_table_rows = list(fact_table_reader)  # Copiare i dati per modificarli successivamente

# Aggiornare la fact table con INJURY_ID
for row in fact_table_rows:
    rd_no = row['RD_NO']
    if rd_no in rd_no_to_injury_data:
        injury_data = rd_no_to_injury_data[rd_no]
        injury_data_tuple = (
            injury_data['INJURIES_FATAL'],
            injury_data['INJURIES_INCAPACITATING'],
            injury_data['INJURIES_NON_INCAPACITATING'],
            injury_data['INJURIES_REPORTED_NOT_EVIDENT'],
            injury_data['INJURIES_NO_INDICATION'],
            injury_data['INJURIES_UNKNOWN'],
            injury_data['MOST_SEVERE_INJURY']
        )
        if injury_data_tuple in injury_data_to_injury_id:
            row['INJURIES_ID'] = injury_data_to_injury_id[injury_data_tuple]

# Scrivere i dati aggiornati nella fact_table
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='w', newline='') as fact_table_file:
    fieldnames = ['RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID', 'CAUSE_ID', 'GEOGRAPHY_ID','INJURIES_ID']
    csv_writer = csv.DictWriter(fact_table_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table_rows)

#########################################################################################
# WEATHER

# Passo 1: Creare una mappa RD_NO -> ('WEATHER_CONDITION', 'LIGHTING_CONDITION') da Crashes_updated
with open('D:/LDS_MODIFICATO/2_step/Crashes_updated.csv', mode='r') as crashes_file:
    crashes_reader = csv.DictReader(crashes_file)
    rd_no_to_conditions = {
        row['RD_NO']: (row['WEATHER_CONDITION'], row['LIGHTING_CONDITION']) for row in crashes_reader
    }

# Passo 2: Creare una mappa ('WEATHER_CONDITION', 'LIGHTING_CONDITION') -> WEATHER_ID da Dimension_Weather
with open('D:/LDS_MODIFICATO/step_4/Dimension_Weather.csv', mode='r') as dimension_weather_file:
    dimension_reader = csv.DictReader(dimension_weather_file)
    conditions_to_weather_id = {
        (row['WEATHER_CONDITION'], row['LIGHTING_CONDITION']): row['WEATHER_ID'] for row in dimension_reader
    }

# Passo 3: Leggere la fact table e aggiungere WEATHER_ID corrispondente
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='r') as fact_table_file:
    fact_table_reader = csv.DictReader(fact_table_file)
    fact_table_rows = list(fact_table_reader)  # Copiare i dati per modificarli successivamente

# Aggiornare la fact table con WEATHER_ID
for row in fact_table_rows:
    rd_no = row['RD_NO']
    if rd_no in rd_no_to_conditions:
        conditions = rd_no_to_conditions[rd_no]
        if conditions in conditions_to_weather_id:
            row['WEATHER_ID'] = conditions_to_weather_id[conditions]

# Scrivere la fact table aggiornata con WEATHER_ID
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='w', newline='') as fact_table_file:
    fieldnames = ['RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID', 'CAUSE_ID', 'GEOGRAPHY_ID','INJURIES_ID', 'WEATHER_ID']
    csv_writer = csv.DictWriter(fact_table_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table_rows)



###########################################################################################

# Passo 1: Creare una mappa 'RD_NO' & 'PERSON_ID' -> ('DAMAGE') da People_updated
with open('D:/LDS_MODIFICATO/2_step/People_updated.csv', mode='r') as people_file:
    people_reader = csv.DictReader(people_file)
    rd_no_person_to_damage = {
        (row['RD_NO'], row['PERSON_ID']): row['DAMAGE'] for row in people_reader
    }

# Passo 1: Creare una mappa 'RD_NO' -> ('NUM_UNITS') da Crashes_updated
with open('D:/LDS_MODIFICATO/2_step/Crashes_updated.csv', mode='r') as crashes_file:
    crashes_reader = csv.DictReader(crashes_file)
    rd_no_to_num_units = {
        row['RD_NO']: row['NUM_UNITS'] for row in crashes_reader
    }


# Passo 3: Leggere la fact table e aggiungere le colonne richieste
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='r') as fact_table_file:
    fact_table_reader = csv.DictReader(fact_table_file)
    fact_table_rows = list(fact_table_reader)  # Copiare i dati per modificarli successivamente

# Aggiungere le nuove colonne
for row in fact_table_rows:
    rd_no = row['RD_NO']
    person_id = row['PERSON_ID']
    
    # Aggiungi 'DAMAGE'
    row['DAMAGE'] = rd_no_person_to_damage.get((rd_no, person_id), None)
    
    # Aggiungi 'NUM_UNITS'
    row['NUM_UNITS'] = rd_no_to_num_units.get(rd_no, None)
    

# Scrivere la fact table aggiornata con le nuove colonne
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='w', newline='') as fact_table_file:
    fieldnames = ['RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID', 'CAUSE_ID', 'GEOGRAPHY_ID','INJURIES_ID', 'WEATHER_ID', 'DAMAGE', 'NUM_UNITS']
    csv_writer = csv.DictWriter(fact_table_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table_rows)

    
################################################################################################
# CREO DAMAGE_TO_USER CON SWAP COLONNE

# Leggere la fact table esistente
import csv

# Leggere la fact table esistente
with open('D:/LDS_MODIFICATO/step_4/fact_table.csv', mode='r') as fact_table_file:
    fact_table_reader = csv.DictReader(fact_table_file)
    fact_table_rows = list(fact_table_reader)  # Copiare i dati esistenti

# Definire il nuovo ordine dei campi
new_field_order = ['Damage_to_users_ID','DAMAGE', 'NUM_UNITS', 'RD_NO', 'PERSON_ID', 'CRASH_UNIT_ID', 'DATE_ID', 'CAUSE_ID', 'GEOGRAPHY_ID', 'INJURIES_ID', 'WEATHER_ID']

# Aggiungere un ID sequenziale
for index, row in enumerate(fact_table_rows, start=1):
    row['Damage_to_users_ID'] = index

# Scrivere il file Damage_to_users.csv con l'ID sequenziale
with open('D:/LDS_MODIFICATO/step_4/Damage_to_users.csv', mode='w', newline='') as damage_to_users_file:
    csv_writer = csv.DictWriter(damage_to_users_file, fieldnames=new_field_order)
    csv_writer.writeheader()
    for row in fact_table_rows:
        # Riordinare i dati per seguire il nuovo ordine
        ordered_row = {field: row.get(field, '') for field in new_field_order}
        csv_writer.writerow(ordered_row)
