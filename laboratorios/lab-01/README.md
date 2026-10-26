# 🧪 Lab 1 — Almacenamiento y sitio estático en la nube

**Asignatura:** Arquitectura en la Nube 2026-2 · **Semana del curso:** 3 (Unidad 1)
**Valor:** 10 % · Corte 1 · Actividad 1
**Módulo AWS Academy:** Módulo 4 — Storage (lab de desafíos «sitio web estático con Amazon S3»)

## 🎯 Objetivo

Usar el almacenamiento de objetos de la nube como si fuera Amazon S3: crear un
**bucket**, activar **versionado**, publicar un **sitio estático** con los tipos
MIME correctos y comprobar que se sirve por HTTP — entendiendo qué hace S3 real
y qué no emula la nube de la estación.

## ✅ Prerrequisitos

- Semana 3: [deck Almacenamiento](../../2026-2-S03-arquitectura-nube-almacenamiento.html) · [PDF](../../2026-2-S03-arquitectura-nube-almacenamiento.pdf) · [video parte 1](../../videos/2026-2-S03-arquitectura-nube-almacenamiento-parte1.mp4) · [parte 2](../../videos/2026-2-S03-arquitectura-nube-almacenamiento-parte2.mp4) · [parte 3](../../videos/2026-2-S03-arquitectura-nube-almacenamiento-parte3.mp4)
- Saber qué es un bucket, un objeto y el versionado (láminas de la semana 3).

## 🛠️ Pasos

La **guía completa, paso a paso con comandos**, está publicada en la plataforma de labs:
**[guía del Lab 1 — sitio estático](https://labs.proyectoasur.org/guia/lab-01-sitio-estatico)**.

1. Crear el bucket `sitio-hep` en `us-east-1` y comprobar su región.
2. Activar **versionado** en el bucket.
3. Subir `index.html`, `error.html` y `estilo.css` con su `Content-Type` declarado.
4. Subir una **segunda versión** de `index.html` y listar las dos versiones.
5. Configurar el sitio web (`IndexDocument` + `ErrorDocument`).
6. Comprobar el sitio por HTTP y ejecutar el autocontrol `revisar` (5 de 5).

## 📦 Entregable

No se suben archivos: se evalúa el **estado de tu nube** (los 5 criterios de
abajo, verificados desde fuera). En la modalidad AWS Academy el lab de desafíos
del Módulo 4 se auto-califica en tu Learner Lab al terminar la actividad.

## 📊 Rúbrica (10 %)

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `bucket_creado` | el bucket existe en `us-east-1` | 1,0 |
| 2 | `versionado` | `Status=Enabled` y ≥ 2 versiones del index | 1,0 |
| 3 | `objetos` | los 3 objetos con su `Content-Type` | 1,0 |
| 4 | `sitio_responde` | `GET` al index → 200 con la marca del sitio | 1,0 |
| 5 | `error_accesible` | `GET` al error → 200 con la página de error | 1,0 |

## 🔗 Enlaces

- [Guía completa en la plataforma de labs](https://labs.proyectoasur.org/guia/lab-01-sitio-estatico)
- [Lab AWS — sitio web estático (S3) en AWS Academy](https://awsacademy.instructure.com/courses/181773/modules/items/17915825) (Módulo 4)
- [Plataforma de labs](https://labs.proyectoasur.org/)
