import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Generando un DataFrame con datos de temperatura de ejemplo
data = {
    'Id': [i + 1 for i in range(365)],
    'Fecha': pd.date_range(start='2023-01-01', periods=365, freq='D'),
    'Temperatura': 20 + 10 * np.sin(np.linspace(0, 2 * np.pi, 365)) + np.random.normal(0, 2, 365) # Simulando un patrón estacional con ruido
}
df = pd.DataFrame(data)

# Guardando el DataFrame en un archivo CSV
df.to_csv('temperatura.csv', index=False)

# Leyendo el archivo CSV
df = pd.read_csv('temperatura.csv')

# Mostrando los primeros registros para verificar
print(df.head())

df['Fecha'] = pd.to_datetime(df['Fecha'])

# Extrayendo el día del año
df['Dia_del_ano'] = df['Fecha'].dt.dayofyear

# Definiendo las características (X) y la variable objetivo (y)
X = df[['Dia_del_ano']].values
y = df['Temperatura'].values

# Normalizando los datos
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

# Dividiendo los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Creando el modelo
model = Sequential()
model.add(Dense(64, input_dim=1, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(1))

# Compilando el modelo
model.compile(optimizer='adam', loss='mse')

# Entrenando el modelo
model.fit(X_train, y_train, epochs=100, batch_size=10, validation_split=0.2)

# Evaluando el modelo
loss = model.evaluate(X_test, y_test)
print(f'Pérdida en el conjunto de prueba: {loss}')

# Haciendo predicciones con nuevos datos
new_data = np.array([[183]])  # Día del año 183
new_data_scaled = scaler_X.transform(new_data)
prediction_scaled = model.predict(new_data_scaled)
prediction = scaler_y.inverse_transform(prediction_scaled)
print(f'Predicción de temperatura para el día 183 del año: {prediction[0][0]}')
