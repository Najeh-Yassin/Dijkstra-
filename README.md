# 🚗 Optimisation de Trajets Dijkstra — Réseau Routier de Tanger (Maroc)

Projet universitaire avancé implémentant l'algorithme de **Dijkstra** sur un graphe routier réel extrait d'OpenStreetMap (OSM) pour la ville de Tanger. Le système propose une navigation multicritère avec des sorties visuelles et analytiques de haute précision.

---

## 📋 Description du Projet

L'application calcule l'itinéraire optimal entre plus de **60 points d'intérêt (POI)** à Tanger (Médina, Gares, Aéroport, Malls, Universités). Elle se distingue par sa capacité à modéliser le réseau urbain réel et à proposer des visualisations interactives modernes.

### 🧠 Cœur Algorithmique
- **Algorithme de Dijkstra** : Implémenté avec un **tas binaire (priority queue)** pour une complexité optimale en $O(E \log V)$.
- **Pondération Multicritère** : Calcul du coût basé sur une fonction composite :
  $$W = \alpha \cdot \text{distance} + \beta \cdot \text{temps} + \gamma \cdot \text{coût}$$
- **Heuristiques de Géomatique** : Utilisation de la distance de **Haversine** pour la recherche spatiale.

---

## ✨ Fonctionnalités Avancées

| Fonctionnalité | Description |
| :--- | :--- |
| **Carte Interactive (Folium)** | Visualisation Web avec **AntPath** (animation du tracé), fond Satellite Esri, et panneau d'info flottant. |
| **Analyse Dynamique** | Liste défilante (Scroll List) des rues traversées et popups d'étapes enrichies. |
| **Graphes Analytiques** | Génération de graphes théoriques avec **NetworkX** (layout Kamada-Kawai) étiquetant POIs et distances. |
| **Rapports JSON Structurés** | Export complet incluant métadonnées, IDs de nœuds, rues et coordonnées GPS. |
| **Études Statistiques** | Génération automatique de matrices de distances (Heatmap) et histogrammes de distribution. |
| **Validation du Graphe** | Outils de diagnostic pour détecter les nœuds isolés ou les segments sans poids. |

---

## 🛠️ Prérequis & Installation

### Configuration Requise
- **Python 3.9+**
- Connexion internet (pour le chargement initial de la carte via OSMnx)

### Dépendances
```bash
pip install -r requirements.txt
```

*Contenu recommandé pour `requirements.txt` :*
```text
osmnx>=1.3.0
networkx>=3.0
folium>=0.14.0
matplotlib>=3.6.0
numpy>=1.23.0
branca>=0.6.0
pandas
seaborn
```

---

## 🚀 Utilisation

```bash
python versionfin.py
```

1.  **Phase de Chargement** : L'application télécharge le réseau de Tanger et prépare les poids.
2.  **Menu Interactif** :
    -   **Option 1** : Choisir un trajet manuel, le critère d'optimisation (Distance, Temps, Coût), et générer la carte.
    -   **Option 2** : Lancer un mode test batch pour générer 10 trajets de référence.
    -   **Option 3/4** : Générer les visuels pour le rapport académique (Graphes théoriques et Heatmaps).

---

## 📂 Structure du Projet

```text
struct_Project/
├── versionfin.py           # Noyau algorithmique et interface principale
├── config.py               # Paramètres de pondération et constantes
├── requirements.txt        # Dépendances Python
├── cache/                  # Cache local des données OSMnx
├── reports/                # Dossier recommandé pour les sorties
│   ├── rapport_*.json      # Rapports détaillés (JSON)
│   ├── web_carte_*.html    # Cartes interactives animées
│   ├── graphe_chemin_*.png # Visualisation théorique du chemin
│   └── rapport_matrice.png # Matrice de distances du réseau
└── dijkstra_router.log     # Journalisation des événements
```

---

## ⚙️ Détails Techniques de la Visualisation

### Carte Web Web (HTML)
La méthode `visualiser_chemin_web` intègre un système de **template Jinja2/HTML** pour afficher :
-   Le nom de la rue actuelle ou du POI le plus proche.
-   La distance cumulée en kilomètres depuis le départ.
-   Une animation de type "AntPath" pour indiquer clairement le sens de circulation.

### Graphe de Rapport (PNG)
Le graphe analytique n'est pas une simple carte mais une représentation mathématique où :
-   **Vert** : Point de départ.
-   **Rouge** : Destination finale.
-   **Orange** : Intersections clés nommées.
-   **Labels bleus** : Poids précis de chaque segment sur l'arête.

---

## 🎓 Contexte
Projet réalisé dans le cadre du module **Analytique des Données – Structures Avancées**. 
*Focus : Structures de données de type Graphe et optimisation algorithmique.*

---
**Auteurs :** [Najeh Yassin](https://github.com/Najeh-Yassin) & Équipe Dijkstra Tanger.
