# 🧪 Lab 4 — Cómputo con sitio dinámico

**Asignatura:** Arquitectura en la Nube 2026-2 · **Semana del curso:** 7 (Unidad 2)
**Valor:** 10 % · Corte 2 · Actividad 1
**Módulo AWS Academy:** Módulo 5 — Compute (lab de desafíos de la cafetería: sitio web dinámico con EC2)

## 🎯 Objetivo

Lanzar una **instancia EC2** con `user-data` que instala y sirve una página
generada, abrir **solo el puerto 80**, publicar el sitio y asignarle una
**dirección IP elástica**.

## ✅ Prerrequisitos

- Semana 7: [deck Cómputo en la nube](../../2026-2-S07-arquitectura-nube-computo.html) · [PDF](../../2026-2-S07-arquitectura-nube-computo.pdf) · [video parte 1](../../videos/2026-2-S07-arquitectura-nube-computo-parte1.mp4) · [parte 2](../../videos/2026-2-S07-arquitectura-nube-computo-parte2.mp4) · [parte 3](../../videos/2026-2-S07-arquitectura-nube-computo-parte3.mp4)
- Haber hecho el Lab 2 (red y grupo de seguridad del servidor web).
- Saber qué hace el `user-data` en el primer arranque de una instancia.

## 🛠️ Pasos

**[Guía completa del Lab 4 — Cómputo con sitio dinámico](https://labs.proyectoasur.org/guia/lab-04-computo-sitio-dinamico)**:

1. Preparar red y grupo de seguridad (TCP 80 abierto).
2. Escribir el **`user-data`** que instala el servidor web y genera la página.
3. **Lanzar la instancia** con su AMI y tipo (`t3.micro`).
4. Comprobar el sitio publicado (HTTP 200 con la marca del sitio).
5. Asociar la **IP elástica** a la instancia.
6. Autocontrol con `revisar` (5 de 5).

## 📦 Entregable

Instancia corriendo con su sitio publicado y su IP elástica (plataforma), o el
lab de desafíos de la cafetería del Módulo 5 en tu Learner Lab de AWS Academy,
auto-calificado al terminar.

## 📊 Rúbrica (10 %)

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `instancia` | la instancia está `running`, con su AMI y tipo | 1,0 |
| 2 | `user_data` | base64 decodificable, instala el servidor y genera la página | 1,0 |
| 3 | `sg_app` | TCP 80 desde `0.0.0.0/0` | 1,0 |
| 4 | `http_200` | el puerto publicado responde 200 con la marca del sitio | 1,0 |
| 5 | `eip` | la IP elástica está asociada a la instancia | 1,0 |

## 🔗 Enlaces

- [Guía completa en la plataforma de labs](https://labs.proyectoasur.org/guia/lab-04-computo-sitio-dinamico)
- [Lab AWS — sitio web dinámico con EC2 en AWS Academy](https://awsacademy.instructure.com/courses/181773/modules/items/17915797) (Módulo 5)
- [Plataforma de labs](https://labs.proyectoasur.org/)
