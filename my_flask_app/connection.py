import pyodbc
def get_db_connection():
    SERVER = 'machine-learning-servidor.database.windows.net'
    DATABASE = 'dataTemperatura'
    USERNAME = 'mluser'
    PASSWORD = 'Halion2014'
    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER},1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connectionString)
    return conn
