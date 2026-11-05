#!/usr/bin/env python3
"""
detectar_codificacion.py
Detecta caracteres mal codificados (mojibake) como Ã, Â, â€ y el caracter de reemplazo U+FFFD ()
en archivos HTML, PDF y Markdown.

Uso:
    python3 detectar_codificacion.py [archivos...]
    Si no se pasan argumentos, revisa los HTML, PDF de S13-S16 y docs/investigacion-*.md.
"""

import sys
import os
import re
import subprocess
from pathlib import Path

BAD_PATTERNS = [
    (re.compile(r'Ã[\x80-\xbf]'), 'UTF-8 decodificado como Latin-1/Windows-1252 (Ã...)'),
    (re.compile(r'Â[\xa0-\xbf]'), 'Caracter suplementario Latin-1 (Â...)'),
    (re.compile(r'â€[\x80-\xbf]'), 'Puntuacion UTF-8 decodificada como Latin-1 (â€...)'),
    (re.compile(r'\ufffd'), 'Caracter de reemplazo Unicode U+FFFD ()'),
    (re.compile(r'Ã'), 'Posible mojibake (Ã)'),
    (re.compile(r'Â'), 'Posible mojibake (Â)'),
    (re.compile(r'â€'), 'Posible mojibake (â€)'),
]

def check_text(text, filename):
    violations = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        for pattern, desc in BAD_PATTERNS:
            match = pattern.search(line)
            if match:
                start = max(0, match.start() - 25)
                end = min(len(line), match.end() + 25)
                snippet = line[start:end].strip()
                violations.append((idx, desc, snippet))
                break  # una violación reportada por línea es suficiente
    return violations

def extract_pdf_text(pdf_path):
    # Intentar con fitz (PyMuPDF)
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        text = ""
        for page_idx, page in enumerate(doc, 1):
            page_text = page.get_text()
            text += f"\n--- Page {page_idx} ---\n" + page_text
        return text
    except ImportError:
        pass

    # Intentar con pdftotext
    try:
        res = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
        return res.stdout
    except Exception as e:
        print(f"Error extrayendo texto de {pdf_path}: {e}", file=sys.stderr)
        return ""

def main():
    args = sys.argv[1:]
    if not args:
        # Archivos por defecto
        cwd = Path(".")
        files = []
        for sem in ["S13", "S14", "S15", "S16"]:
            files.extend(list(cwd.glob(f"*{sem}*.html")))
            files.extend(list(cwd.glob(f"*{sem}*.pdf")))
        files.extend(list((cwd / "docs").glob("investigacion-*.md")))
    else:
        files = [Path(a) for a in args]

    total_violations = 0
    checked_files = 0

    for file_path in files:
        if not file_path.exists():
            continue

        checked_files += 1
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            text = extract_pdf_text(file_path)
        else:
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"Error leyendo {file_path}: {e}", file=sys.stderr)
                continue

        violations = check_text(text, file_path.name)
        if violations:
            total_violations += len(violations)
            print(f"❌ {file_path} ({len(violations)} problemas de codificación):")
            for line_no, desc, snippet in violations[:8]:  # Mostrar max 8 por archivo
                print(f"   Línea/Pág {line_no}: [{desc}] ... {snippet} ...")
            if len(violations) > 8:
                print(f"   ... y {len(violations) - 8} más.")
        else:
            print(f"✅ {file_path}: 0 problemas de codificación")

    print("-" * 50)
    print(f"TOTAL: {total_violations} problemas de codificación en {checked_files} archivos inspeccionados.")

    if total_violations > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
