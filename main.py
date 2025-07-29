import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv


def adjust_brightness(hex_color, factor):
    """Retourne une couleur ajustée en fonction du facteur de luminosité."""
    hex_color = hex_color.lstrip('#')
    comps = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    def ajust(c):
        return int(c + (255 - c) * (factor - 1)) if factor >= 1 else int(c * factor)
    r, g, b = [ajust(c) for c in comps]
    return f"#{r:02x}{g:02x}{b:02x}"

# Fenêtre principale
root = tk.Tk()
root.title("WMS – Entrepôt Matériel Informatique ESTRALOPITECK v1")
root.geometry("1400x800")

# Titre
label_title = tk.Label(root, text="Entrepôt Matériel Informatique – ESTRALOPITECK", font=("Arial", 18, "bold"))
label_title.pack(pady=10)

# Barre d'actions
action_bar = tk.Frame(root)
button_help = tk.Button(action_bar, text="Aide", command=lambda: messagebox.showinfo("Aide", "Aide non implémentée"))
button_help.pack(side="right", padx=5)
button_ref = tk.Button(action_bar, text="Référence", command=lambda: messagebox.showinfo("Référence", "Référence non implémentée"))
button_ref.pack(side="right")
action_bar.pack(fill="x", padx=10)

# Onglets
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

tabs = {}
for name in ["Produit", "Fournisseur", "Journal", "Inventaire", "Étiquettes", "Emplacement", "Outils"]:
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=name)
    tabs[name] = frame

# --- Base functions (Produit, Fournisseur, Journal, Inventaire, Étiquettes) ---
# Produit
tab_prod = tabs["Produit"]
tk.Label(tab_prod, text="Module Produit", font=("Arial", 14)).pack(pady=10)
prod_ref = tk.Entry(tab_prod)
prod_ref.pack(fill="x", padx=10)
def search_product(): messagebox.showinfo("Recherche", f"Recherche produit : {prod_ref.get()}")
tk.Button(tab_prod, text="Rechercher", command=search_product).pack(pady=5)

# Fournisseur
tab_fourn = tabs["Fournisseur"]
tk.Label(tab_fourn, text="Module Fournisseur", font=("Arial", 14)).pack(pady=10)
fourn_name = tk.Entry(tab_fourn)
fourn_name.pack(fill="x", padx=10)
def add_supplier(): messagebox.showinfo("Fournisseur", f"Fournisseur ajouté : {fourn_name.get()}")
tk.Button(tab_fourn, text="Ajouter", command=add_supplier).pack(pady=5)

# Journal
tab_journal = tabs["Journal"]
tk.Label(tab_journal, text="Journal d'activité", font=("Arial", 14)).pack(pady=10)
journal_txt = tk.Text(tab_journal, height=20)
journal_txt.pack(fill="both", expand=True, padx=10, pady=5)
scroll_journal = ttk.Scrollbar(tab_journal, command=journal_txt.yview)
journal_txt.config(yscrollcommand=scroll_journal.set)
scroll_journal.pack(side="right", fill="y")

# Inventaire
tab_inv = tabs["Inventaire"]
tk.Label(tab_inv, text="Inventaire", font=("Arial", 14)).pack(pady=10)
cols = ("Réf", "Nom", "Quantité", "Emplacement")
tree = ttk.Treeview(tab_inv, columns=cols, show="headings")
for col in cols: tree.heading(col, text=col)
tree.pack(fill="both", expand=True, padx=10, pady=5)
def load_csv(path=None):
    """Charge un fichier CSV d'inventaire depuis le chemin spécifié ou par défaut."""
    tree.delete(*tree.get_children())
    file_path = path or 'inventory_hardware.csv'
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                tree.insert('', 'end', values=(row['Réf'], row['Nom'], row['Quantité'], row['Emplacement']))
    except FileNotFoundError:
        messagebox.showwarning("Fichier manquant", f"{file_path} non trouvé.")
# Chargement initial
load_csv()


# Étiquettes
tab_etq = tabs["Étiquettes"]
tk.Label(tab_etq, text="Étiquettes", font=("Arial", 14)).pack(pady=10)
tk.Button(tab_etq, text="Imprimer étiquette", command=lambda: messagebox.showinfo("Étiquette", "Impression... ")).pack(pady=5)

# --- Onglet Emplacement sans niveaux, 2 faces par rack, couleurs par rayon ---
tab_empl = tabs["Emplacement"]
emplacement_frame = tk.Frame(tab_empl)
emplacement_frame.pack(fill="both", expand=True)

# Canvas grille
grid_canvas = tk.Canvas(emplacement_frame, bg="white", width=700)
grid_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
rows, cols = 6, 4
cell_w, cell_h = 150, 90
spacing = 15
faces = ['A', 'B']
# Couleurs distinctes par rayon (6 tons)
row_colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33"]
face_factor = {'A': 1.2, 'B': 0.8}

def on_click(code):
    """Affiche un mini tableau des produits présents à l'emplacement code dans une fenêtre dédiée."""
    rows_data = [tree.item(i)['values'] for i in tree.get_children() if tree.item(i)['values'][3] == code]
    # Création de la fenêtre de détails
    detail_win = tk.Toplevel(root)
    detail_win.title(f"Détails Emplacement {code}")
    # En-têtes de colonnes
    headers = ["Réf", "Nom", "Quantité"]
    for j, h in enumerate(headers):
        tk.Label(detail_win, text=h, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padx=5, pady=2).grid(row=0, column=j, sticky="nsew")
    # Contenu des lignes
    if rows_data:
        for i, (ref, name, qty, loc) in enumerate(rows_data[:5], start=1):
            tk.Label(detail_win, text=ref, borderwidth=1, relief="solid", padx=5, pady=2).grid(row=i, column=0, sticky="nsew")
            tk.Label(detail_win, text=name, borderwidth=1, relief="solid", padx=5, pady=2).grid(row=i, column=1, sticky="nsew")
            tk.Label(detail_win, text=qty, borderwidth=1, relief="solid", padx=5, pady=2).grid(row=i, column=2, sticky="nsew")
    else:
        tk.Label(detail_win, text="Aucun produit", padx=10, pady=5).pack(padx=10, pady=10)
    # Ajuste la taille des colonnes
    for j in range(len(headers)):
        detail_win.grid_columnconfigure(j, weight=1)

for r in range(rows):
    y_offset = r * (cell_h + spacing) + 10
    base_color = row_colors[r]
    for c in range(cols):
        x_offset = c * (cell_w + 10) + 10
        for face in faces:
            y0 = y_offset + (faces.index(face)) * (cell_h/2)
            y1 = y0 + (cell_h/2)
            code = f"R{r+1}E{c+1}{face}"
            color = adjust_brightness(base_color, face_factor[face])
            grid_canvas.create_rectangle(x_offset, y0, x_offset+cell_w, y1, fill=color, outline='black', tags=code)
            grid_canvas.create_text(x_offset+5, y0+15, text=code, anchor='w', font=("Arial", 8))
            grid_canvas.tag_bind(code, '<Button-1>', lambda e, code=code: on_click(code))
        # contour global
        grid_canvas.create_rectangle(x_offset, y_offset, x_offset+cell_w, y_offset+cell_h, outline='black', width=2)

# Formulaire Emplacement
form = tk.Frame(emplacement_frame)
form.pack(side="left", fill="y", padx=20, pady=10)
entries = {}
for lbl in ["Rayon", "Étagère", "Face"]:
    tk.Label(form, text=lbl).pack(anchor='w')
    ent = tk.Entry(form)
    ent.pack(fill='x', pady=5)
    entries[lbl] = ent

def select_loc():
    vals = {k: v.get() for k,v in entries.items()}
    messagebox.showinfo("Sélection", f"Lieu: {vals}")
tk.Button(form, text="Sélectionner", command=select_loc).pack(fill='x', pady=5)

# --- Onglet Outils ---
tab_outils = tabs["Outils"]

def import_csv_ui():
    filetypes = [("CSV Files", "*.csv")]
    path = filedialog.askopenfilename(filetypes=filetypes)
    if path:
        load_csv(path)

button_import = tk.Button(tab_outils, text="Importer CSV", width=20, command=import_csv_ui)
button_import.pack(pady=5)
button_export = tk.Button(tab_outils, text="Exporter CSV", width=20, command=lambda: messagebox.showinfo("Export", "Export effectué"))
button_export.pack(pady=5)
button_export.pack(pady=5)

root.mainloop()
