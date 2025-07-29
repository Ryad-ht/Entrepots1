import tkinter as tk
from tkinter import ttk

def adjust_brightness(hex_color, factor):
    """Adapte la luminosité d'une couleur hex (factor >1 = éclaircir, <1 = assombrir)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    def adjust(c):
        if factor >= 1:
            return int(c + (255 - c) * (factor - 1))
        else:
            return int(c * factor)
    return f"#{adjust(r):02x}{adjust(g):02x}{adjust(b):02x}"

root = tk.Tk()
root.title("WMS - Emplacement")
root.geometry("1000x800")

# Titre
tk.Label(
    root,
    text="Entrepôt de stockage de ESTRALOPITECK",
    font=("Arial", 18, "bold")
).pack(pady=10)

# Onglets
notebook = ttk.Notebook(root)
for name in ["Produit", "Fournisseur", "Journal", "Inventaire", "Étiquettes", "Emplacement", "Outils"]:
    notebook.add(ttk.Frame(notebook), text=name)
notebook.pack(fill="x", padx=10)

# Boutons Aide / Référence
top_frame = tk.Frame(root)
tk.Button(top_frame, text="Aide").pack(side="right", padx=5)
tk.Button(top_frame, text="Référence").pack(side="right")
top_frame.pack(fill="x", pady=5, padx=10)

# Contenu principal
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Canvas pour l'aperçu du magasin
canvas = tk.Canvas(main_frame, bg="white")
canvas.pack(side="left", fill="both", expand=True)

rows, cols = 6, 4
cell_w, cell_h = 150, 90
couloir_spacing = 15  # espacement entre chaque ligne
base_colors = ["#ff6666", "#66ff66", "#6666ff", "#ffcc66"]  # 4 couleurs, une par colonne
contrast = {1: 1.2, 2: 1.0, 3: 0.8}  # niveaux clair, moyen, sombre

for r in range(rows):
    for c in range(cols):
        x0 = c * cell_w + 10
        # On décale chaque ligne r par r * couloir_spacing
        y0 = r * cell_h + 10 + r * couloir_spacing
        band_h = cell_h / 3
        base = base_colors[c]  # couleur selon la colonne
        for lvl in range(1, 4):
            y_start = y0 + (lvl - 1) * band_h
            y_end   = y_start + band_h
            color = adjust_brightness(base, contrast[lvl])
            canvas.create_rectangle(
                x0, y_start, x0 + cell_w, y_end,
                fill=color, outline="grey"
            )
            # Indication du niveau
            canvas.create_text(
                x0 + 5, y_start + band_h / 2,
                text=f"N{lvl}", anchor="w", font=("Arial", 8)
            )
        # contour global de la case
        canvas.create_rectangle(
            x0, y0, x0 + cell_w, y0 + cell_h,
            outline="black", width=2
        )

# Formulaire à droite
form = tk.Frame(main_frame)
form.pack(side="right", fill="y", padx=20)
for label in ["Ranger", "Rack", "Niveau", "Position"]:
    tk.Label(form, text=label).pack(anchor="w")
    tk.Entry(form).pack(fill="x", pady=5)
for btn in ["Sélectionner", "Export Palettes", "Entrée", "Sortie", "En cours", "Clôture"]:
    tk.Button(form, text=btn, width=20).pack(pady=5)

root.mainloop()
