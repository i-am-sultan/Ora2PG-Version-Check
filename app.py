import tkinter as tk
from tkinter import messagebox
import cx_Oracle

import os

def compare_db_versions():
    try:
        # Connect to Oracle as sysdba
        dsn_tns = cx_Oracle.makedsn(oracle_hostname.get(), oracle_port.get(), service_name=oracle_schema.get())
        oracle_conn = cx_Oracle.connect(user=oracle_username.get(), password=oracle_password.get(), dsn=dsn_tns, mode=cx_Oracle.SYSDBA)
        
        oracle_cursor = oracle_conn.cursor()
        oracle_cursor.execute("SELECT db_version FROM sys.packdef")
        oracle_version = oracle_cursor.fetchone()[0]
        
        # Connect to PostgreSQL
        postgres_conn = psycopg2.connect(
            dbname=postgres_dbname.get(),
            user=postgres_username.get(),
            password=postgres_password.get(),
            host=postgres_hostname.get(),
            port=postgres_port.get()
        )
        postgres_cursor = postgres_conn.cursor()
        postgres_cursor.execute("SELECT db_version FROM gateway.packdef")
        postgres_version = postgres_cursor.fetchone()[0]
        
        # Compare Versions
        if oracle_version == postgres_version:
            messagebox.showinfo("Result", "DB Versions are the same!")
        else:
            messagebox.showinfo("Result", f"DB Versions differ: Oracle ({oracle_version}) vs PostgreSQL ({postgres_version})")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))
    
    finally:
        if 'oracle_conn' in locals():
            oracle_conn.close()
        if 'postgres_conn' in locals():
            postgres_conn.close()

# Default values for Oracle credentials
default_oracle_hostname = "localhost"
default_oracle_port = "1521"
default_oracle_username = "sys"
default_oracle_password = "sultan"
default_oracle_schema = "ORCL"

# Default values for PostgreSQL credentials
default_postgres_hostname = "localhost"
default_postgres_port = "5432"
default_postgres_username = "postgres"
default_postgres_password = "12345"
default_postgres_dbname = "student"


# Create Tkinter GUI
root = tk.Tk()
root.title("DB Version Comparator")

# Oracle Credentials
tk.Label(root, text="Oracle Hostname").grid(row=0)
tk.Label(root, text="Oracle Port").grid(row=1)
tk.Label(root, text="Oracle Username").grid(row=2)
tk.Label(root, text="Oracle Password").grid(row=3)
tk.Label(root, text="Oracle Schema").grid(row=4)

oracle_hostname = tk.Entry(root)
oracle_port = tk.Entry(root)
oracle_username = tk.Entry(root)
oracle_password = tk.Entry(root, show="*")
oracle_schema = tk.Entry(root)

# Insert default values
oracle_hostname.insert(0, default_oracle_hostname)
oracle_port.insert(0, default_oracle_port)
oracle_username.insert(0, default_oracle_username)
oracle_password.insert(0, default_oracle_password)
oracle_schema.insert(0, default_oracle_schema)

oracle_hostname.grid(row=0, column=1)
oracle_port.grid(row=1, column=1)
oracle_username.grid(row=2, column=1)
oracle_password.grid(row=3, column=1)
oracle_schema.grid(row=4, column=1)

# PostgreSQL Credentials
tk.Label(root, text="PostgreSQL Hostname").grid(row=5)
tk.Label(root, text="PostgreSQL Port").grid(row=6)
tk.Label(root, text="PostgreSQL Username").grid(row=7)
tk.Label(root, text="PostgreSQL Password").grid(row=8)
tk.Label(root, text="PostgreSQL DB Name").grid(row=9)

postgres_hostname = tk.Entry(root)
postgres_port = tk.Entry(root)
postgres_username = tk.Entry(root)
postgres_password = tk.Entry(root, show="*")
postgres_dbname = tk.Entry(root)

# Insert default values
postgres_hostname.insert(0, default_postgres_hostname)
postgres_port.insert(0, default_postgres_port)
postgres_username.insert(0, default_postgres_username)
postgres_password.insert(0, default_postgres_password)
postgres_dbname.insert(0, default_postgres_dbname)

postgres_hostname.grid(row=5, column=1)
postgres_port.grid(row=6, column=1)
postgres_username.grid(row=7, column=1)
postgres_password.grid(row=8, column=1)
postgres_dbname.grid(row=9, column=1)

# Compare Button
compare_button = tk.Button(root, text="Compare", command=compare_db_versions)
compare_button.grid(row=10, columnspan=2)

root.mainloop()
