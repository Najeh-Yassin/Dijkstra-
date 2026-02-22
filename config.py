"""
config.py - Centralized configuration for the Dijkstra Router Tanger project.
All tunable parameters are defined here for easy maintenance.
"""

# ─── Network Settings ────────────────────────────────────────────────────────
CITY_NAME: str = "Tanger, Morocco"
NETWORK_TYPE: str = "drive"          # 'drive' | 'walk' | 'bike' | 'all'
OSM_TIMEOUT: int = 300               # seconds

# ─── Routing Parameters ──────────────────────────────────────────────────────
DEFAULT_SPEED_KMH: float = 45.0      # average urban speed (km/h)
FUEL_COST_PER_KM: float = 1.8        # DH / km

# Default composite-weight coefficients
ALPHA_DISTANCE: float = 1.0          # weight for distance component
BETA_TIME: float = 0.5               # weight for time component
GAMMA_COST: float = 0.3              # weight for cost component

# ─── Detection ───────────────────────────────────────────────────────────────
DEFAULT_DETECTION_RADIUS_M: int = 200   # metres around path nodes
DETECTION_RADIUS_OPTIONS: dict = {
    "1": 100,
    "2": 200,
    "3": 300,
}

# ─── Nearest-node cache ──────────────────────────────────────────────────────
NEAREST_NODE_CACHE_SIZE: int = 512   # LRU cache entries

# ─── Output / Export ─────────────────────────────────────────────────────────
OUTPUT_DIR: str = "."                # directory for generated files
JSON_INDENT: int = 2
MAX_STREETS_IN_REPORT: int = 10
MAX_POI_IN_REPORT: int = 20

# ─── Visualisation ───────────────────────────────────────────────────────────
MAP_ZOOM_START: int = 14
ROUTE_COLOR: str = "#1a73e8"         # Google-blue
ROUTE_WEIGHT: int = 6
ROUTE_OPACITY: float = 0.85
POI_MARKER_RADIUS: int = 9
POI_MARKER_COLOR: str = "#ff6d00"    # deep-orange
PNG_DPI: int = 150
PNG_FIGSIZE: tuple = (12, 9)

# ─── Batch / Test Mode ───────────────────────────────────────────────────────
BATCH_PAIRS = [
    ("Gare Tanger Ville (TGV)",        "Aéroport Ibn Battouta",          "distance"),
    ("Grand Socco (Place 9 Avril)",    "Cap Spartel (Phare)",            "temps"),
    ("Tanger City Mall",               "Plage Municipale (Corniche)",    "mixte"),
    ("FST Tanger (Boukhalef)",         "Grand Socco (Place 9 Avril)",    "distance"),
    ("Port de Tanger Ville (Ferry)",   "Café Hafa",                      "mixte"),
    ("Place de France",                "Grottes d'Hercule",              "temps"),
    ("Marjane Route de Tétouan",       "Kasbah (Musée)",                 "distance"),
    ("Aéroport Ibn Battouta",          "Petit Socco",                    "mixte"),
    ("ENCG Tanger",                    "Boulevard Pasteur",              "temps"),
    ("Grand Stade Ibn Batouta",        "Malabata (Mövenpick/Casino)",    "cout"),
]

# ─── Analysis (matrix / histogram) ───────────────────────────────────────────
ANALYSIS_LIEUX = [
    "Gare Tanger Ville (TGV)",
    "Grand Socco (Place 9 Avril)",
    "Aéroport Ibn Battouta",
    "Cap Spartel (Phare)",
]
ANALYSIS_SHORTS = ["Gare", "Socco", "Aéroport", "Spartel"]
HISTOGRAM_SAMPLE_SIZE: int = 20
HISTOGRAM_MAX_TRIES: int = 50

# ─── Logging ─────────────────────────────────────────────────────────────────
LOG_LEVEL: str = "INFO"              # DEBUG | INFO | WARNING | ERROR
LOG_FILE: str = "dijkstra_router.log"
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
