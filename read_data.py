import pandas as pd
import sqlite3
conn = sqlite3.connect('amztracker.db')
df = pd.read_sql_query('''SELECT * FROM prices''',conn)
print(df)