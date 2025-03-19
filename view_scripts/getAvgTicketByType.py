import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host="localhost",    
    user="root",         
    password="MilaLab*",  
    database="clinica_w_data"  
)

# Crear un cursor para ejecutar la consulta
cursor = connection.cursor()

# Consulta SQL para obtener el ticket promedio por sucursal, año y tipo de producto
query_ticket_promedio = """
SELECT 
    b.name AS branch_name, 
    YEAR(s.date) AS year, 
    p.type AS product_type,
    AVG(s.amount) AS ticket_promedio
FROM sales s
INNER JOIN branches b ON b.id = s.branch_id
INNER JOIN sale_details sd ON sd.sale_id = s.id
INNER JOIN products p ON p.id = sd.product_id
WHERE s.status_id = 3
AND s.deleted_at IS NULL
GROUP BY b.name, YEAR(s.date), p.type
ORDER BY b.name, year, p.type;
"""

# Ejecutar la consulta
cursor.execute(query_ticket_promedio)

# Obtener los resultados
results_ticket_promedio = cursor.fetchall()

# Crear un DataFrame con los resultados
columns_ticket_promedio = [column[0] for column in cursor.description]
df = pd.DataFrame(results_ticket_promedio, columns=columns_ticket_promedio)

# Cerrar conexión con la base de datos
cursor.close()
connection.close()

# Pivotar los datos para organizar la tabla
pivot_table = df.pivot_table(index=["branch_name", "product_type"], columns="year", values="ticket_promedio", aggfunc="mean")

# Redondear a 2 decimales
pivot_table = pivot_table.applymap(lambda x: round(x, 2) if pd.notna(x) else "-")

# Crear la imagen con la tabla
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# Convertir la tabla a formato adecuado
table_headers = ["Sucursal", "Tipo de Producto"] + [str(year) for year in pivot_table.columns]
table_rows = [[branch, product] + [str(value) for value in row] for (branch, product), row in zip(pivot_table.index, pivot_table.values)]

# Dibujar la tabla en la imagen
table = ax.table(cellText=table_rows, colLabels=table_headers, cellLoc="center", loc="center", colColours=["lightgray"] * len(table_headers))
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([0, 1])  # Ajusta las dos primeras columnas

# Guardar la imagen
plt.savefig("archivos/old_data/ticket_promedio.png", dpi=300, bbox_inches="tight")

# Mostrar la tabla
plt.show()
