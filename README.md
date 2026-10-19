# Rimadesio Aurora

Calendario, risultati e classifiche di Rimadesio Aurora (Under 13 Gold e Under 14 Regionale, FIP Lombardia 2026/27).

Pagina statica: legge i dati dal backend pubblico FIP a ogni apertura.

## Come è fatto

- `index.html` è l'unico sorgente: pagina, stili, logica e una copia di riserva dei dati FIP, tutto in un file.
- Online: https://marzorati-it.github.io/rimadesio/ (GitHub Pages, branch `main`).
- `tools/prerender.py` riscrive dentro `index.html` il contenuto già calcolato dai dati salvati, così il file resta leggibile anche nelle anteprime senza JavaScript. Va lanciato dopo ogni modifica (`python3 tools/prerender.py`, serve Node).
- Icone: `favicon.svg` (sorgente), `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `favicon-32.png`, `manifest.webmanifest`.
