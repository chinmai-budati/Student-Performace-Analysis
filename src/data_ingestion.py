import pandas as pd
import os
from sqlalchemy import create_engine, text

DB_USER = 'root'
DB_PASSWORD = 'Me_chinmai%4004' 
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'student_analytics_db'

engine_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(engine_url)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            current_db = result.scalar()
            print(f"Success! Connected to MySQL database: {current_db}")
    except Exception as e:
        print(f"Connection failed. Error: {e}")

DATA_DIR = r'C:\Users\chinm\OneDrive\Desktop\Student_Performance_Analysis\data' 

def load_parent_tables():
    print("\n--- Initiating Phase 2: Loading Parent Tables ---")
    
    parent_tables = {
        'courses.csv': 'courses',
        'studentInfo.csv': 'students',
        'assessments.csv': 'assessments',
        'vle.csv': 'vle_materials'
    }
    
    for csv_file, table_name in parent_tables.items():
        file_path = os.path.join(DATA_DIR, csv_file)
        
        try:
            print(f"Reading {csv_file}...")
            df = pd.read_csv(file_path)

            if csv_file == 'studentInfo.csv':  
                df = df.drop(columns=['code_module', 'code_presentation'])

            df = df.drop_duplicates(subset=['id_student'])
            
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            
            print(f"Successfully loaded {len(df)} rows into '{table_name}'!")
            
        except FileNotFoundError:
            print(f"Could not find {csv_file} in {DATA_DIR}. Check your folder path!")
        except Exception as e:
            print(f"Failed to load {csv_file}. Error: {e}")

def load_child_tables():
    print("\n--- Initiating Phase 3: Loading Child Tables ---")
    
    child_tables = {
        'studentRegistration.csv': 'registrations',
        'studentAssessment.csv': 'student_results'
    }
    
    for csv_file, table_name in child_tables.items():
        file_path = os.path.join(DATA_DIR, csv_file)
        
        try:
            print(f"Reading {csv_file}...")
            df = pd.read_csv(file_path)
            
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            
            print(f"Successfully loaded {len(df)} rows into '{table_name}'!")
            
        except FileNotFoundError:
            print(f"Could not find {csv_file} in {DATA_DIR}. Check your folder path!")
        except Exception as e:
            print(f"Failed to load {csv_file}. Error: {e}")

def load_clicks_table():
    print("\n--- Initiating Phase 4: The Behemoth (Student Clicks) ---")
    
    file_path = os.path.join(DATA_DIR, 'studentVle.csv')
    table_name = 'student_clicks'
    chunk_size = 100000  # Process 100,000 rows at a time
    
    try:
        print(f"Reading studentVle.csv in chunks of {chunk_size}...")
        total_rows = 0
        
        # This loop automatically breaks the massive CSV into manageable pieces
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            total_rows += len(chunk)
            print(f"⏳ Loaded {total_rows:,} rows so far...")
            
        print(f"SUCCESS! All {total_rows:,} clicks loaded into '{table_name}'!")
        
    except FileNotFoundError:
        print(f"Could not find studentVle.csv. Check your folder path!")
    except Exception as e:
        print(f"Failed to load studentVle.csv. Error: {e}")

if __name__ == "__main__":
    print("Initiating Phase 1: Database Connection...")
    test_connection()
    # load_parent_tables()
    # load_child_tables()
    load_clicks_table()