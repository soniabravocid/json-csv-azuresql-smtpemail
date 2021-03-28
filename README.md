# json-csv-azuresql-smtpemail
--------------------
## Introducción

Aplicación Python que procesa archivos planos con información de usuarios y de clasificación de datos de un conjunto de bases de datos. Dicha aplicación almacena los datos procesados en una base de datos y gatilla envío de correos electrónicos de validación para aquellas bases de datos críticas.

Versión Python: 3.7.4

## Prerrequsitos

* Instalar las siguientes librerias:

`pandas`
`pyodbc`
`ssl`
`email-to`

## Ejecución
Ejecutar main.py

Si desea agregar o modificar los datos de entrada, puede actualizar los archivos:
- input/db_classification.json
- input/users.csv


