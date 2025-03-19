import pandas as pd

df = pd.read_csv("archivos/clientes.csv") 

df["Tipo de Cliente"] = ""
df["Tags"] = "" 

df["ultima_compra"] = pd.to_datetime(df["ultima_compra"], errors="coerce")
df["Last_Year_of_Purchase"] = df["ultima_compra"].dt.year

df.to_csv("archivos/clean_clients.csv", index=False)

# Guardar en Excel
excel_file = "archivos/clean_clients.xlsx"
with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Clientes Limpios", index=False)

year_counts = df["Last_Year_of_Purchase"].value_counts().sort_index()

year_counts_str = " ".join([f"{year} : {count} personas" for year, count in year_counts.items()])
print(f"Años de últimas compras en el sistema: [{year_counts_str}]")

# Obtener el valor máximo y mínimo de compras
max_compras = df["compras_2024_2025"].max()
min_compras = df["compras_2024_2025"].min()
mean_compras = df["compras_2024_2025"].mean()


# Claudia es la persona que tiene mas compras: 109

print(f"Valor máximo de compras de un cliente en el periodo (2024/2025): {max_compras}")
print(f"Valor mínimo de compras de un cliente en el periodo (2024/2025): {min_compras}")
print(f"Promedio de compras por cliente en el periodo (2024/2025): {mean_compras:.2f}")




# Obtener el valor máximo y mínimo de gasto de clientes
max_gastos = df["total_gastado_2024_2025"].max()
min_gastos = df["total_gastado_2024_2025"].min()
mean_gastos = df["total_gastado_2024_2025"].mean()


print(f"Valor máximo de ingresos de un cliente en el periodo (2024/2025): {max_gastos}")
print(f"Valor mínimo de ingresos de un cliente en el periodo (2024/2025): {min_gastos}")
print(f"Promedio de ingresos por cliente en el periodo (2024/2025): {mean_gastos:.2f}")
