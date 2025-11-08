import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo para gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
print("ANÁLISIS DE VENTAS - TIENDA ELECTRÓNICA".center(70))
print()
# Carga de datos
df = pd.read_csv('ventas_electronica.csv')
# Convertir fecha a datetime
df['fecha'] = pd.to_datetime(df['fecha'])
# Crear columna de ingreso total
df['ingreso_total'] = df['precio'] * df['cantidad']
# Extraer mes de la fecha
df['mes'] = df['fecha'].dt.month_name()
print(f"Datos cargados exitosamente")
print(f"Total de registros: {len(df)}")
print(f"Periodo: {df['fecha'].min().strftime('%d/%m/%Y')} - {df['fecha'].max().strftime('%d/%m/%Y')}")
print()
# Primeras filas
print(" Primeras 5 filas del dataset:")
print(df.head())
print()
# Información del dataset
print("Información del dataset:")
print(df.info())
print()
# Análisis estadístico
print("\n" + "="*70)
print("2. ESTADÍSTICAS DESCRIPTIVAS")
print("-" * 70)
print("\n Estadísticas de Precios:")
print(df['precio'].describe())
print("\nEstadísticas de Cantidad:")
print(df['cantidad'].describe())
print("\nEstadísticas de Ingresos Totales:")
print(df['ingreso_total'].describe())
print()
#Analisis por categorias
print("\n" + "="*70)
print("3. ANÁLISIS POR CATEGORÍAS")
print("-" * 70)
ventas_categoria = df.groupby('categoria').agg({
    'ingreso_total': 'sum',
    'cantidad': 'sum',
    'producto': 'count'
}).round(2)
ventas_categoria.columns = ['Ingreso Total', 'Unidades Vendidas', 'Transacciones']
ventas_categoria = ventas_categoria.sort_values('Ingreso Total', ascending=False)
print("\n Ventas por Categoría:")
print(ventas_categoria)
print()
# Categoría más rentable
categoria_top = ventas_categoria.index[0]
ingreso_top = ventas_categoria.iloc[0]['Ingreso Total']
print(f" Categoría más rentable: {categoria_top} (${ingreso_top:,.2f})")
print()
# ========== 4. ANÁLISIS POR VENDEDOR ==========
print("\n" + "="*70)
print("  4. ANÁLISIS POR VENDEDOR")
print("-" * 70)
ventas_vendedor = df.groupby('vendedor').agg({
    'ingreso_total': 'sum',
    'producto': 'count'
}).round(2)
ventas_vendedor.columns = ['Ingreso Total', 'Ventas Realizadas']
ventas_vendedor = ventas_vendedor.sort_values('Ingreso Total', ascending=False)
print("\n Desempeño por Vendedor:")
print(ventas_vendedor)
print()
mejor_vendedor = ventas_vendedor.index[0]
print(f" Mejor vendedor: {mejor_vendedor} (${ventas_vendedor.iloc[0]['Ingreso Total']:,.2f})")
print()
# Análisis por ciudad
print("\n" + "="*70)
print(" 5. ANÁLISIS POR CIUDAD")
print("-" * 70)
ventas_ciudad = df.groupby('ciudad').agg({
    'ingreso_total': 'sum',
    'producto': 'count'
}).round(2)
ventas_ciudad.columns = ['Ingreso Total', 'Transacciones']
ventas_ciudad = ventas_ciudad.sort_values('Ingreso Total', ascending=False)
print("\n Ventas por Ciudad:")
print(ventas_ciudad)
print()
# Analisis metodo de pago
print("\n" + "="*70)
print(" 6. ANÁLISIS POR MÉTODO DE PAGO")
print("-" * 70)
metodo_pago = df.groupby('metodo_pago').agg({
    'ingreso_total': 'sum',
    'producto': 'count'
}).round(2)
metodo_pago.columns = ['Ingreso Total', 'Transacciones']
metodo_pago['Porcentaje'] = (metodo_pago['Transacciones'] / metodo_pago['Transacciones'].sum() * 100).round(2)
print("\n Ventas por Método de Pago:")
print(metodo_pago)
print()
# Productos mas vendidos
print("\n" + "="*70)
print(" 7. TOP 10 PRODUCTOS MÁS VENDIDOS")
print("-" * 70)
productos_top = df.groupby('producto').agg({
    'cantidad': 'sum',
    'ingreso_total': 'sum'
}).round(2)
productos_top.columns = ['Unidades Vendidas', 'Ingreso Total']
productos_top = productos_top.sort_values('Ingreso Total', ascending=False).head(10)
print("\n Top 10 Productos por Ingreso:")
print(productos_top)
print()
# Analisis de tiempo
print("\n" + "="*70)
print("8. ANÁLISIS TEMPORAL (POR MES)")
print("-" * 70)
ventas_mes = df.groupby('mes').agg({
    'ingreso_total': 'sum',
    'producto': 'count'
}).round(2)
ventas_mes.columns = ['Ingreso Total', 'Transacciones']
# Ordenar por el orden de los meses
order_meses = ['January', 'February', 'March']
ventas_mes = ventas_mes.reindex(order_meses)
print("\n Ventas por Mes:")
print(ventas_mes)
print()
# metricas
print("\n" + "="*70)
print(" 9. MÉTRICAS CLAVE DEL NEGOCIO")
print("-" * 70)
total_ingresos = df['ingreso_total'].sum()
total_transacciones = len(df)
ticket_promedio = df['ingreso_total'].mean()
productos_vendidos = df['cantidad'].sum()
print(f"\n  Ingresos Totales: ${total_ingresos:,.2f}")
print(f" Total de Transacciones: {total_transacciones}")
print(f"  Ticket Promedio: ${ticket_promedio:,.2f}")
print(f"  Total de Productos Vendidos: {productos_vendidos} unidades")
print()
# Visualizacion
print("\n" + "="*70)
print(" 10. GENERANDO VISUALIZACIONES...")
print("-" * 70)
# Crear figura con múltiples subplots
fig = plt.figure(figsize=(16, 12))
# 1. Ingresos por Categoría
plt.subplot(2, 3, 1)
ventas_categoria['Ingreso Total'].plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Ingresos por Categoría', fontsize=14, fontweight='bold')
plt.xlabel('Categoría')
plt.ylabel('Ingresos ($)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
# 2. Ventas por Vendedor
plt.subplot(2, 3, 2)
ventas_vendedor['Ingreso Total'].plot(kind='bar', color='lightcoral', edgecolor='black')
plt.title('Ingresos por Vendedor', fontsize=14, fontweight='bold')
plt.xlabel('Vendedor')
plt.ylabel('Ingresos ($)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
# 3. Distribución de Métodos de Pago
plt.subplot(2, 3, 3)
metodo_pago['Transacciones'].plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                                   colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Distribución de Métodos de Pago', fontsize=14, fontweight='bold')
plt.ylabel('')
# 4. Ventas por Ciudad
plt.subplot(2, 3, 4)
ventas_ciudad['Ingreso Total'].plot(kind='barh', color='lightgreen', edgecolor='black')
plt.title('Ingresos por Ciudad', fontsize=14, fontweight='bold')
plt.xlabel('Ingresos ($)')
plt.ylabel('Ciudad')
plt.grid(axis='x', alpha=0.3)
# 5. Top 5 Productos
plt.subplot(2, 3, 5)
productos_top.head(5)['Ingreso Total'].plot(kind='barh', color='gold', edgecolor='black')
plt.title('Top 5 Productos por Ingresos', fontsize=14, fontweight='bold')
plt.xlabel('Ingresos ($)')
plt.ylabel('Producto')
plt.grid(axis='x', alpha=0.3)
# 6. Tendencia Mensual
plt.subplot(2, 3, 6)
ventas_mes['Ingreso Total'].plot(kind='line', marker='o', linewidth=2, 
                                 markersize=8, color='purple')
plt.title('Tendencia de Ingresos Mensuales', fontsize=14, fontweight='bold')
plt.xlabel('Mes')
plt.ylabel('Ingresos ($)')
plt.xticks(range(len(ventas_mes)), ['Enero', 'Febrero', 'Marzo'], rotation=0)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/analisis_ventas.png', dpi=300, bbox_inches='tight')
print(" Gráfico guardado como 'analisis_ventas.png'")
