import pandas as pd
from connection import get_db_connection  # Asegúrate de que get_db_connection() esté correctamente definido en connection.py

# Ruta al archivo CSV
file_path = './data/temperatura.csv'

# Leer el archivo CSV con el separador correcto
df = pd.read_csv(file_path, sep=';') 

# Convertir la columna 'Date' al tipo datetime y luego al formato ISO 8601
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Conectar a la base de datos
conn = get_db_connection()  # Ajusta la función según cómo obtengas la conexión a tu base de datos
cursor = conn.cursor()

# Insertar los datos del DataFrame en la tabla
for index, row in df.iterrows():
    cursor.execute("INSERT INTO Temperature (Id, Value, Date) VALUES (?, ?, ?)", 
                   (row['Id'], row['Value'], row['Date'].strftime('%Y-%m-%d')))

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Datos importados exitosamente a la base de datos.")
