import mysql.connector
import pandas as pd

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host="localhost",    
    user="root",         
    password="C1e0-cat-m0wers",  
    database="clinica_w_data"  
)

# Crear un cursor para ejecutar la consulta
cursor = connection.cursor()

# Consulta SQL para obtener el ticket promedio por sucursal y año
query_ticket_promedio = """
SELECT 
    b.name AS branch_name, 
    YEAR(s.date) AS year, 
    AVG(s.amount) AS ticket_promedio
FROM sales s
INNER JOIN branches b ON b.id = s.branch_id
WHERE s.status_id = 3
AND s.deleted_at is NULL
GROUP BY b.name, YEAR(s.date);
"""

# Ejecutar la consulta
cursor.execute(query_ticket_promedio)

# Obtener los resultados
results_ticket_promedio = cursor.fetchall()

# Crear un DataFrame con los resultados
columns_ticket_promedio = [column[0] for column in cursor.description]
df_ticket_promedio = pd.DataFrame(results_ticket_promedio, columns=columns_ticket_promedio)

# Cerrar conexión con la base de datos
cursor.close()
connection.close()

# Guardar el DataFrame en un archivo CSV
df_ticket_promedio.to_csv("archivos/ticket_promedio.csv", index=False)

# Mostrar los primeros registros
print(df_ticket_promedio.head())
