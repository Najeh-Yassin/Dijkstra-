import osmnx as ox
import networkx as nx
import folium
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from math import radians, sin, cos, sqrt, atan2
import numpy as np
from typing import List, Tuple, Dict, Optional, Set
import time
from dataclasses import dataclass
import json
import random

# Configuration globale
ox.settings.use_cache = True
ox.settings.log_console = False
ox.settings.timeout = 300

@dataclass
class CheminResultats:
    """Structure de données pour stocker les résultats d'un calcul."""
    chemin: List[int]
    distance_totale: float
    temps_total: float
    cout_total: float
    poids_total: float
    nœuds_visites: int
    temps_calcul: float
    points_coordonnees: List[Tuple[float, float]]

class DijkstraRouterTanger:
    """
    Routeur optimisé pour Tanger.
    Implémente Dijkstra sur graphe réel avec pondération multicritère.
    """
    
    # Base de données des lieux importants de Tanger
    POINTS_INTERET = {
        # --- 🚆 TRANSPORT & ENTRÉES VILLE ---
        "Gare Tanger Ville (TGV)": (35.7730, -5.8139),
        "Gare Tanger Morora": (35.7485, -5.8298),
        "Aéroport Ibn Battouta": (35.7269, -5.9169),
        "Port de Tanger Ville (Ferry)": (35.7905, -5.8085),
        "Gare Routière (Nouvelle)": (35.7382, -5.8545),
        "Entrée Autoroute Tanger-Rabat": (35.7250, -5.8450),

        # --- 🕌 MÉDINA & CENTRE HISTORIQUE ---
        "Grand Socco (Place 9 Avril)": (35.7867, -5.8125),
        "Petit Socco": (35.7858, -5.8081),
        "Kasbah (Musée)": (35.7839, -5.8119),
        "Tombeaux des Phéniciens": (35.7915, -5.8205),
        "Légation Américaine": (35.7850, -5.8113),
        "Bab Fahs": (35.7865, -5.8122),
        "Cinéma Rif": (35.7842, -5.8129),
        "Hôtel Continental": (35.7885, -5.8095),

        # --- 🏙️ CENTRE VILLE (VILLE NOUVELLE) ---
        "Place de France": (35.7815, -5.8135),
        "Boulevard Pasteur": (35.7805, -5.8140),
        "Place des Nations": (35.7755, -5.8165),
        "Place du Koweit (Iberia)": (35.7780, -5.8220),
        "Rond-Point Riad Tétouan": (35.7685, -5.8180),
        "Grande Poste": (35.7790, -5.8150),
        "Hôtel El Minzah": (35.7820, -5.8130),
        "Consulat d'Espagne": (35.7760, -5.8220),

        # --- 🌊 CÔTE, PLAGES & NATURE ---
        "Marina Bay": (35.7850, -5.8050),
        "Plage Municipale (Corniche)": (35.7766, -5.8040),
        "Malabata (Mövenpick/Casino)": (35.7800, -5.7900),
        "Cap Spartel (Phare)": (35.7922, -5.9225),
        "Grottes d'Hercule": (35.7592, -5.9392),
        "Parc Perdicaris (Rmilat)": (35.7950, -5.8500),
        "Café Hafa": (35.7909, -5.8217),
        "Achakar Beach": (35.7650, -5.9350),
        "Forêt Diplomatique": (35.6800, -5.9500),

        # --- 🛍️ SHOPPING & COMMERCE ---
        "Tanger City Mall": (35.7733, -5.8134),
        "Socco Alto Mall": (35.7688, -5.8427),
        "Ibn Batouta Mall": (35.7795, -5.8145),
        "Marjane Route de Tétouan": (35.7410, -5.8150),
        "Atacadao (Sidi Driss)": (35.7350, -5.8250),
        "Marché Central": (35.7710, -5.8210),
        "Casabarata (Marché aux puces)": (35.7550, -5.8250),

        # --- 🎓 ÉDUCATION & UNIVERSITÉS ---
        "Rectorat UAE": (35.7327, -5.8818),
        "FST Tanger (Boukhalef)": (35.7350, -5.8900),
        "ENCG Tanger": (35.7600, -5.8600),
        "ENSAT (École des Sciences Appliquées)": (35.7300, -5.8950),
        "Lycée Regnault": (35.7785, -5.8200),
        "American School of Tangier": (35.7790, -5.8350),

        # --- 🏥 SANTÉ & ADMINISTRATION ---
        "Hôpital Mohammed V": (35.7750, -5.8350),
        "Hôpital Ibn Rochd": (35.7680, -5.8320),
        "Wilaya de Tanger": (35.7655, -5.8280),
        "Tribunal de Première Instance": (35.7640, -5.8300),
        "Clinique du Détroit": (35.7630, -5.8390),

        # --- 🏟️ SPORT & LOISIRS ---
        "Grand Stade Ibn Batouta": (35.7483, -5.8775),
        "Village Sportif (Ziaten)": (35.7520, -5.8750),
        "Royal Golf de Tanger": (35.7650, -5.8550),
        "Club de Tir (Route de Rabat)": (35.7300, -5.8600),
        "Plaza de Toros (Arènes)": (35.7645, -5.8155),

        # --- 🏘️ QUARTIERS POPULAIRES & PÉRIPHÉRIE ---
        "Beni Makada": (35.7500, -5.8100),
        "Sidi Driss": (35.7450, -5.8200),
        "Dradeb": (35.7850, -5.8250),
        "Mesnana": (35.7400, -5.8800),
        "Gzenaya (Zone Franche)": (35.7100, -5.9200),
        "Val Fleuri": (35.7700, -5.8300),
        "California (Quartier résidentiel)": (35.7750, -5.8450)
    }

    def __init__(self, network_type: str = 'drive'):
        self.ville = "Tanger, Morocco"
        self.network_type = network_type
        self.vitesse_moyenne = 45.0  # km/h
        self.cout_par_km = 1.8  # DH/km
        
        # Pondérations par défaut
        self.alpha = 1.0   # distance
        self.beta = 0.5    # temps
        self.gamma = 0.3   # coût
        
        self.G = None
        self.noeuds_coords = None
    
    def charger_carte(self):
        """Charge le graphe routier depuis OpenStreetMap."""
        print(f"\n📡 Connexion aux serveurs OSM pour {self.ville}...")
        try:
            self.G = ox.graph_from_place(self.ville, network_type=self.network_type, simplify=True)
            if self.G is None or len(self.G.nodes) == 0: raise ValueError("Carte vide reçue")
            print(f"✅ Carte téléchargée avec succès")
            self._preparer_coordonnees()
            self._calculer_attributs_aretes()
            return True
        except Exception as e:
            print(f"❌ Erreur critique de chargement: {str(e)}")
            return False
            
    def valider_graphe(self):
        """Vérifie la cohérence du graphe chargé (Méthodologie)."""
        print("\n🔍 VALIDATION DU GRAPHE")
        print("-" * 40)
        problemes = []
        
        isolés = [n for n in self.G.nodes() if self.G.degree(n) == 0]
        if isolés: problemes.append(f"{len(isolés)} nœuds isolés détectés")
        
        sans_poids = sum(1 for u, v, d in self.G.edges(data=True) if 'poids_custom' not in d)
        if sans_poids > 0: problemes.append(f"{sans_poids} arêtes sans poids")
        
        if problemes:
            print("⚠️  Problèmes détectés:")
            for p in problemes: print(f"   • {p}")
        else:
            print(f"✅ Graphe validé: {len(self.G.nodes())} nœuds, {len(self.G.edges())} arêtes")
        print("-" * 40)
        return len(problemes) == 0
    
    def _preparer_coordonnees(self):
        self.noeuds_coords = {n: (d['y'], d['x']) for n, d in self.G.nodes(data=True) if 'y' in d}
    
    def _calculer_attributs_aretes(self):
        """Enrichit les arêtes avec Distance, Temps et Coût."""
        print("📊 Calcul des poids des segments routiers...")
        for u, v, key, data in self.G.edges(keys=True, data=True):
            distance = data.get('length', 100)
            if 'length' not in data and u in self.noeuds_coords and v in self.noeuds_coords:
                distance = self._haversine_distance(*self.noeuds_coords[u], *self.noeuds_coords[v]) * 1000
            
            temps = (distance / 1000) / self.vitesse_moyenne
            cout = (distance / 1000) * self.cout_par_km
            
            data.update({'distance': distance, 'temps': temps, 'cout': cout})
            # Poids composite pour Dijkstra
            data['poids_custom'] = (self.alpha * distance + self.beta * temps * 3600 + self.gamma * cout * 100)
            data['weight'] = data['poids_custom']
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Formule mathématique pour la distance GPS."""
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2)**2
        return R * 2 * atan2(sqrt(a), sqrt(1-a))
    
    def trouver_noeuds_proches(self, point, k=3):
        """Trouve le nœud du graphe le plus proche d'une coordonnée GPS."""
        lat_p, lon_p = point
        dists = [(self._haversine_distance(lat_p, lon_p, lat_n, lon_n), nid) 
                 for nid, (lat_n, lon_n) in self.noeuds_coords.items()]
        dists.sort()
        return [(nid, d) for d, nid in dists[:k]]
    
    def ajuster_coefficients(self, critere):
        """Modifie les poids selon le choix de l'utilisateur."""
        if critere == 'distance': self.alpha, self.beta, self.gamma = 1.0, 0.0, 0.0
        elif critere == 'temps': self.alpha, self.beta, self.gamma = 0.0, 1.0, 0.0
        elif critere == 'cout': self.alpha, self.beta, self.gamma = 0.0, 0.0, 1.0
        else: self.alpha, self.beta, self.gamma = 0.5, 0.3, 0.2
        self._calculer_attributs_aretes()
    
    def dijkstra(self, start_node, end_node):
        """
        Implémente l'algorithme de Dijkstra optimisé avec tas binaire (heapq).
        Complexité: O(E log V)
        """
        start_time = time.time()
        
        dist = {node: float('inf') for node in self.G.nodes()}
        precedent = {node: None for node in self.G.nodes()}
        visited = set()
        
        dist[start_node] = 0
        heap = [(0, start_node)] # (coût, nœud)
        n_visites = 0
        
        while heap:
            d, u = heappop(heap)
            
            if u in visited: continue
            visited.add(u)
            n_visites += 1
            
            if u == end_node: break # Cible atteinte
            
            for v in self.G.neighbors(u):
                if v in visited: continue
                # Trouver l'arête la moins chère (cas des MultiGraphes)
                min_w = min(d.get('poids_custom', d.get('length', 100)) for d in self.G[u][v].values())
                
                # Relâchement
                if dist[u] + min_w < dist[v]:
                    dist[v] = dist[u] + min_w
                    precedent[v] = u
                    heappush(heap, (dist[v], v))
        
        if precedent[end_node] is None: return None
            
        # Reconstruction du chemin
        chemin = []
        curr = end_node
        while curr:
            chemin.append(curr)
            curr = precedent[curr]
        chemin.reverse()
        
        metrics = self._calculer_metriques_chemin(chemin)
        return CheminResultats(
            chemin, metrics['distance_totale'], metrics['temps_total'],
            metrics['cout_total'], dist[end_node], n_visites,
            time.time() - start_time, metrics['points_coords']
        )
    
    def _calculer_metriques_chemin(self, chemin):
        d_tot, t_tot, c_tot, coords = 0, 0, 0, []
        for i in range(len(chemin) - 1):
            u, v = chemin[i], chemin[i+1]
            if u in self.noeuds_coords: coords.append(self.noeuds_coords[u])
            edge = min(self.G[u][v].values(), key=lambda x: x.get('poids_custom', 0))
            d_tot += edge.get('distance', 0)
            t_tot += edge.get('temps', 0)
            c_tot += edge.get('cout', 0)
        if chemin and chemin[-1] in self.noeuds_coords: coords.append(self.noeuds_coords[chemin[-1]])
        return {'distance_totale': d_tot, 'temps_total': t_tot, 'cout_total': c_tot, 'points_coords': coords}

    def trouver_chemin_optimal(self, p_dep, p_arr, critere='mixte'):
        self.ajuster_coefficients(critere)
        try:
            n1 = self.trouver_noeuds_proches(p_dep)[0][0]
            n2 = self.trouver_noeuds_proches(p_arr)[0][0]
            return self.dijkstra(n1, n2)
        except Exception as e:
            return None

    def _recuperer_noms_rues(self, chemin):
        noms, last = [], ""
        for i in range(len(chemin) - 1):
            u, v = chemin[i], chemin[i+1]
            if u in self.G and v in self.G[u]:
                data = list(self.G[u][v].values())[0]
                nom = data.get('name', 'Rue inconnue')
                if isinstance(nom, list): nom = nom[0]
                if nom and nom != "Rue inconnue" and nom != last:
                    noms.append(nom)
                    last = nom
        return noms

    def afficher_resultats(self, res, n_dep, n_arr, critere, sauvegarder=False):
        """Version avec option de sauvegarde automatique."""
        print("\n" + "="*60 + "\n📊 RÉSULTATS DÉTAILLÉS\n" + "="*60)
        if not res: 
            print("❌ Aucun itinéraire trouvé."); return
            
        rues = self._recuperer_noms_rues(res.chemin)
        
        # Affichage
        print(f"🚩 DÉPART  : {n_dep}")
        print(f"⬇️  Via {len(rues)} axes routiers")
        
        print("\n📍 RUES TRAVERSÉES (Détail complet) :")
        if len(rues) > 0:
            for r in rues: 
                print(f"   • {r}")
        else:
            print("   (Aucun nom de rue disponible)")
            
        print(f"\n🔗 Nœuds traversés (IDs) : {', '.join(map(str, res.chemin))}")
        
        print(f"\n🏁 ARRIVÉE : {n_arr}")
        
        print("-" * 60)
        print(f"📏 Distance totale : {res.distance_totale/1000:.2f} km")
        print(f"⏱️  Temps estimé    : {res.temps_total*60:.1f} min")
        print(f"💰 Coût carburant  : {res.cout_total:.2f} DH")
        print(f"🧮 Étapes (nœuds)  : {len(res.chemin)}")
        print(f"🔍 Nœuds explorés  : {res.nœuds_visites}")
        print(f"⚡ Temps calcul    : {res.temps_calcul*1000:.1f} ms")
        
        # Indicateurs de performance
        vitesse_moy = (res.distance_totale/1000) / res.temps_total if res.temps_total > 0 else 0
        print(f"🚗 Vitesse moyenne : {vitesse_moy:.1f} km/h")
        print("="*60)
        
        # Sauvegarde optionnelle
        if sauvegarder:
            data = {
                "trajet": {"depart": n_dep, "arrivee": n_arr, "critere": critere},
                "resultats": {
                    "distance_km": round(res.distance_totale/1000, 2),
                    "temps_min": round(res.temps_total*60, 1),
                    "cout_dh": round(res.cout_total, 2),
                    "vitesse_kmh": round(vitesse_moy, 1),
                    "etapes": len(res.chemin),
                    "rues": rues[:10]  # Premières 10 rues
                }
            }
            fn = f"resultat_{int(time.time())}.json"
            with open(fn, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Résultat sauvegardé: {fn}")

    # --- FONCTIONS POUR LE RAPPORT ---

    def afficher_statistiques_graphe(self):
        """Version enrichie des statistiques pour le rapport."""
        print("\n📊 STATISTIQUES DÉTAILLÉES DU RÉSEAU")
        print("="*60)
        
        nb_n, nb_e = len(self.G.nodes()), len(self.G.edges())
        degres = [d for n, d in self.G.degree()]
        dists = [d.get('distance', 0)/1000 for u, v, d in self.G.edges(data=True)]
        
        # 1. Structure
        print("\n🔹 STRUCTURE DU GRAPHE:")
        print(f"  • Nœuds (intersections)    : {nb_n:,}")
        print(f"  • Arêtes (segments routes) : {nb_e:,}")
        print(f"  • Type                     : MultiDiGraph orienté pondéré")
        
        # 2. Connectivité
        print(f"\n🔹 CONNECTIVITÉ:")
        print(f"  • Degré moyen              : {sum(degres)/len(degres):.2f}")
        print(f"  • Degré minimum            : {min(degres)}")
        print(f"  • Degré maximum            : {max(degres)}")
        
        # 3. Distances
        print(f"\n🔹 DISTANCES DES SEGMENTS:")
        print(f"  • Longueur totale réseau   : {sum(dists):,.1f} km")
        print(f"  • Longueur moyenne segment : {sum(dists)/len(dists):.3f} km")
        print(f"  • Segment le plus long     : {max(dists):.2f} km")
        
        # 4. Points d'intérêt
        print(f"\n🔹 POINTS D'INTÉRÊT:")
        print(f"  • Nombre total             : {len(self.POINTS_INTERET)}")
        
        print("="*60)
        print("✅ Statistiques prêtes pour la section 'Présentation du Réseau'")

    def generer_graphique_chemin_visuel_rapport(self, res, n_dep, n_arr):
        """Génère une image PNG statique du chemin pour le rapport Word."""
        if not res: return
        print("\n🎨 Génération du tracé pour le rapport Word...")
        
        plt.figure(figsize=(10, 8))
        # Fond (routes grises)
        edges = list(self.G.edges())[:5000] # Limité pour la rapidité
        for u, v in edges:
            if u in self.noeuds_coords and v in self.noeuds_coords:
                y = [self.noeuds_coords[u][0], self.noeuds_coords[v][0]]
                x = [self.noeuds_coords[u][1], self.noeuds_coords[v][1]]
                plt.plot(x, y, c='lightgray', lw=0.5, zorder=1)
        
        # Chemin (rouge)
        path_y, path_x = zip(*res.points_coordonnees)
        plt.plot(path_x, path_y, c='red', lw=2, label='Itinéraire optimal', zorder=2)
        
        # Points
        plt.scatter([path_x[0]], [path_y[0]], c='green', s=100, label='Départ', zorder=3)
        plt.scatter([path_x[-1]], [path_y[-1]], c='blue', s=100, label='Arrivée', zorder=3)
        
        plt.title(f"Itinéraire Optimisé : {n_dep} -> {n_arr}")
        plt.legend()
        plt.axis('off')
        plt.tight_layout()
        fn = f"rapport_trajet_{int(time.time())}.png"
        plt.savefig(fn, dpi=150)
        print(f"✅ Image sauvegardée: {fn}")
        plt.close()

    def generer_analyse_pdf_conforme(self):
        """Génère Matrice et Histogramme de manière robuste."""
        import matplotlib.pyplot as plt
        try: import seaborn as sns
        except ImportError: sns = None
        
        print("\n📊 Génération des graphiques d'analyse...")
        lieux = ["Gare Tanger Ville (TGV)", "Grand Socco (Place 9 Avril)", 
                 "Aéroport Ibn Battouta", "Cap Spartel (Phare)"]
        shorts = ["Gare", "Socco", "Aéroport", "Spartel"]
        
        # 1. Matrice
        print("   • Calcul matrice...")
        mat = []
        for d in lieux:
            row = []
            for a in lieux:
                if d == a: row.append(0)
                else:
                    try:
                        n1 = self.trouver_noeuds_proches(self.POINTS_INTERET[d], k=1)[0][0]
                        n2 = self.trouver_noeuds_proches(self.POINTS_INTERET[a], k=1)[0][0]
                        r = self.dijkstra(n1, n2)
                        row.append(round(r.distance_totale/1000, 1) if r else 0)
                    except: row.append(0)
            mat.append(row)

        plt.figure(figsize=(6, 5))
        if sns: sns.heatmap(mat, annot=True, cmap="YlGnBu", xticklabels=shorts, yticklabels=shorts, fmt='g')
        else: plt.imshow(mat); plt.colorbar()
        plt.title("Matrice Distances (km)")
        plt.tight_layout()
        plt.savefig("rapport_matrice.png", dpi=200)
        plt.close()
        print("   ✅ 'rapport_matrice.png' créé.")

        # 2. Histogramme (Robuste)
        print("   • Calcul histogramme...")
        times = []
        pts = list(self.POINTS_INTERET.values())
        for _ in range(50): 
            if len(times) >= 20: break
            try:
                p1, p2 = random.choice(pts), random.choice(pts)
                if p1 == p2: continue
                n1 = self.trouver_noeuds_proches(p1, k=1)[0][0]
                n2 = self.trouver_noeuds_proches(p2, k=1)[0][0]
                r = self.dijkstra(n1, n2)
                if r and r.temps_total > 0: times.append(r.temps_total * 60)
            except: pass
            
        plt.figure(figsize=(6, 4))
        plt.hist(times, bins=10, color='skyblue', edgecolor='black')
        plt.title(f"Distribution Temps Trajets (sur {len(times)} trajets)")
        plt.xlabel("Minutes"); plt.ylabel("Nombre")
        plt.tight_layout()
        plt.savefig("rapport_histogramme.png", dpi=200)
        plt.close()
        print("   ✅ 'rapport_histogramme.png' créé.")

    def exporter_rapport_complet(self, resultats_list):
        """Exporte tous les résultats du mode test en JSON."""
        print("\n💾 Export complet des résultats...")
        rapport = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trajets": []
        }
        for dep, arr, crit, res in resultats_list:
            if res:
                rapport["trajets"].append({
                    "depart": dep, "arrivee": arr, "critere": crit,
                    "km": round(res.distance_totale/1000, 2),
                    "min": round(res.temps_total*60, 1),
                    "dh": round(res.cout_total, 2)
                })
        fn = f"rapport_complet_{int(time.time())}.json"
        with open(fn, 'w', encoding='utf-8') as f: json.dump(rapport, f, indent=2)
        print(f"✅ Export JSON: {fn}")

    def mode_test_rapport(self):
        """Mode automatique pour générer 10 trajets avec barre de progression."""
        print("\n🧪 MODE TEST AUTOMATIQUE")
        print("="*60)
        
        paires = [
            ("Gare Tanger Ville (TGV)", "Aéroport Ibn Battouta", "distance"),
            ("Grand Socco (Place 9 Avril)", "Cap Spartel (Phare)", "temps"),
            ("Tanger City Mall", "Plage Municipale (Corniche)", "mixte"),
            ("FST Tanger (Boukhalef)", "Grand Socco (Place 9 Avril)", "distance"),
            ("Port de Tanger Ville (Ferry)", "Café Hafa", "mixte"),
            ("Place de France", "Grottes d'Hercule", "temps"),
            ("Marjane Route de Tétouan", "Kasbah (Musée)", "distance"),
            ("Aéroport Ibn Battouta", "Petit Socco", "mixte"),
            ("ENCG Tanger", "Boulevard Pasteur", "temps"),
            ("Grand Stade Ibn Batouta", "Malabata (Mövenpick/Casino)", "cout")
        ]
        
        res_list = []
        total = len(paires)
        print(f"Génération de {total} trajets pour le rapport...\n")
        
        for i, (d, a, c) in enumerate(paires, 1):
            # Barre de progression textuelle
            prog = "█" * (i * 20 // total) + "░" * (20 - i * 20 // total)
            print(f"[{prog}] Trajet {i}/{total}", end="\r")
            
            try:
                p1 = self.POINTS_INTERET[d]; p2 = self.POINTS_INTERET[a]
                r = self.trouver_chemin_optimal(p1, p2, c)
                if r:
                    res_list.append((d, a, c, r))
                    print(f"\n   ✓ {d[:15]}... → {a[:15]}... : {r.distance_totale/1000:.1f}km")
            except Exception as e: print(f"\n   ✗ Erreur: {str(e)[:40]}")
        
        print("\n" + "="*60)
        print(f"📊 RÉSULTATS: {len(res_list)}/{total} trajets réussis")
        if res_list: self.exporter_rapport_complet(res_list)

    # --- NOUVELLES FONCTIONNALITÉS (AMÉLIORATIONS) ---

    def generer_graphe_mathematique_illustratif(self):
        """
        Génère une image du réseau sous forme de graphe mathématique 
        pour illustrer le fonctionnement de Dijkstra avec des données factices.
        """
        print("\n🎨 Génération du graphe mathématique illustratif (Théorie des graphes)...")
        
        # 1. Création d'un graphe factice (mock data)
        # Structure des données en entrée : Dictionnaire de nœuds avec coordonnées (lat, lon)
        noeuds_mock = {
            "A (Départ)": (35.78, -5.81),
            "B": (35.77, -5.80),
            "C": (35.76, -5.82),
            "D": (35.75, -5.79),
            "E": (35.74, -5.81),
            "F (Arrivée)": (35.73, -5.80)
        }
        
        G_mock = nx.Graph()
        for nom, pos in noeuds_mock.items():
            # Inversion lat/lon pour l'affichage (x=lon, y=lat)
            G_mock.add_node(nom, pos=(pos[1], pos[0]))
            
        # 2. Ajout des arêtes avec des poids (distances)
        # Structure : Liste de tuples (Nœud1, Nœud2, Poids)
        aretes_mock = [
            ("A (Départ)", "B", 2.5),
            ("A (Départ)", "C", 3.0),
            ("B", "C", 1.2),
            ("B", "D", 4.0),
            ("C", "E", 2.8),
            ("D", "E", 1.5),
            ("D", "F (Arrivée)", 3.5),
            ("E", "F (Arrivée)", 2.0)
        ]
        
        for u, v, w in aretes_mock:
            G_mock.add_edge(u, v, weight=w)
            
        # 3. Calcul du plus court chemin avec Dijkstra
        depart = "A (Départ)"
        arrivee = "F (Arrivée)"
        chemin_optimal = nx.dijkstra_path(G_mock, depart, arrivee, weight='weight')
        edges_chemin = list(zip(chemin_optimal, chemin_optimal[1:]))
        
        # 4. Visualisation avec Matplotlib
        plt.figure(figsize=(10, 7))
        pos = nx.get_node_attributes(G_mock, 'pos')
        
        # Dessiner tous les nœuds (couleur neutre)
        nx.draw_networkx_nodes(G_mock, pos, node_color='lightgray', node_size=1500, edgecolors='gray')
        
        # Mettre en surbrillance les nœuds du chemin optimal
        nx.draw_networkx_nodes(G_mock, pos, nodelist=chemin_optimal, node_color='orange', node_size=1500, edgecolors='red', linewidths=2)
        
        # Mettre en évidence le départ et l'arrivée
        nx.draw_networkx_nodes(G_mock, pos, nodelist=[depart], node_color='lightgreen', node_size=1500, edgecolors='green', linewidths=2)
        nx.draw_networkx_nodes(G_mock, pos, nodelist=[arrivee], node_color='salmon', node_size=1500, edgecolors='red', linewidths=2)
        
        # Dessiner toutes les arêtes (couleur neutre)
        nx.draw_networkx_edges(G_mock, pos, edge_color='gray', width=1.5, style='dashed')
        
        # Mettre en surbrillance les arêtes du chemin optimal
        nx.draw_networkx_edges(G_mock, pos, edgelist=edges_chemin, edge_color='red', width=3)
        
        # Ajouter les étiquettes des nœuds (noms des places)
        nx.draw_networkx_labels(G_mock, pos, font_size=10, font_weight='bold')
        
        # Ajouter les étiquettes des arêtes (poids/distances)
        edge_labels = nx.get_edge_attributes(G_mock, 'weight')
        edge_labels_format = {k: f"{v} km" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G_mock, pos, edge_labels=edge_labels_format, font_size=9, font_color='blue', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        plt.title(f"Théorie des Graphes : Algorithme de Dijkstra\nChemin optimal en rouge ({depart} ➔ {arrivee})", fontsize=14, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        fn = f"graphe_dijkstra_illustratif_{int(time.time())}.png"
        plt.savefig(fn, dpi=200, bbox_inches='tight')
        print(f"✅ Image du graphe mathématique sauvegardée: {fn}")
        plt.close()

    def visualiser_chemin_web(self, res, n_dep, n_arr):
        """Génère la carte interactive HTML avec style Satellite et POIs."""
        if not res: return
        print("\n🗺️ Génération de la carte interactive...")
        
        lats, lons = zip(*res.points_coordonnees)
        centre_lat = sum(lats) / len(lats)
        centre_lon = sum(lons) / len(lons)
        
        # Création de la carte avec fond par défaut (sera écrasé par la tuile satellite)
        m = folium.Map(location=[centre_lat, centre_lon], zoom_start=14, tiles=None)
        
        # Ajout du fond de carte Satellite (Esri World Imagery)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Ajout d'un fond de carte alternatif (OpenStreetMap classique)
        folium.TileLayer('openstreetmap', name='OpenStreetMap', control=True).add_to(m)

        # Tracé de la ligne du chemin (PolyLine)
        folium.PolyLine(
            res.points_coordonnees, 
            color='blue', 
            weight=5, 
            opacity=0.8,
            tooltip="Chemin optimal"
        ).add_to(m)
        
        # Marqueurs pour les points intermédiaires
        # On ignore le premier et le dernier point qui auront leurs propres marqueurs
        for node_id, coord in zip(res.chemin[1:-1], res.points_coordonnees[1:-1]):
            nom_noeud = str(node_id)
            folium.CircleMarker(
                location=coord,
                radius=8,
                color='darkorange',
                fill=True,
                fill_color='darkorange',
                fill_opacity=0.8,
                popup=nom_noeud,
                tooltip=nom_noeud
            ).add_to(m)

        # Marqueur de DÉPART
        folium.Marker(
            res.points_coordonnees[0], 
            popup=f"<b>Départ:</b> {n_dep}", 
            tooltip="Point de départ",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
        
        # Marqueur d'ARRIVÉE
        folium.Marker(
            res.points_coordonnees[-1], 
            popup=f"<b>Arrivée:</b> {n_arr}", 
            tooltip="Point d'arrivée",
            icon=folium.Icon(color='red', icon='flag', prefix='fa')
        ).add_to(m)
        
        # Panneau d'information flottant (Contrôle HTML personnalisé)
        distance_km = res.distance_totale / 1000
        nb_intermediaires = len(res.points_coordonnees) - 2
        
        from branca.element import Template, MacroElement
        
        template = f"""
        {{% macro html(this, kwargs) %}}
        <div style="
            position: fixed; 
            top: 10px; right: 10px; width: 320px; height: auto; 
            background-color: rgba(255, 255, 255, 0.9); border: 2px solid #333; z-index:9999; font-size:14px;
            padding: 15px; border-radius: 8px; box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
            font-family: Arial, sans-serif;
            ">
            <h3 style="margin-top:0; color: #2c3e50; border-bottom: 1px solid #ccc; padding-bottom: 5px;">🗺️ Légende du Trajet</h3>
            <ul style="list-style-type: none; padding: 0; margin: 0; line-height: 1.8;">
                <li>🏁 <b>Départ :</b> {n_dep}</li>
                <li>🏁 <b>Arrivée :</b> {n_arr}</li>
                <li>📏 <b>Distance :</b> {distance_km:.2f} km</li>
                <li>📍 <b>POIs :</b> {nb_intermediaires}</li>
                <li>⚡ <b>Algo :</b> DIJKSTRA</li>
            </ul>
        </div>
        {{% endmacro %}}
        """
        macro = MacroElement()
        macro._template = Template(template)
        m.get_root().add_child(macro)
        
        # Ajout du contrôle des couches
        folium.LayerControl().add_to(m)

        fn = f"web_carte_{int(time.time())}.html"
        m.save(fn)
        print(f"✅ Carte Web interactive (Satellite) sauvegardée: '{fn}'")

    # --- MENU INTERACTIF ---
    
    def choisir_points_interactif(self):
        self.afficher_menu_points()
        keys = list(self.POINTS_INTERET.keys())
        
        def get_pt(txt):
            while True:
                c = input(f"\n{txt} (N° ou Q): ").strip().upper()
                if c == 'Q': return None, None
                if c.isdigit() and 1 <= int(c) <= len(keys):
                    return self.POINTS_INTERET[keys[int(c)-1]], keys[int(c)-1]
                print("❌ Choix invalide")

        p1, n1 = get_pt("Point de DÉPART")
        if not p1: return None, None, None, None, None
        
        p2, n2 = get_pt("Point d'ARRIVÉE")
        if not p2: return None, None, None, None, None
        
        print("\nCRITÈRE: 1.Distance 2.Temps 3.Coût")
        c = input("Choix (1-3): ").strip()
        crit = {'1':'distance', '2':'temps', '3':'cout'}.get(c, 'mixte')
        
        return p1, p2, n1, n2, crit

    def afficher_menu_points(self):
        print("\n📍 POINTS D'INTÉRÊT TANGER")
        for i, k in enumerate(self.POINTS_INTERET.keys(), 1):
            print(f"{i:2d}. {k}")
        print("Q. Quitter")

def main():
    """Menu Principal Professionnel."""
    print("\n" + "="*70)
    print(" "*15 + "🚗 PROJET ALGORITHME DE DIJKSTRA 🚗")
    print(" "*10 + "Optimisation de Trajets - Réseau Routier de Tanger")
    print("="*70)
    print("🎓 Analytique des Données - Structures Avancées")
    print("="*70)
    
    router = DijkstraRouterTanger()
    
    # Phase 1: Chargement
    print("\n🔄 PHASE 1/3 - CHARGEMENT DU RÉSEAU")
    if not router.charger_carte(): 
        print("❌ Échec. Fin."); return
    
    # Phase 2: Validation
    print("\n🔍 PHASE 2/3 - VALIDATION DU GRAPHE")
    if not router.valider_graphe(): 
        if input("\n⚠️  Continuer? (O/N): ").upper() != 'O': return
    
    # Phase 3: Stats
    print("\n📊 PHASE 3/3 - ANALYSE DU RÉSEAU")
    router.afficher_statistiques_graphe()
    
    while True:
        print("\n┌─────────────────────────────────────────────────────┐")
        print("│  1. 🧭 Mode Interactif (Choix manuel de trajet)    │")
        print("│  2. 🧪 Mode Test Batch (10 trajets automatiques)   │")
        print("│  3. 📊 Générer Graphiques pour Rapport             │")
        print("│  4. 🕸️  Générer Graphe Mathématique (Illustration)  │")
        print("│  5. 📋 Aide                                         │")
        print("│  6. 🚪 Quitter                                      │")
        print("└─────────────────────────────────────────────────────┘")
        
        choix = input("\n👉 Votre choix (1-6): ").strip()
        
        if choix == '1':
            print("\n" + "─"*70 + "\n 🧭 MODE INTERACTIF\n" + "─"*70)
            res_tuple = router.choisir_points_interactif()
            if res_tuple[0]:
                p1, p2, n1, n2, crit = res_tuple
                resultat = router.trouver_chemin_optimal(p1, p2, crit)
                router.afficher_resultats(resultat, n1, n2, crit, sauvegarder=True)
                
                if resultat:
                    # Génération automatique de l'image du graphe avec le chemin
                    router.generer_graphique_chemin_visuel_rapport(resultat, n1, n2)
                    
                    print("\n📤 ACTIONS SUPPLÉMENTAIRES: 1.HTML (Web) 2.Menu")
                    act = input("👉 Choix: ").strip()
                    if act == '1': router.visualiser_chemin_web(resultat, n1, n2)
        
        elif choix == '2':
            router.mode_test_rapport()
            input("\n✅ Entrée pour continuer...")
        
        elif choix == '3':
            router.generer_analyse_pdf_conforme()
            input("\n✅ Entrée pour continuer...")
            
        elif choix == '4':
            router.generer_graphe_mathematique_illustratif()
            input("\n✅ Entrée pour continuer...")
            
        elif choix == '5':
             print("\nOBJECTIF: Calcul chemin optimal via Dijkstra.")
             print("FONCTIONS: Matrice distances, Histogramme temps, Carte Web, Graphe Mathématique.")
             input("\n✅ Entrée pour continuer...")
             
        elif choix == '6':
            print("\n👋 Au revoir!"); break

if __name__ == "__main__":
    main()
