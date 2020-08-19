import psycopg2


database = 'ipo_crawler'
user = 'postgres'
password = '@Futeng2466'
host = '127.0.0.1'
port ='5432'

conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
# print('Opened database successfully')

cur = conn.cursor()

sql_create_table = "CREATE TABLE ipo_crawler (id serial not null primary key, market char(20) not NULL, stock_code char(20) not NULL, stock_name char(20) not NULL, total_issued char(20) not NULL, public_price char(20) not NULL, lots_size char(20) not NULL, currency char(20) not NULL, subscription_date_start char(20) not NULL, subscription_date_end char(20) not NULL, public_date char(20) not NULL);"
# sql_create_table = "CREATE TABLE stock_event (id serial not null primary key, market char(20) not NULL, stock_code char(20) not NULL, stock_name char(20) not NULL, sus_trad_status char(20) not NULL, suspension_price char(20), trading_price char(20), currency char(20) not NULL, suspension_date_start char(20), trading_date_start char(20), suspension_reason char(20) not NULL);"
cur.execute(sql_create_table)
print("Created table Successfull.")

# sql_select = 'select * from ipocrawler'
# cur.execute(sql_select)
# rows = cur.fetchall()
# for row in rows:
#     print(row)

conn.commit()
conn.close()
