# # WMS – Gestion d’Emplacements (v1)

**Version :** 1.0  
**Date :** 29 juillet 2025  

## Description

Ce projet est une première version d’une interface graphique légère de Warehouse Management System (WMS) développée en Python (Tkinter). Elle permet de visualiser et de gérer les emplacements d’un entrepôt sur une vue en grille, de saisir et de filtrer les informations de rangement, et d’accéder rapidement aux modules clés d’un WMS.

## Fonctionnalités

- **Onglets de navigation**  
  - Produit, Fournisseur, Journal, Inventaire, Étiquettes, Emplacement, Outils  
- **Barre d’actions** en haut à droite  
  - Boutons **Aide** et **Référence**  
- **Formulaire de saisie**  
  - Champs : Ranger, Rack, Niveau, Position  
  - Boutons : Sélectionner, Export Palettes, Entrée, Sortie, En cours, Clôture  
- **Aperçu visuel de l’entrepôt**  
  - Grille 6 lignes × 4 colonnes  
  - Chaque case subdivisée en 3 bandes (Niveaux 1–3)  
  - Couleurs dynamiques par colonne et dégradé de contraste clair–sombre par niveau  
  - Espacement “couloir” entre chaque ligne pour simuler les allées  
- **Titre personnalisable**  
  - Entrepôt de stockage de **ESTRALOPITECK**

## Technologies

- **Langage :** Python 3  
- **Bibliothèque UI :** Tkinter (inclus dans la bibliothèque standard)  
- **Organisation :** fichier unique `main.py` (ou module équivalent)

## Installation

1. Cloner ce dépôt :  
   ```bash
   git clone https://github.com/votre-organisation/wms-emplacement.git
   cd wms-emplacement

