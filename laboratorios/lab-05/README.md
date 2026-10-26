# 🧪 Lab 5 — Base de datos administrada y respaldos

**Asignatura:** Arquitectura en la Nube 2026-2 · **Semana del curso:** 8 (Unidad 2)
**Valor:** 10 % · Corte 2 · Actividad 2
**Módulo AWS Academy:** Módulo 6 — Databases (lab de desafíos «migración a RDS»)

## 🎯 Objetivo

Crear una base **PostgreSQL administrada y privada**, cargar pedidos, generar un
**snapshot** y **restaurar una instancia nueva** comprobando que los datos
sobreviven — la diferencia entre respaldo y réplica, en la práctica.

## ✅ Prerrequisitos

- Semana 8: [deck BD administradas y backup](../../2026-2-S08-arquitectura-nube-bd-administradas-backup.html) · [PDF](../../2026-2-S08-arquitectura-nube-bd-administradas-backup.pdf) · [video parte 1](../../videos/2026-2-S08-arquitectura-nube-bd-administradas-backup-parte1.mp4) · [parte 2](../../videos/2026-2-S08-arquitectura-nube-bd-administradas-backup-parte2.mp4) · [parte 3](../../videos/2026-2-S08-arquitectura-nube-bd-administradas-backup-parte3.mp4)
- Haber hecho el Lab 2 (la base es privada: solo el grupo `sg-db` llega al 5432).
- Distinguir Multi-AZ (alta disponibilidad) de réplica de lectura (escala de lectura).

## 🛠️ Pasos

**[Guía completa del Lab 5 — RDS y respaldos](https://labs.proyectoasur.org/guia/lab-05-rds-respaldos)**:

1. Crear la instancia **RDS** (PostgreSQL, privada, con respaldos activados).
2. Conectarse con `psql` y **cargar pedidos**.
3. Crear el **snapshot** de la base.
4. **Restaurar** en una instancia nueva desde el snapshot.
5. Comprobar que los datos están en la restaurada.
6. Autocontrol con `revisar` (5 de 5).

## 📦 Entregable

Base administrada con datos, snapshot y restauración verificada (plataforma), o
el lab de desafíos «migración a RDS» del Módulo 6 en tu Learner Lab.

## 📊 Rúbrica (10 %)

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `instancia_rds` | la base está `available`, PostgreSQL, privada | 1,0 |
| 2 | `respaldos` | retención de respaldos ≥ 7 días | 1,0 |
| 3 | `datos` | la tabla `pedidos` con al menos 2 filas vía `psql` | 1,0 |
| 4 | `snapshot` | el snapshot existe y es de esa base | 1,0 |
| 5 | `restaurada` | la instancia restaurada está `available` y con los pedidos | 1,0 |

## 🔗 Enlaces

- [Guía completa en la plataforma de labs](https://labs.proyectoasur.org/guia/lab-05-rds-respaldos)
- [Lab AWS — migración a RDS en AWS Academy](https://awsacademy.instructure.com/courses/181773/modules/items/17915811) (Módulo 6)
- [Plataforma de labs](https://labs.proyectoasur.org/)
