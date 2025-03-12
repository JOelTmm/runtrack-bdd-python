import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="Pipes606&",           
    database="LaPlateforme" 
)

cursor = conn.cursor()

cursor.execute("SELECT nom, capacite FROM salle")

resultats = cursor.fetchall()
print(resultats)  

cursor.close()
conn.close()
