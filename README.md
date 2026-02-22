# 🚗 Projet Algorithme de Dijkstra – Tanger (Professional Edition)

Ce projet implémente les algorithmes **Dijkstra** et **A\*** pour trouver les itinéraires optimaux dans la ville de Tanger, Maroc, en utilisant des données routières réelles via OpenStreetMap.

---

## 📋 Description

L'application calcule le meilleur trajet entre deux points d'intérêt à Tanger selon plusieurs critères (distance, temps, coût). Elle utilise des graphes pondérés construits à partir de données géographiques réelles et offre une interface en ligne de commande professionnelle.

---

## ✨ Fonctionnalités

| Fonctionnalité | Détail |
|---|---|
| **Dijkstra** | Algorithme classique garanti optimal – O(E log V) |
| **A\*** | Algorithme heuristique (Haversine), 2–5× plus rapide que Dijkstra |
| **Multi-critères** | Optimisation selon la distance, le temps, le coût ou un mode mixte |
| **60+ Points d'intérêt** | Gares, aéroport, médina, plages, universités, hôpitaux… |
| **Détection de POIs** | Points d'intérêt traversés détectés avec rayon configurable |
| **Mode Interactif** | Choix manuel du départ, de l'arrivée, du critère et de l'algorithme |
| **Mode Batch** | 10 trajets automatiques avec barre de progression `tqdm` |
| **Carte HTML interactive** | Folium avec tile switcher, minimap, fullscreen, panneau d'info |
| **Image PNG** | Carte statique pour rapports Word/PDF |
| **Export JSON** | Résultats détaillés par trajet et rapport complet batch |
| **Export CSV** | Tableau récapitulatif par trajet |
| **Matrice de distances** | Heatmap seaborn entre 4 lieux clés |
| **Histogramme** | Distribution des temps de trajet sur 20 trajets aléatoires |
| **Logging** | Console + fichier `dijkstra_router.log` |
| **Configuration centralisée** | Tous les paramètres dans `config.py` |
| **Cache LRU** | Accélération des recherches de nœuds proches |

---

## 🛠️ Prérequis

Python 3.9+ et les bibliothèques suivantes :

```bash
pip install -r requirements.txt
```

Contenu de `requirements.txt` :

```
osmnx>=1.3.0
networkx>=3.0
folium>=0.14.0
matplotlib>=3.6.0
numpy>=1.23.0
tqdm>=4.65.0
seaborn>=0.12.0
```

> `seaborn` et `tqdm` sont optionnels mais fortement recommandés.

---

## 🚀 Installation et Exécution

```bash
# 1. Cloner le dépôt
git clone https://github.com/Najeh-Yassin/Dijkstra-.git
cd Dijkstra-

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python versionfin.py
```

---

## 📂 Structure du Projet

```
struct_Project/
├── versionfin.py          # Script principal (router + UI)
├── config.py              # Configuration centralisée (paramètres)
├── requirements.txt       # Dépendances Python
├── README.md              # Documentation
├── dijkstra_router.log    # Fichier de logs (généré à l'exécution)
├── cache/                 # Cache OSMnx (généré automatiquement)
├── resultat_*.json        # Résultats JSON par trajet
├── resultat_*.csv         # Résultats CSV par trajet
├── rapport_complet_*.json # Rapport batch complet
├── web_carte_*.html       # Cartes interactives Folium
├── rapport_trajet_*.png   # Cartes statiques PNG
├── rapport_matrice.png    # Heatmap matrice de distances
└── rapport_histogramme.png# Histogramme des temps de trajet
```

---

## ⚙️ Configuration (`config.py`)

Tous les paramètres sont centralisés dans [`config.py`](config.py) :

```python
DEFAULT_SPEED_KMH = 45.0      # Vitesse moyenne urbaine
FUEL_COST_PER_KM  = 1.8       # Coût carburant (DH/km)
DEFAULT_DETECTION_RADIUS_M = 200  # Rayon détection POIs (m)
ROUTE_COLOR = "#1a73e8"        # Couleur de l'itinéraire sur la carte
LOG_LEVEL   = "INFO"           # Niveau de log
```

---

## 🗺️ Carte Interactive HTML

La carte générée inclut :
- **3 fonds de carte** : OpenStreetMap, CartoDB Positron, Satellite (Esri)
- **Minimap** en bas à droite
- **Bouton plein écran**
- **Panneau d'information** flottant (distance, temps, coût, algorithme)
- **Marqueurs animés** départ (vert) / arrivée (rouge)
- **Cercles orange** pour chaque POI traversé avec popup détaillé
- **Contrôle des couches** pour afficher/masquer les POIs

---

## 🔬 Algorithmes

### Dijkstra
- Garantit le chemin optimal
- Explore tous les nœuds accessibles jusqu'à la destination
- Complexité : **O(E log V)**

### A* (recommandé)
- Utilise une heuristique Haversine pour guider la recherche
- Explore moins de nœuds → **2–5× plus rapide** en pratique
- Même qualité de résultat sur les graphes routiers

### Poids composite
```
w = α·distance + β·temps·3600 + γ·coût·100
```
Les coefficients α, β, γ sont ajustés selon le critère choisi.

---

## 📝 Auteur

Projet réalisé dans le cadre du module **Analytique des Données – Structures Avancées**.
