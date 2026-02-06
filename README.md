# 🚗 Projet Algorithme de Dijkstra - Tanger

Ce projet implémente l'algorithme de Dijkstra pour trouver les itinéraires optimaux dans la ville de Tanger, Maroc, en utilisant des données routières réelles via OpenStreetMap.

## 📋 Description

L'application permet de calculer le meilleur trajet entre deux points d'intérêt à Tanger selon plusieurs critères (distance, temps, coût). Elle utilise des graphes pondérés construits à partir de données géographiques réelles.

## ✨ Fonctionnalités

- **Calcul d'itinéraires optimaux** : Utilisation de l'algorithme de Dijkstra.
- **Multi-critères** : Optimisation selon la distance, le temps estimé ou le coût (carburant).
- **Points d'intérêt prédéfinis** : Gares, aéroports, lieux touristiques, centres commerciaux, etc.
- **Mode Interactif** : Choix manuel des points de départ et d'arrivée.
- **Mode Test (Batch)** : Génération automatique de rapports sur plusieurs trajets.
- **Visualisation** :
  - Génération de cartes interactives HTML (`folium`).
  - Génération de graphiques statiques PNG (`matplotlib`).
- **Analyse de données** : Matrices de distances et histogrammes de temps de trajet.

## 🛠️ Prérequis

Le projet nécessite Python 3.x et les bibliothèques suivantes :

```bash
pip install osmnx networkx folium matplotlib numpy
```

*(Note: `seaborn` est optionnel pour des graphiques plus esthétiques)*

## 🚀 Installation et Exécution

1.  Clonez ce dépôt :
    ```bash
    git clone https://github.com/Najeh-Yassin/Dijkstra-.git
    cd Dijkstra-
    ```

2.  Installez les dépendances nécessaires.

3.  Lancez l'application :
    ```bash
    python versionfin.py
    ```

## 📂 Structure du Projet

- `versionfin.py` : Script principal contenant la logique de l'algorithme, la classe `DijkstraRouterTanger` et l'interface utilisateur.
- `cache/` : Dossier généré pour le cache des données cartographiques OSM.
- `*.json` : Fichiers de résultats générés (sauvegardes automatiques).
- `*.png` / `*.html` : Cartes et graphiques générés.

## 📝 Auteur

Projet réalisé dans le cadre du module Analytique des Données - Structures Avancées.
