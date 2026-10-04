# NOTAS DE PRODUCCIÓN — plan para continuar en local

Última actualización: 4 oct 2026 (sesión en la nube de Claude Code). Léelo junto con `CLAUDE.md` y
`docs/ESTANDAR-PRODUCCION.md`.

## Qué se hizo en esta sesión
1. Análisis del repo, del temario (vs AWS Academy Cloud Architecting y SAA-C03) y de las presentaciones viejas
   de Azure/OpenStack → `docs/analisis-tematico.md`, `docs/fuentes-recursos.md`.
2. Estándar de producción, plantilla, librería de íconos multi-nube y herramientas (`herramientas/`).
3. Producción con subagentes Sonnet (uno por semana, auditados con `verificar.py` + revisión visual de capturas).
4. **No se generaron videos** (decisión del docente: los hace en local). Cada semana deja HTML + PDF + `guiones/`.

## Estado por semana (sesión SUSPENDIDA por el docente; agentes detenidos)
Leyenda: ✅ pasa `verificar.py` completo (estructura, guion, render sin desbordes) · 👁 falta mi revisión visual de capturas
(el verificador no detecta textos encimados ni flechas sobre etiquetas: mirar `--capturas`) · ⚠️ incompleta.
Semanas ≥ 9: creadas pero **NO publicadas** en `index.html` ("Próximamente").

| Sem | Tema | Diap. | Estado |
|---|---|---|---|
| S01 | Fundamentos | publicada: 13 | ⚠️ borrador **incompleto** (3 de 4 partes, 45 diap.) en `borradores/`; la publicada sigue intacta. Hay que terminarlo: partes 3–4 (modelos de servicio/infraestructura global; proveedores y Well-Architected). Ver temario en `docs/analisis-tematico.md` |
| S02 | Despliegue e identidad | 60 | ✅ 👁 rehecha (reemplaza la publicada; ya no coincide con su video anterior) |
| S03 | Almacenamiento | 60 | ✅ 👁 rehecha |
| S04 | Redes | 60 | ✅ revisada visualmente |
| S05 | Seguridad y cumplimiento | 60 | ✅ 👁 rehecha |
| S07 | Cómputo | 56 | ✅ revisada visualmente |
| S08 | BD administradas y backup | 56 | ✅ revisada visualmente |
| S09 | Identidad avanzada | 60 | ✅ 👁 nueva |
| S10 | Elasticidad, HA y monitorización | 60 | ✅ revisada visualmente |
| S11 | IaC + repaso U2 | 60 | ✅ 👁 nueva |
| S12 | Caché y CDN | 60 | ✅ 👁 nueva |
| S13 | Arquitecturas desacopladas | 56 | ✅ revisada visualmente |
| S14 | Serverless y microservicios (+ contenedores) | 60 | ✅ 👁 nueva |
| S15 | Ingeniería de datos | 60 | ✅ 👁 nueva |
| S16 | DR + repaso general (sem. 16–17) | — | ⚠️ borrador **incompleto** en `borradores/` (47 diap.: la parte 4 solo tiene 4 diapositivas de contenido) |

Comprobación rápida: `python3 herramientas/verificar.py ARCHIVO.html --capturas /tmp/cap` y mirar `hoja-contacto.png`.
Nota: S02, S03 y S05 sobrescribieron las versiones publicadas (la versión anterior sigue en el historial de git).

## Plan para continuar en local
### A. Terminar lo que falte
Para S01 y S16 (⚠️): terminar los borradores de `borradores/` (copiar a la raíz al terminar). Para las 👁: revisión visual de capturas. En general, si el verificador marca ❌, corregir con
Claude local siguiendo `docs/ESTANDAR-PRODUCCION.md`; si no existe, producirlo desde `plantillas/semana-base.html`.
Temario de cada semana (4 partes) en `docs/analisis-tematico.md` §3.3 y en los títulos del calendario de `index.html`.

### B. Revisión técnica por el docente (pendiente de contrastar con la guía oficial de AWS Academy)
Los subagentes escribieron de memoria; confirmar antes de grabar:
- **Labs** (pasos y valores de ejemplo): S04 (VPC 10.0.0.0/16, subredes .1.0/.2.0), S07 (sitio dinámico EC2),
  S08 (migración RDS), S10 (Auto Scaling: mín. 2, máx. 6, CPU objetivo 50 %). Alinear con las guías de los módulos 5, 6, 7, 10.
- **Cifras de AWS:** retención de copias RDS 1–35 días; failover Multi-AZ 60–120 s; ALB health check por defecto;
  CloudWatch retención 3 h/15 d/63 d/15 m; Trusted Advisor (categorías y planes); tamaño máx. de mensaje SQS (1 MiB desde 2025);
  límites por fragmento de Kinesis; VPN 1,25 Gbps por túnel; tarifa de IPv4 pública (~0,005 USD/h).
- **Tallas de instancia** en S07 (m5/c5/r5/t3) y afirmaciones sobre Nitro/KVM, Hyper-V (Azure), KVM (GCP).
- Cifras de los casos de la Corporación Industrial del Caribe: son **ilustrativas** (marcadas así en pantalla).

### C. Generar PDF y videos (en el computador del docente)
```bash
pip install playwright edge-tts && python -m playwright install chromium   # + ffmpeg
python3 herramientas/generar_pdf.py 2026-2-SNN-*.html
python3 herramientas/generar_videos.py 2026-2-SNN-*.html          # 4 MP4 en videos/ (voz es-CO-GonzaloNeural)
```
- Confirmar con el docente **qué voz usó en los videos actuales** (`--voz`); `edge-tts --list-voices | grep es-`.
- Los videos S04 (1 video de la versión vieja) y S07/S08 (4 partes de la versión vieja) quedan **desactualizados**:
  regenerar y luego `python3 herramientas/publicar_semana.py 04|07|08` para actualizar los enlaces.
- Cada semana pesa ~75 MB en videos; valorar Git LFS o subirlos a OneDrive y enlazar desde `index.html`.

### D. Publicar semana a semana
1. PDF + videos generados → `python3 herramientas/publicar_semana.py NN` (activa la tarjeta en `index.html`).
2. Commit y push. Orden sugerido según calendario: S09 → S10 → S11 → S12 → S13 → S14 → S15 → S16.

### E. Tareas pendientes de mantenimiento
- Reescribir `README.md` (describe el curso viejo de Azure: 19 videos, placeholders sin completar).
- Revisar/eliminar los stubs de `laboratorios/lab-01..07` (restos del curso Azure; el índice los referencia como "complementarios").
- Verificar el logo CUC: las portadas cargan `es.wikipedia.org/.../Logo_cuc.png` (si falla, usar `logo-cuc.png` local del historial git).
- Opcional: portar S01–S05 al mismo nivel visual si alguna quedó sin rehacer.

## Decisiones del docente que rigen
- Títulos y fechas del calendario NO cambian; mejoras dentro de cada semana.
- Enfoque multi-nube conceptual (por eso se usan ejemplos Azure/OpenStack/GCP) con práctica en AWS Academy.
- Semanas futuras: material creado pero desactivado hasta que el docente las publique.
- Videos con voz sintética: los genera el docente en local; aquí solo diapositivas + guion + instrucciones.

## Reutilizar el flujo en otra asignatura
`docs/prompt-replicar-asignatura.md`.
