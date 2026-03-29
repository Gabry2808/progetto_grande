# DevLog

## Semaine 1 — Découverte d’Arcade (Gabry)

### Setup du projet
Temps: ~30 min

- création du projet et installation de `arcade` avec `uv`
- création des fichiers principaux (`main.py`, `gameview.py`, `constants.py`, `textures.py`)
- configuration de GitHub et des clés SSH
- mise en place d’une première version jouable du jeu

### Fonctionnalités réalisées
- affichage du joueur, de l’herbe et des buissons
- déplacement du joueur au clavier
- collisions avec les obstacles
- remise à zéro avec `Escape`
- caméra qui suit le joueur
- animation du joueur
- cristaux à ramasser

### Tests
- ajout de `tests/conftest.py`
- mise en place du test `test_collect_crystals.py`

### État du projet
À la fin de la semaine 1, le jeu fonctionnait avec :
- une carte simple
- un joueur contrôlable
- des obstacles
- une caméra
- des animations
- des cristaux collectables
- un premier test automatisé

### Amélioration des contrôles clavier
Temps: ~1h

- correction du problème de gestion des touches simultanées
- implémentation d’un système avec états (`go_right`, `go_left`, etc.)
- amélioration du comportement du joueur lors des changements de direction

### Amélioration de la caméra
Temps: ~1h

- implémentation d’une marge autour du joueur
- la caméra ne suit plus immédiatement le joueur
- déplacement de la caméra uniquement lorsque le joueur s’approche des bords
- conservation du clamp pour éviter de sortir du monde

### Ajout des sons
Temps: ~20 min

- chargement d’un son avec `arcade.load_sound`
- lecture du son lors de la collecte des cristaux avec `arcade.play_sound`
- séparation entre chargement (init) et utilisation (runtime)



## Semaine 2: Maps et monstres

### Implémentation de la structure Map
Temps: ~2h

- Création du fichier `map.py`
- Définition de l'enum `GridCell`
- Implémentation de la classe `Map`
- Ajout de la méthode `get(x, y)`

### Refactoring de GameView
Temps: ~1h

- Modification de `GameView` pour recevoir une `Map`
- Suppression du hardcoding de la map
- Génération des sprites à partir de `map.get(x, y)`
- Position du joueur basée sur `player_start_x` et `player_start_y`

### Création de la map de découverte
Temps: ~30 min

- Implémentation de `MAP_DECOUVERTE`
- Reproduction de la map précédente avec les buissons et cristaux

### Adaptation du projet
Temps: ~20 min

- Modification de `main.py` pour passer `MAP_DECOUVERTE`
- Adaptation des tests (`test_collect_crystals`)
- Vérification que le jeu fonctionne

### Début de la section "Charger la map depuis un fichier"
Temps: ~20 min

- Création du dossier `maps`
- Ajout du fichier `maps/map1.txt`
- Analyse du format du fichier de carte

### Suite et fin de la section "Charger la map depuis un fichier" sans spinner (Enzo)
Temps: ~ 1h 30 min

- implementation de plusieurs fonctions de pour decouper le travail

### Spinner
Temps: ~2h30 min

- implementation de la classe spinner, fontion pour calculer les limites dans Map
- dessiner, bouger les spinners avec des listes dans Gameview

## SEMAINE 3 : Trous et boomerang

### creation classe Player et Direction (Enzo)
Temps: 30min

- implementer Player qui herite de arcade.TextureAnimation et refactoriser GameView pour l'alleger  sans grand "changement" dans un nouveau module : player
- implementer Direction pour les differentes orientation du joueur dans le module player

### Afficher Score (Enzo)
Temps : 45min

- completer GameView et utiliser les fonctionnalites de Arcade pour afficher en bas a gauche le Score (nombre de crystaux collectes)

### Boomerang (Enzo)
Temps: 3h

- nouveau module : boomerang avec une classe Boomerang
- implementer une classe BoomerangState dans ce module
- ameliorer la GameView

## SEMAINE 4: Epee et Chauve-Souris
