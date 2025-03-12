import mysql.connector

# Connexion à la base de données
try:
    conn = mysql.connector.connect(
        host="localhost",       
        user="root",            
        password="Pipes606&",  
        database="LaPlateforme" 
    )

    if conn.is_connected():
        print("✅ Connexion réussie à la base de données 'LaPlateforme'")

        cursor = conn.cursor()

        query = "SELECT * FROM etudiant"
        cursor.execute(query)

        resultats = cursor.fetchall()

        print("\nListe des étudiants :")
        for etudiant in resultats:
            print(etudiant)

        cursor.close()
        conn.close()

except mysql.connector.Error as e:
    print(f"❌ Erreur lors de la connexion à MySQL : {e}")
