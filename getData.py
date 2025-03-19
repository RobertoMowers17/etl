import mysql.connector
import pandas as pd

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host="localhost",    
    user="root",         
    password="C1e0-cat-m0wers",  
    database="clinica_w_data"  
)

cursor = connection.cursor()

# Consulta 1: Obtener la última compra y total de compras por cliente
query_last_purchase = """
SELECT c.id, c.mobil_phone, c.email, c.first_name, c.last_name, c.employment, c.rfc, 
       MAX(s.date) AS ultima_compra, COUNT(*) AS total_compras 
FROM clients c 
INNER JOIN sales s ON c.id = s.client_id 
WHERE c.id != 1 AND s.status_id = 3 AND s.deleted_at IS NULL
GROUP BY c.id;
"""
cursor.execute(query_last_purchase)
df_last_purchase = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])

# Consulta 2: Obtener la cantidad de compras por año
query_compras_por_año = """
SELECT c.id, YEAR(s.date) AS year, COUNT(*) AS compras
FROM clients c
INNER JOIN sales s ON c.id = s.client_id
WHERE c.id != 1 AND s.status_id = 3 AND s.deleted_at IS NULL
GROUP BY c.id, YEAR(s.date);
"""
cursor.execute(query_compras_por_año)
df_compras_por_año = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])

# Transformar la tabla de compras por año
df_compras_pivot = df_compras_por_año.pivot(index="id", columns="year", values="compras").fillna(0).astype(int)
df_compras_pivot["compras_2024_2025"] = df_compras_pivot.get(2024, 0) + df_compras_pivot.get(2025, 0)

# Consulta 3: Obtener el total gastado por cliente
query_total_spent = """
SELECT c.id, SUM(s.amount) AS total_gastado
FROM clients c
INNER JOIN sales s ON c.id = s.client_id
WHERE c.id != 1 AND s.status_id = 3 AND s.deleted_at IS NULL
GROUP BY c.id;
"""
cursor.execute(query_total_spent)
df_total_spent = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])

# Consulta 4: Obtener el total gastado en 2024/2025
query_total_spent_2024_2025 = """
SELECT c.id, SUM(s.amount) AS total_gastado_2024_2025
FROM clients c
INNER JOIN sales s ON c.id = s.client_id
WHERE c.id != 1 AND s.status_id = 3 AND s.deleted_at IS NULL 
AND YEAR(s.date) IN (2024, 2025)
GROUP BY c.id;
"""
cursor.execute(query_total_spent_2024_2025)
df_total_spent_2024_2025 = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])

# Cerrar conexión
cursor.close()
connection.close()

# Fusionar DataFrames
df_final = df_last_purchase.merge(df_compras_pivot, on="id", how="left")
df_final = df_final.merge(df_total_spent, on="id", how="left")
df_final = df_final.merge(df_total_spent_2024_2025, on="id", how="left")

# Rellenar valores nulos con 0
df_final = df_final.fillna(0)

# Guardar el DataFrame en un archivo CSV
df_final.to_csv('archivos/clientes.csv', index=False)

print("DataFrame combinado guardado en clientes.csv")
print(df_final.head())
