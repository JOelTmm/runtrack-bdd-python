import mysql.connector

class EmployeCRUD:
    def __init__(self, host="localhost", user="root", password="Pipes606&", database="entreprise"):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("✅ Connexion à la base de données réussie.")
        except mysql.connector.Error as e:
            print("❌ Erreur lors de la connexion :", e)
            exit(1)

    def afficher_employes(self):
        # Requête pour joindre employe et service et trier par nom et prénom
        query = """
        SELECT e.nom, e.prenom, e.salaire, s.nom AS service
        FROM employe e
        JOIN service s ON e.id_service = s.id
        ORDER BY e.nom, e.prenom;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            print("\nListe des employés :")
            # Format souhaité : Nom Prénom salaire€ , Service
            for row in rows:
                nom, prenom, salaire, service = row
                print(f"{nom} {prenom} {salaire:.2f}€, {service}")
        else:
            print("Aucun employé trouvé.")

    def ajouter_employe(self):
        print("\n--- Ajouter un employé ---")
        nom = input("Entrez le nom : ").strip()
        prenom = input("Entrez le prénom : ").strip()
        try:
            salaire = float(input("Entrez le salaire : ").strip())
        except ValueError:
            print("Salaire invalide.")
            return
        try:
            id_service = int(input("Entrez l'ID du service : ").strip())
        except ValueError:
            print("ID du service invalide.")
            return
        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (nom, prenom, salaire, id_service))
        self.conn.commit()
        print("➕ Employé ajouté.")

    def mettre_a_jour_employe(self):
        print("\n--- Mettre à jour le salaire d'un employé ---")
        try:
            employe_id = int(input("Entrez l'ID de l'employé à mettre à jour : ").strip())
        except ValueError:
            print("ID invalide.")
            return
        try:
            nouveau_salaire = float(input("Entrez le nouveau salaire : ").strip())
        except ValueError:
            print("Salaire invalide.")
            return
        query = "UPDATE employe SET salaire = %s WHERE id = %s"
        self.cursor.execute(query, (nouveau_salaire, employe_id))
        self.conn.commit()
        print("💲 Salaire mis à jour.")

    def supprimer_employe(self):
        print("\n--- Supprimer un employé ---")
        try:
            employe_id = int(input("Entrez l'ID de l'employé à supprimer : ").strip())
        except ValueError:
            print("ID invalide.")
            return
        query = "DELETE FROM employe WHERE id = %s"
        self.cursor.execute(query, (employe_id,))
        self.conn.commit()
        print("🗑️ Employé supprimé.")

    def fermer_connexion(self):
        self.cursor.close()
        self.conn.close()
        print("🔒 Connexion à la base de données fermée.")

def menu():
    crud = EmployeCRUD()
    while True:
        print("\n=== Menu CRUD Employé ===")
        print("1. Afficher les employés")
        print("2. Ajouter un employé")
        print("3. Mettre à jour le salaire d'un employé")
        print("4. Supprimer un employé")
        print("5. Quitter")
        choix = input("Entrez votre choix (1-5) : ").strip()
        if choix == '1':
            crud.afficher_employes()
        elif choix == '2':
            crud.ajouter_employe()
        elif choix == '3':
            crud.mettre_a_jour_employe()
        elif choix == '4':
            crud.supprimer_employe()
        elif choix == '5':
            crud.fermer_connexion()
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu()
