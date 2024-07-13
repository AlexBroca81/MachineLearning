import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Generando un DataFrame con datos de temperatura de ejemplo
# Aumento la cantidad de datos a 365 días para tener un año completo
data = {
    'Id': [i + 1 for i in range(365)],
    'Fecha': pd.date_range(start='2023-01-01', periods=365, freq='D'),
    'Temperatura': 20 + 10 * np.sin(np.linspace(0, 2 * np.pi, 365)) + np.random.normal(0, 2, 365) # Simulando un patrón estacional con ruido
}
df = pd.DataFrame(data)

# Redondeando los valores de la columna 'Temperatura' a 2 decimales
df['Temperatura'] = df['Temperatura'].round(2)

# Guardando el DataFrame en un archivo CSV
df.to_csv('data/temperatura.csv', index=False)

# Leyendo el archivo CSV
df = pd.read_csv('data/temperatura.csv')

# Mostrando los primeros registros para verificar
print(df.head())

df['Fecha'] = pd.to_datetime(df['Fecha'])

df['Dia_del_ano'] = df['Fecha'].dt.dayofyear

X = df[['Dia_del_ano']].values
y = df['Temperatura'].values

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(128, input_dim=1, activation='relu'))  # Aumentamos el tamaño de las capas ocultas
model.add(Dense(64, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

history = model.fit(X_train, y_train, epochs=200, batch_size=16, validation_split=0.2)  # Aumentamos el número de épocas y cambiamos el tamaño de batch

loss = model.evaluate(X_test, y_test)
print(f'Pérdida en el conjunto de prueba: {loss}')

# Haciendo predicciones con nuevos datos
new_data = np.array([[200]])  # Día del año 200
new_data_scaled = scaler_X.transform(new_data)
prediction_scaled = model.predict(new_data_scaled)
prediction = scaler_y.inverse_transform(prediction_scaled)
print(f'Predicción de temperatura para el día 200 del año: {prediction[0][0]:.2f}')  # Redondear la predicción a 2 decimales

# Verificando las predicciones en los datos de prueba
predictions = model.predict(X_test)
predictions_descaled = scaler_y.inverse_transform(predictions)
actuals_descaled = scaler_y.inverse_transform(y_test)

# Mostrando algunas predicciones vs valores reales
for i in range(5):
    print(f'Predicción: {predictions_descaled[i][0]:.2f}, Valor real: {actuals_descaled[i][0]:.2f}')
