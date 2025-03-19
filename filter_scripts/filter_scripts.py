import pandas as pd

df = pd.read_csv("archivos/clean_clients.csv") 

# Personas sin compras los ultimos 8 meses se asignaran como Clientes congelados

df["Tipo de Cliente"] = df["Tipo de Cliente"].astype(str) 
df.loc[df["total_gastado_ultimos_8_meses"] == 0, "Tipo de Cliente"] = "Cliente Congelado"
df.to_csv("archivos/clean_clients.csv", index=False)


# Revisar el promedio de los clientes restantes

max_compras = df["total_gastado_ultimos_8_meses"].where(df["Tipo de Cliente"] != "Cliente Congelado").max()
min_compras = df["total_gastado_ultimos_8_meses"].where(df["Tipo de Cliente"] != "Cliente Congelado").min()
mean_compras = df["total_gastado_ultimos_8_meses"].where(df["Tipo de Cliente"] != "Cliente Congelado").mean()

print(f"Valor máximo de compras de un cliente en el periodo (ultimos 8 meses): {max_compras}")
print(f"Valor mínimo de compras de un cliente en el periodo (ultimos 8 meses): {min_compras}")
print(f"Promedio de compras por cliente en el periodo (ultimos 8 meses): {mean_compras:.2f}")


# Analisis de clientes activos

active_clients = df["total_gastado_ultimos_8_meses"].where(df["Tipo de Cliente"] != "Cliente Congelado")

count_active_clients = active_clients.count()
count_over_30 = active_clients[active_clients > 20000].count()

print(f"Hay un tal de {count_active_clients} clientes activos de los cuales {count_over_30} superan los 20,000 en los ultimos 8 meses ")


# Asignamos a estos clientes el tipo Cliente VIP

df.loc[df["total_gastado_ultimos_8_meses"] > 20000, "Tipo de Cliente"] = "Cliente VIP"
df.to_csv("archivos/clean_clients.csv", index=False)


# Clientes restantes (Basico, Recurrente, o Super Cliente)

clientes_normales = df["total_gastado_ultimos_8_meses"].where(df["Tipo de Cliente"] == "nan" ).count()

mean_compras = df["total_gastado_ultimos_8_meses"].where(df["Tipo de Cliente"] == "nan" ).mean()

mas_que_mean = df["total_gastado_ultimos_8_meses"].where((df["Tipo de Cliente"] == "nan") & (df["total_gastado_ultimos_8_meses"] > mean_compras)).count()
menos_que_mean = df["total_gastado_ultimos_8_meses"].where((df["Tipo de Cliente"] == "nan") & (df["total_gastado_ultimos_8_meses"] < mean_compras)).count()


print(f"Quedan un total de {clientes_normales} sin asignar y su promedio en los ultimos 8 meses es de {mean_compras:.2f}")
print(f"Hay un total de {mas_que_mean} que tienen mas gastado que el promedio y un total de {menos_que_mean} que tienen menos")



# 
