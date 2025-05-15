# Pattern Matcher

Un projet de vision par ordinateur qui détecte un motif spécifique dans une vidéo à l'aide de l'algorithme FLANN (Fast Library for Approximate Nearest Neighbors).

---

## Fonctionnalités

- Chargement automatique d'une vidéo et d'une image modèle.
- Détection du motif dans chaque frame de la vidéo.
- Sauvegarde des frames où le motif a été trouvé.
- Affichage du niveau de confiance lors des détections.

---

## Exemple

À chaque frame où un motif est détecté, un rectangle est dessiné et la confiance est indiquée. Les frames correspondantes sont sauvegardées dans un dossier `output/`.

---

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/DOFRADJO/pattern-matcher.git
   cd pattern-matcher
