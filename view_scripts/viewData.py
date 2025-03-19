import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Cargar datos
df = pd.read_csv("archivos/old_data/clean_clients.csv")
df_ticket = pd.read_csv("archivos/old_data/ticket_promedio.csv")

def generar_reporte():
    pdf = FPDF("P", "mm", "A4")  
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Título del Reporte
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Reporte de Ventas y Propuesta de Clientes", ln=True, align='C')
    pdf.ln(10)

    # 📌 **SECCIÓN 1: Tabla de Ticket Promedio**
    df_pivot = df_ticket.pivot_table(index='branch_name', columns='year', values='ticket_promedio', aggfunc='mean').reset_index()
    
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Ticket Promedio por Sucursal y Año", ln=True, align='C')
    pdf.ln(5)
    
    # Columnas
    years = df_pivot.columns[1:]
    col_widths = [50] + [25] * len(years)
    
    pdf.set_font("Arial", size=10)
    pdf.cell(col_widths[0], 8, "Sucursal", border=1, align='C')
    for year in years:
        pdf.cell(col_widths[1], 8, str(int(year)), border=1, align='C')
    pdf.ln()
    
    pdf.set_font("Arial", size=8)
    for _, row in df_pivot.iterrows():
        pdf.cell(col_widths[0], 8, str(row['branch_name']), border=1, align='C')
        for year in years:
            pdf.cell(col_widths[1], 8, f"${row[year]:.2f}" if pd.notna(row[year]) else "N/A", border=1, align='C')
        pdf.ln()

    pdf.ln(10)

    # 📌 **SECCIÓN 2: Gráfico de Clientes según Compras**
    mean_compras = df["compras_2024_2025"].mean()

    clientes_congelados = df[df["compras_2024_2025"] == 0] 
    cliente_basico = df[(df["compras_2024_2025"] > 0) & (df["compras_2024_2025"] <= mean_compras)]
    cliente_recurrente = df[(df["compras_2024_2025"] > mean_compras) & (df["compras_2024_2025"] <= 5)]
    super_cliente = df[df["compras_2024_2025"] > 5]

    categorias = ["Clientes Congelados", "Clientes Básicos", "Clientes Recurrentes", "Super Clientes"]
    valores = [len(clientes_congelados), len(cliente_basico), len(cliente_recurrente), len(super_cliente)]
    
    # Gráfico de pastel con Matplotlib
    plt.figure(figsize=(6, 6))
    plt.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=140, wedgeprops={"edgecolor": "black"})
    plt.title("Propuesta de Tipo de Clientes según compras")
    plt.savefig("archivos/old_data/grafico_compras.png")
    plt.close()

    pdf.cell(200, 10, "Propuesta de Tipo de Clientes según cantidad de compras en el periodo 2024/2025", ln=True, align='C')
    pdf.ln(5)
    pdf.image("archivos/old_data/grafico_compras.png", x=30, w=150)
    pdf.ln(15)
    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, "Descripción: Este gráfico muestra la distribución de clientes según su frecuencia de compra en el periodo 2024/2025.")
    pdf.ln(10)

    # 📌 **SECCIÓN 3: Gráfico de Clientes según Dinero Gastado**
    mean_gasto = df["total_gastado_2024_2025"].mean()
    
    clientes_bajo_gasto = df[df["total_gastado_2024_2025"] <= mean_gasto]
    clientes_medio_gasto = df[(df["total_gastado_2024_2025"] > mean_gasto) & (df["total_gastado_2024_2025"] <= 5000)]
    clientes_alto_gasto = df[df["total_gastado_2024_2025"] > 5000]

    categorias_gasto = ["Bajo Gasto", "Medio Gasto", "Alto Gasto"]
    valores_gasto = [len(clientes_bajo_gasto), len(clientes_medio_gasto), len(clientes_alto_gasto)]

    # Gráfico de pastel con Matplotlib
    plt.figure(figsize=(6, 6))
    plt.pie(valores_gasto, labels=categorias_gasto, autopct="%1.1f%%", startangle=140, wedgeprops={"edgecolor": "black"})
    plt.title("Propuesta de Tipo de Clientes según gasto")
    plt.savefig("archivos/old_data/grafico_gasto.png")
    plt.close()

    pdf.cell(200, 10, "Propuesta de Tipo de Clientes según dinero gastado en el periodo 2024/2025", ln=True, align='C')
    pdf.ln(5)
    pdf.image("archivos/old_data/grafico_gasto.png", x=30, w=150)
    pdf.ln(15)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, "Descripción: Este gráfico muestra la clasificación de clientes según el monto total gastado en 2024/2025.")
    pdf.ln(10)

    # Guardar PDF
    pdf.output("archivos/old_data/reporte_clientes.pdf")
    print("Informe generado: archivos/old_data/reporte_clientes.pdf")

generar_reporte()
