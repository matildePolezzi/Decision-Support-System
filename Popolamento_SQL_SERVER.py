import csv
import pyodbc
from tqdm import tqdm

def execute_many(cursor, query, data):
    cursor.executemany(query, data)

def populate_table_from_csv_batch(cursor, table_name, file_path, batch_size):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header
        rows = [tuple(row) for row in csv_reader]

    with tqdm(total=len(rows), desc=f'Inserting into {table_name} table') as pbar:
        try:
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                num_columns = len(batch[0])
                placeholders = ', '.join(['?'] * num_columns)
                execute_many(cursor, f'INSERT INTO {table_name} VALUES ({placeholders})', batch)
                pbar.update(len(batch))
        except pyodbc.Error as e:
            print(f"Error: {e}")
        finally:
            conn.commit()


if __name__ == '__main__':
    
    # Connection data
    server = 'tcp:lds.di.unipi.it'
    database = 'Group_ID_21_DB'
    username = 'Group_ID_21'
    password = '6RSW5VK4'

    # Connection string
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    try:
        # Delete all data from the tables
        cursor.execute('DELETE FROM Damage_to_users')
        #cursor.execute('DELETE FROM Dimension_Crash')
        #cursor.execute('DELETE FROM Dimension_Person')
        #cursor.execute('DELETE FROM Dimension_Vehicle')
        #cursor.execute('DELETE FROM Dimension_Date')
        #cursor.execute('DELETE FROM Dimension_Cause')
        #cursor.execute('DELETE FROM Dimension_Geography')
        #cursor.execute('DELETE FROM Dimension_Injuries')
        #cursor.execute('DELETE FROM Dimension_Weather')

        # Populate all tables using batch inserts
        #populate_table_from_csv_batch(cursor, 'Dimension_Crash', r'D:/1_LDS/step_4/Dimension_Crash.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Person', r'D:/1_LDS/step_4/Dimension_Person.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Vehicle', r'D:/1_LDS/step_4/Dimension_Vehicle.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Date', r'D:/1_LDS/step_4/Dimension_Date.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Cause', r'D:/1_LDS/step_4/Dimension_Cause.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Geography', r'D:/1_LDS/step_4/Dimension_Geography.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Injuries', r'D:/1_LDS/step_4/Dimension_Injury.csv', batch_size=10000)
        #populate_table_from_csv_batch(cursor, 'Dimension_Weather', r'D:/1_LDS/step_4/Dimension_Weather.csv', batch_size=10000)
        populate_table_from_csv_batch(cursor, 'Damage_to_users', r'D:/1_LDS/Damage_to_users.csv', batch_size=10000)

        # Commit once after all batches are processed
        conn.commit()

    except pyodbc.Error as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()
