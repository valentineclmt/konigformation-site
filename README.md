# konigformation.com — site statique

Site de Konig Formation, généré par `build.py` (Python 3, aucune dépendance) et servi par GitHub Pages depuis le dossier `docs/`.

## Structure
- `content/sitedata.py` — coordonnées, liens (RDV, Qualiopi, CGV…), avis, chiffres, financement
- `content/formations.py` — les fiches formations et les pages « univers » (IA, Pack Office)
- `content/posts/*.html` — un fichier par article de blog (en-tête JSON + contenu HTML)
- `static/` — CSS, JS, polices, images, PDF (copiés tels quels)
- `build.py` — génère `docs/` ; `docs/` est ce qui est publié

## Publier une modification
```
python3 build.py
git add -A && git commit -m "…" && git push
```
GitHub Pages met le site à jour en 1 à 2 minutes.

## Ajouter un article
Créer `content/posts/<slug>.html` :
```
<!--
{
 "title": "Titre de l'article",
 "slug": "<slug>",
 "date": "2026-12-01",
 "category": "intelligence-artificielle",   (ou pack-office, marketing-digital)
 "description": "Méta-description ~155 caractères",
 "cover": "assets/covers/<slug>.png"
}
-->
<p>Contenu HTML…</p>
```
Déposer la couverture (1200×630) dans `static/assets/covers/`, puis `python3 build.py` et pousser.
L'URL de l'article sera `https://www.konigformation.com/<slug>/`.
