import pandas as pd

# Cargar el archivo XLSX
df = pd.read_excel('app/data/departments.xlsx', sheet_name='departments')

# Guardar como CSV con comas como separador
df.to_csv('app/data/departments.csv', index=False, sep=',')

# Cargar el archivo XLSX
df = pd.read_excel('app/data/hired_employees.xlsx', sheet_name='hired_employees')

# Guardar como CSV con comas como separador
df.to_csv('app/data/hired_employees.csv', index=False, sep=',')

# Cargar el archivo XLSX
df = pd.read_excel('app/data/jobs.xlsx', sheet_name='jobs')

# Guardar como CSV con comas como separador
df.to_csv('app/data/jobs.csv', index=False, sep=',')