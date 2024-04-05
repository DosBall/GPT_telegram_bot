from sshtunnel import SSHTunnelForwarder
import psycopg2
import pandas as pd
import json

cred = r'qalan_cred.json'
glob_params = json.load(open(cred))

def get_sql_data(query,db_name):
    global glob_params
    params = glob_params[db_name]

    if db_name == 'qalan':
        # SSH tunnel setup
        ssh_host = params['ssh_host']
        ssh_username = params['ssh_username']
        ssh_pkey = "pskz_db_ssh_key.txt"  # Path to your private key file
        ssh_pkey_password = params['ssh_pkey_password']
        remote_bind_address = 'localhost'
        remote_bind_port = 3306
        local_bind_address = 'localhost'
        local_bind_port = 8000

        # PostgreSQL setup
        db_name = params['db_name']
        db_username = params['db_username']
        db_password = params['db_password']
        try:
            with SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_username,
                ssh_pkey=ssh_pkey,  # Use your private key for authentication
                ssh_private_key_password=ssh_pkey_password,
                remote_bind_address=('127.0.0.1', 8080)
            ) as tunnel:
                conn = psycopg2.connect(
                    host=params['host'],
                    port=params['port'],
                    dbname=db_name,
                    user=db_username,
                    password=db_password
                )
            # example of usage

             # Create a cursor object
            cur = conn.cursor()
            try:    
                df_user = pd.read_sql_query(query, conn)
                return df_user
            
            except Exception as e_get:
                print(e_get)

            cur.close()
            conn.close()

        except Exception as e:
           print(e)

def insert_sql_data(query,db_name):
    global glob_params
    params = glob_params[db_name]

    if db_name == 'qalan':
        # SSH tunnel setup
        ssh_host = params['ssh_host']
        ssh_username = params['ssh_username']
        ssh_pkey = "pskz_db_ssh_key.txt"  # Path to your private key file
        ssh_pkey_password = params['ssh_pkey_password']
        remote_bind_address = 'localhost'
        remote_bind_port = 3306
        local_bind_address = 'localhost'
        local_bind_port = 8000

        # PostgreSQL setup
        db_name = params['db_name']
        db_username = params['db_username']
        db_password = params['db_password']
        try:
            with SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_username,
                ssh_pkey=ssh_pkey,  # Use your private key for authentication
                ssh_private_key_password=ssh_pkey_password,
                remote_bind_address=('127.0.0.1', 8080)
            ) as tunnel:
                conn = psycopg2.connect(
                    host=params['host'],
                    port=params['port'],
                    dbname=db_name,
                    user=db_username,
                    password=db_password
                )

            cur = conn.cursor()
             # example of usage

             # Create a cursor object
        
            try:
                cur.execute(query)
            except Exception as e_insert:
                print(e_insert)

            cur.close()
            conn.close()
        except Exception as e:
           print(e)

query = '''select * from pupils limit 10'''
get_sql_data(query,'qalan')
