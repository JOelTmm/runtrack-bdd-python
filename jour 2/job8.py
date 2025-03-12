import mysql.connector
from datetime import datetime

class ZooManagement:
    def __init__(self, host="localhost", user="root", password="Pipes606&", database="zoo"):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("✅ Connexion à la base de données 'zoo' réussie.")
        except mysql.connector.Error as e:
            print("❌ Erreur lors de la connexion :", e)
            exit(1)

    # --- Opérations sur la table animal ---
    def add_animal(self):
        print("\n--- Ajouter un animal ---")
        nom = input("Nom de l'animal : ").strip()
        race = input("Race : ").strip()
        id_cage_input = input("ID de la cage (laisser vide si non assigné) : ").strip()
        id_cage = int(id_cage_input) if id_cage_input != "" else None
        date_naissance_str = input("Date de naissance (YYYY-MM-DD) : ").strip()
        try:
            # Vérifier la validité de la date
            date_naissance = datetime.strptime(date_naissance_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Format de date invalide.")
            return
        pays_origine = input("Pays d'origine : ").strip()

        sql = """INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine)
                 VALUES (%s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (nom, race, id_cage, date_naissance, pays_origine))
        self.conn.commit()
        print("➕ Animal ajouté avec succès.")

    def update_animal(self):
        print("\n--- Modifier un animal ---")
        try:
            animal_id = int(input("Entrez l'ID de l'animal à modifier : ").strip())
        except ValueError:
            print("❌ ID invalide.")
            return
        print("Entrez les nouvelles valeurs (laisser vide pour ne pas modifier) :")
        nom = input("Nouveau nom : ").strip()
        race = input("Nouvelle race : ").strip()
        id_cage_input = input("Nouvel ID de cage : ").strip()
        date_naissance_str = input("Nouvelle date de naissance (YYYY-MM-DD) : ").strip()
        pays_origine = input("Nouveau pays d'origine : ").strip()

        # Construire la requête de mise à jour dynamiquement
        updates = []
        params = []

        if nom:
            updates.append("nom = %s")
            params.append(nom)
        if race:
            updates.append("race = %s")
            params.append(race)
        if id_cage_input:
            try:
                id_cage = int(id_cage_input)
                updates.append("id_cage = %s")
                params.append(id_cage)
            except ValueError:
                print("❌ ID de cage invalide.")
                return
        if date_naissance_str:
            try:
                date_naissance = datetime.strptime(date_naissance_str, "%Y-%m-%d").date()
                updates.append("date_naissance = %s")
                params.append(date_naissance)
            except ValueError:
                print("❌ Format de date invalide.")
                return
        if pays_origine:
            updates.append("pays_origine = %s")
            params.append(pays_origine)

        if not updates:
            print("Aucune modification saisie.")
            return

        sql = "UPDATE animal SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(animal_id)
        self.cursor.execute(sql, tuple(params))
        self.conn.commit()
        print("📝 Animal mis à jour.")

    def delete_animal(self):
        print("\n--- Supprimer un animal ---")
        try:
            animal_id = int(input("Entrez l'ID de l'animal à supprimer : ").strip())
        except ValueError:
            print("❌ ID invalide.")
            return
        sql = "DELETE FROM animal WHERE id = %s"
        self.cursor.execute(sql, (animal_id,))
        self.conn.commit()
        print("🗑️ Animal supprimé.")

    def display_animals(self):
        print("\n--- Liste de tous les animaux ---")
        sql = "SELECT id, nom, race, id_cage, date_naissance, pays_origine FROM animal"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Aucun animal trouvé.")

    def display_animals_in_cages(self):
        print("\n--- Liste des animaux assignés à une cage ---")
        sql = """SELECT a.id, a.nom, a.race, a.date_naissance, a.pays_origine, c.id, c.superficie, c.capacite_max
                 FROM animal a
                 JOIN cage c ON a.id_cage = c.id
                 ORDER BY c.id, a.nom"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Aucun animal assigné à une cage.")

    # --- Opérations sur la table cage ---
    def add_cage(self):
        print("\n--- Ajouter une cage ---")
        try:
            superficie = int(input("Superficie de la cage : ").strip())
            capacite_max = int(input("Capacité maximale de la cage : ").strip())
        except ValueError:
            print("❌ Valeur numérique invalide.")
            return

        sql = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
        self.cursor.execute(sql, (superficie, capacite_max))
        self.conn.commit()
        print("➕ Cage ajoutée avec succès.")

    def update_cage(self):
        print("\n--- Modifier une cage ---")
        try:
            cage_id = int(input("Entrez l'ID de la cage à modifier : ").strip())
        except ValueError:
            print("❌ ID invalide.")
            return
        print("Entrez les nouvelles valeurs (laisser vide pour ne pas modifier) :")
        superficie_input = input("Nouvelle superficie : ").strip()
        capacite_input = input("Nouvelle capacité maximale : ").strip()

        updates = []
        params = []
        if superficie_input:
            try:
                superficie = int(superficie_input)
                updates.append("superficie = %s")
                params.append(superficie)
            except ValueError:
                print("❌ Superficie invalide.")
                return
        if capacite_input:
            try:
                capacite_max = int(capacite_input)
                updates.append("capacite_max = %s")
                params.append(capacite_max)
            except ValueError:
                print("❌ Capacité invalide.")
                return

        if not updates:
            print("Aucune modification saisie.")
            return

        sql = "UPDATE cage SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(cage_id)
        self.cursor.execute(sql, tuple(params))
        self.conn.commit()
        print("📝 Cage mise à jour.")

    def delete_cage(self):
        print("\n--- Supprimer une cage ---")
        try:
            cage_id = int(input("Entrez l'ID de la cage à supprimer : ").strip())
        except ValueError:
            print("❌ ID invalide.")
            return
        sql = "DELETE FROM cage WHERE id = %s"
        self.cursor.execute(sql, (cage_id,))
        self.conn.commit()
        print("🗑️ Cage supprimée.")

    def calculate_total_superficie(self):
        print("\n--- Calcul de la superficie totale de toutes les cages ---")
        sql = "SELECT SUM(superficie) FROM cage"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        total = result[0] if result[0] is not None else 0
        print(f"La superficie totale de toutes les cages est de : {total} m².")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        print("🔒 Connexion à la base de données fermée.")


def menu():
    zoo = ZooManagement()
    while True:
        print("\n===== Menu Gestion du Zoo =====")
        print("1. Ajouter un animal")
        print("2. Modifier un animal")
        print("3. Supprimer un animal")
        print("4. Afficher tous les animaux")
        print("5. Afficher les animaux assignés à une cage")
        print("6. Ajouter une cage")
        print("7. Modifier une cage")
        print("8. Supprimer une cage")
        print("9. Calculer la superficie totale des cages")
        print("10. Quitter")
        choix = input("Votre choix (1-10) : ").strip()

        if choix == "1":
            zoo.add_animal()
        elif choix == "2":
            zoo.update_animal()
        elif choix == "3":
            zoo.delete_animal()
        elif choix == "4":
            zoo.display_animals()
        elif choix == "5":
            zoo.display_animals_in_cages()
        elif choix == "6":
            zoo.add_cage()
        elif choix == "7":
            zoo.update_cage()
        elif choix == "8":
            zoo.delete_cage()
        elif choix == "9":
            zoo.calculate_total_superficie()
        elif choix == "10":
            zoo.close_connection()
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu()
