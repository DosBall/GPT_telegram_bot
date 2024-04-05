from sshtunnel import SSHTunnelForwarder
import psycopg2
import pandas as pd

# SSH tunnel setup
ssh_host = #ip
ssh_username = #name
ssh_pkey =  # Path to your private key file
ssh_pkey_password = 
remote_bind_address = 
remote_bind_port = 3306
local_bind_address = 
local_bind_port = 8000

# PostgreSQL setup
db_name = 
db_username = 
db_password = 

with SSHTunnelForwarder(
    (ssh_host, 22),
    ssh_username=ssh_username,
    ssh_pkey=ssh_pkey,  # Use your private key for authentication
    ssh_private_key_password=ssh_pkey_password,
    remote_bind_address=(<ip>, 8080)
) as tunnel:
    conn = psycopg2.connect(
        host=#<host>,
        port=5432,
        dbname=db_name,
        user=db_username,
        password=db_password
    )
# example of usage

# Create a cursor object
cur = conn.cursor()

df_users = pd.read_sql_query('''select distinct sender_user_id from chat_messages where inserted_at >= '2023-01-01' and length(text)>=50 and text like '%?%' and receiver_user_id is null''',conn)

df_all = pd.DataFrame()
users = tuple(df_users['sender_user_id'])

for i in range(len(users)):
    try:
        df = cur.execute('''with users as (select distinct sender_user_id from chat_messages where sender_user_id = %s),
        messages_send as (select sender_user_id, text send_text, inserted_at
                        from chat_messages
                        where sender_user_id in (select * from users)
                            and inserted_at >= '2023-01-01'),
        messages_receive as (select receiver_user_id, text rec_text, inserted_at
                            from chat_messages
                            where receiver_user_id in (select * from users)
                                and inserted_at >= '2023-01-01'), main as (
    select s.sender_user_id,s.send_text,s.inserted_at send_date,r.receiver_user_id,r.rec_text,r.inserted_at received_date, row_number() over (partition by sender_user_id,send_text order by r.inserted_at asc) as rank
    from messages_send s
            left join messages_receive r on s.sender_user_id = r.receiver_user_id and s.inserted_at <= r.inserted_at
    order by s.inserted_at desc, r.inserted_at asc)
    select * from main where rank = 1 and length(send_text)>=50''', (users[i],))
        #df_all = df_all.append(df)
        df_all = pd.concat([df_all, df])
        print(cur.fetchall())
        print('-----------------------------------')
    except Exception as e:
        print(e)
        print('-----------------------------------')
        continue
print(df_users.columns)
cur.close()
conn.close()





