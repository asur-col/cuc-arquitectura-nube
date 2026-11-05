#!/usr/bin/env python3
"""
verificar_tamano_texto.py
Verifica que todo el texto SVG en las diapositivas tenga font-size >= 16 px,
salvo las fuentes (.src o textos de pie).
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup

def verificar_deck(html_path):
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    violations = []
    
    slides = soup.find_all("section", class_="slide")
    for s_idx, slide in enumerate(slides, 1):
        if "cover" in slide.get("class", []):
            continue  # Portadas tienen su propia tipografía
            
        svg = slide.find("svg", class_="dgm")
        if not svg:
            # Buscar cualquier svg en el cuerpo
            svg = slide.find("svg")
            
        if not svg:
            continue
            
        for t in svg.find_all("text"):
            # Omitir si es fuente o atribución
            classes = t.get("class", [])
            if isinstance(classes, str):
                classes = [classes]
            if "src" in classes or "fuente" in classes:
                continue
            text_content = t.get_text().strip()
            if text_content.startswith("Fuente:") or text_content.startswith("Licencia:"):
                continue
                
            fs_val = t.get("font-size")
            if not fs_val:
                # Buscar en style
                style = t.get("style", "")
                m = re.search(r'font-size:\s*(\d+)px', style)
                if m:
                    fs_val = m.group(1)
                    
            if fs_val:
                # Quitar 'px' si viene incluido
                try:
                    size = float(re.sub(r'[^\d.]', '', fs_val))
                    if size < 16.0:
                        violations.append((s_idx, size, text_content[:40]))
                except ValueError:
                    pass

    return violations

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 verificar_tamano_texto.py archivo.html")
        sys.exit(1)
        
    html_path = Path(sys.argv[1])
    violations = verificar_deck(html_path)
    if violations:
        print(f"❌ {html_path.name}: {len(violations)} textos con font-size < 16 px:")
        for s_idx, size, snippet in violations[:10]:
            print(f"   Diap {s_idx}: {size}px -> '{snippet}'")
        if len(violations) > 10:
            print(f"   ... y {len(violations) - 10} más.")
        sys.exit(1)
    else:
        print(f"✅ {html_path.name}: 0 textos con font-size < 16 px (cumple estándar)")
        sys.exit(0)

if __name__ == "__main__":
    main()
