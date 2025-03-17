import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")  # Forcer l'utilisation du backend TkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Liste des catégories prédéfinies
CATEGORIES = [
    "Électronique", "Vêtements", "Alimentation", "Maison & Déco",
    "Sport & Loisirs", "Jouets", "Beauté & Santé", "Livres & Papeterie"
]

# Connexion à la base de données MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pipes606&",
            database="store"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erreur", f"Connexion à la base de données échouée : {e}")
        return None

# Récupérer les produits
def fetch_products():
    conn = connect_to_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT product.id, product.name, product.price, product.quantity, category.name "
                   "FROM product "
                   "JOIN category ON product.id_category = category.id")
    products = cursor.fetchall()
    conn.close()
    return products

# Afficher les produits dans la table
def display_products():
    for row in tree.get_children():
        tree.delete(row)
    products = fetch_products()
    for product in products:
        tree.insert("", "end", values=product)

# Ajouter un produit
def add_product():
    name = entry_name.get().strip()
    description = entry_description.get().strip()
    price = entry_price.get().strip()
    quantity = entry_quantity.get().strip()
    category = combo_category.get()

    if not all([name, price, quantity, category]):
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")
        return

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showwarning("Erreur", "Prix doit être un nombre et Quantité un entier.")
        return

    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM category WHERE name = %s", (category,))
    result = cursor.fetchone()
    if result:
        category_id = result[0]
    else:
        messagebox.showerror("Erreur", "Catégorie non trouvée.")
        conn.close()
        return

    cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) "
                   "VALUES (%s, %s, %s, %s, %s)", 
                   (name, description, price, quantity, category_id))
    conn.commit()
    conn.close()
    display_products()
    clear_entries()

# Supprimer un produit
def delete_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un produit à supprimer.")
        return

    product_id = tree.item(selected_item)["values"][0]
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
    display_products()

# Mettre à jour un produit
def update_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un produit à mettre à jour.")
        return

    product_id = tree.item(selected_item)["values"][0]
    new_price = entry_price.get().strip()
    new_quantity = entry_quantity.get().strip()

    if not all([new_price, new_quantity]):
        messagebox.showwarning("Erreur", "Prix et Quantité sont requis pour la mise à jour.")
        return

    try:
        new_price = float(new_price)
        new_quantity = int(new_quantity)
    except ValueError:
        messagebox.showwarning("Erreur", "Prix doit être un nombre et Quantité un entier.")
        return

    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET price = %s, quantity = %s WHERE id = %s", 
                   (new_price, new_quantity, product_id))
    conn.commit()
    conn.close()
    display_products()
    clear_entries()

# Exporter les produits en CSV
def export_to_csv():
    products = fetch_products()
    if not products:
        messagebox.showwarning("Exportation", "Aucun produit à exporter.")
        return
    df = pd.DataFrame(products, columns=["ID", "Nom", "Prix", "Quantité", "Catégorie"])
    df.to_csv("products.csv", index=False)
    messagebox.showinfo("Exportation", "Les produits ont été exportés en fichier CSV.")

# Filtrer les produits par catégorie
def filter_by_category():
    selected_category = combo_category_filter.get()
    if not selected_category:
        display_products()  # Si aucune catégorie sélectionnée, afficher tous les produits
        return

    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT product.id, product.name, product.price, product.quantity, category.name "
                   "FROM product "
                   "JOIN category ON product.id_category = category.id "
                   "WHERE category.name = %s", (selected_category,))
    products = cursor.fetchall()
    conn.close()
    for row in tree.get_children():
        tree.delete(row)
    for product in products:
        tree.insert("", "end", values=product)

# Afficher le graphique
def display_graph():
    # Effacer le contenu précédent du frame graphique (sauf le bouton)
    for widget in graph_frame.winfo_children():
        if isinstance(widget, tk.Button):
            continue
        widget.destroy()

    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT category.name, SUM(product.quantity) "
                   "FROM product "
                   "JOIN category ON product.id_category = category.id "
                   "GROUP BY category.name")
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showwarning("Graphique", "Aucune donnée disponible pour le graphique.")
        return

    categories = [item[0] for item in data]
    quantities = [item[1] for item in data]

    # Créer une figure Matplotlib
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(categories, quantities, color="skyblue")
    ax.set_xlabel("Catégories")
    ax.set_ylabel("Quantité Totale")
    ax.set_title("Quantité Totale par Catégorie")
    fig.autofmt_xdate(rotation=45)  # Rotation des étiquettes

    # Intégrer le graphique dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Effacer les champs d'entrée
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    combo_category.set("")

# Interface graphique Tkinter
root = tk.Tk()
root.title("Gestion des Stocks")
root.geometry("900x700")

# Frame pour les entrées
frame_entry = tk.LabelFrame(root, text="Ajouter ou Modifier un Produit", padx=10, pady=10)
frame_entry.pack(padx=10, pady=5, fill="x")

tk.Label(frame_entry, text="Nom").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_entry, width=25)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Description").grid(row=1, column=0, padx=5, pady=5)
entry_description = tk.Entry(frame_entry, width=25)
entry_description.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Prix").grid(row=2, column=0, padx=5, pady=5)
entry_price = tk.Entry(frame_entry, width=25)
entry_price.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Quantité").grid(row=3, column=0, padx=5, pady=5)
entry_quantity = tk.Entry(frame_entry, width=25)
entry_quantity.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Catégorie").grid(row=4, column=0, padx=5, pady=5)
combo_category = ttk.Combobox(frame_entry, values=CATEGORIES, width=22)
combo_category.grid(row=4, column=1, padx=5, pady=5)

# Frame pour les boutons
frame_buttons = tk.Frame(root)
frame_buttons.pack(padx=10, pady=5)

tk.Button(frame_buttons, text="Ajouter", command=add_product, bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Mettre à jour", command=update_product, bg="orange", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Supprimer", command=delete_product, bg="red", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Exporter en CSV", command=export_to_csv).grid(row=0, column=3, padx=5)

# Frame pour le filtre
frame_filter = tk.LabelFrame(root, text="Filtrer par Catégorie", padx=10, pady=10)
frame_filter.pack(padx=10, pady=5, fill="x")

combo_category_filter = ttk.Combobox(frame_filter, values=[""] + CATEGORIES, width=22)
combo_category_filter.grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_filter, text="Filtrer", command=filter_by_category).grid(row=0, column=1, padx=5)

# Frame pour la liste des produits
frame_tree = tk.Frame(root)
frame_tree.pack(padx=10, pady=5, fill="both", expand=True)

columns = ("ID", "Nom", "Prix", "Quantité", "Catégorie")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# Frame pour le graphique
graph_frame = tk.LabelFrame(root, text="Graphique des Quantités", padx=10, pady=10)
graph_frame.pack(padx=10, pady=5, fill="both", expand=True)

tk.Button(graph_frame, text="Afficher Graphique", command=display_graph).pack(pady=5)

# Afficher les produits au démarrage
display_products()

# Lancer l'interface
root.mainloop()