# 🧪 Lab 3 — IAM, roles y mínimo privilegio

**Asignatura:** Arquitectura en la Nube 2026-2 · **Temas:** semanas 2 y 9 (identidad y acceso, identidad avanzada)
**Valor:** práctica del tema de identidad — el Módulo 9 de AWS Academy no trae lab de desafíos, así que este laboratorio se hace en la estación de la universidad
**Módulo AWS Academy relacionado:** Módulo 9 — Identidad avanzada (contenido, sin lab de desafíos)

## 🎯 Objetivo

Aplicar el **mínimo privilegio** de verdad: crear un **rol de EC2** con una
política de **solo lectura** sobre el bucket del sitio, un **instance profile**
que lo use, y un **usuario auditor** con una **denegación explícita** — sin
comodines (`*`, `:*`, `NotAction`).

## ✅ Prerrequisitos

- Semana 9: [deck Identidad avanzada](../../2026-2-S09-arquitectura-nube-identidad-avanzada.html) · [PDF](../../2026-2-S09-arquitectura-nube-identidad-avanzada.pdf) · [video parte 1](../../videos/2026-2-S09-arquitectura-nube-identidad-avanzada-parte1.mp4) · [parte 2](../../videos/2026-2-S09-arquitectura-nube-identidad-avanzada-parte2.mp4) · [parte 3](../../videos/2026-2-S09-arquitectura-nube-identidad-avanzada-parte3.mp4)
- Semana 2 (base de identidad): [deck Despliegue e identidad](../../2026-2-S02-arquitectura-nube-despliegue-identidad.html)
- Haber hecho el Lab 1 (el rol lee el bucket del sitio).

## 🛠️ Pasos

**[Guía completa del Lab 3 — IAM, roles y mínimo privilegio](https://labs.proyectoasur.org/guia/lab-03-iam-minimo-privilegio)**:

1. Crear la **política de confianza** y el **rol** (`sts:AssumeRole` para EC2).
2. Crear la **política de solo lectura** del bucket (solo `GetObject` y `ListBucket`).
3. Revisar que la política queda **sin comodines**.
4. Crear el **instance profile** y asociarle el rol.
5. Crear el **usuario auditor**: permiso de listar + **Deny explícito** de borrar.
6. Autocontrol con `revisar` (5 de 5).

## 📦 Entregable

Estado de tu nube: rol, política, instance profile y usuario auditor con la
denegación explícita, verificados desde fuera por los 5 criterios.

## 📊 Rúbrica (5 criterios automáticos)

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `rol_confianza` | el rol confía en EC2 con `sts:AssumeRole` | 1,0 |
| 2 | `politica_bucket` | solo `GetObject` y `ListBucket` sobre el bucket | 1,0 |
| 3 | `sin_comodines` | políticas del rol sin `*`, `:*` ni `NotAction` | 1,0 |
| 4 | `instance_profile` | el perfil contiene el rol | 1,0 |
| 5 | `usuario_auditor` | Allow de listar + Deny explícito de borrar | 1,0 |

## 🔗 Enlaces

- [Guía completa en la plataforma de labs](https://labs.proyectoasur.org/guia/lab-03-iam-minimo-privilegio)
- [Plataforma de labs](https://labs.proyectoasur.org/)
