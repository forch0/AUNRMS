# import psycopg2
# import os

# # Database connection details
# LOCAL_DB = {
#     'dbname': os.getenv('DB_NAME', 'AUN'),
#     'user': os.getenv('DB_USER', 'postgres'),
#     'password': os.getenv('DB_PASSWORD', 'POSTGRES'),
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'port': os.getenv('DB_PORT', '5432'),
# }

# # Supabase database configuration
# SUPABASE_DB = {
#     'dbname': 'postgres',
#     'user': 'postgres.cesztotrungramvrtiqa',
#     'password': 'nSbWwmdEk#f2dv3',
#     'host': 'aws-0-eu-central-1.pooler.supabase.com',
#     'port': '5432',
# }

# def get_table_names(conn):
#     """Fetches table names from the database."""
#     with conn.cursor() as cursor:
#         cursor.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public'
#         """)
#         tables = cursor.fetchall()
#     return [table[0] for table in tables]

# def sync_table(local_conn, supabase_conn, table_name):
#     """Syncs a single table between local and Supabase databases."""
#     with local_conn.cursor() as local_cursor, supabase_conn.cursor() as supabase_cursor:
#         try:
#             # Fetch data from local table
#             local_cursor.execute(f"SELECT * FROM {table_name}")
#             rows = local_cursor.fetchall()
#             columns = [desc[0] for desc in local_cursor.description]

#             # Create an insert query for Supabase
#             if rows:
#                 placeholders = ', '.join(['%s'] * len(columns))
#                 insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

#                 # Copy data to Supabase table
#                 for row in rows:
#                     try:
#                         supabase_cursor.execute(insert_query, row)
#                     except Exception as e:
#                         print(f"Error inserting row into table '{table_name}': {e}")

#                 # Commit changes to Supabase
#                 supabase_conn.commit()
#                 print(f"Successfully synced table '{table_name}'")
#             else:
#                 print(f"No data found for table '{table_name}'")

#         except Exception as e:
#             print(f"An error occurred while syncing table '{table_name}': {e}")

# def main():
#     # Connect to local and Supabase databases
#     try:
#         local_conn = psycopg2.connect(**LOCAL_DB)
#         supabase_conn = psycopg2.connect(**SUPABASE_DB)

#         # Get list of tables from local database
#         tables = get_table_names(local_conn)
#         print(f"Tables found: {tables}")

#         # Sync each table
#         for table in tables:
#             sync_table(local_conn, supabase_conn, table)

#     except Exception as e:
#         print(f"An error occurred during syncing: {e}")

#     finally:
#         # Close database connections
#         local_conn.close()
#         supabase_conn.close()

# if __name__ == "__main__":
#     main()