# 🧪 Lab 2 — VPC, subredes y grupos de seguridad

**Asignatura:** Arquitectura en la Nube 2026-2 · **Semana del curso:** 4 (Unidad 1)
**Valor:** 10 % · Corte 1 · Actividad 2
**Módulos AWS Academy:** Módulos 7 y 8 — Networking (lab de desafíos «red VPC»)

## 🎯 Objetivo

Diseñar una **VPC de dos capas en dos zonas de disponibilidad** (`10.20.0.0/16`),
con salida a Internet **solo para la capa pública** y **grupos de seguridad de
mínimo privilegio**: web abierta al mundo, base de datos abierta solo al grupo
web, y subredes privadas sin ruta a Internet.

## ✅ Prerrequisitos

- Semana 4: [deck Redes](../../2026-2-S04-arquitectura-nube-redes.html) · [PDF](../../2026-2-S04-arquitectura-nube-redes.pdf) · [video parte 1](../../videos/2026-2-S04-arquitectura-nube-redes-parte1.mp4) · [parte 2](../../videos/2026-2-S04-arquitectura-nube-redes-parte2.mp4) · [parte 3](../../videos/2026-2-S04-arquitectura-nube-redes-parte3.mp4)
- Saber leer notación CIDR y distinguir Security Group (con estado, por instancia) de NACL (sin estado, por subred).
- Si usas PuTTY para entrar por SSH: [guía de acceso SSH — PEM y PPK](../acceso-ssh-lab-vpc.html).

## 🛠️ Pasos

**[Guía completa del Lab 2 — VPC, subredes y grupos de seguridad](https://labs.proyectoasur.org/guia/lab-02-vpc-subredes)**:

1. Crear la VPC y las **cuatro subredes** (dos públicas, dos privadas, en dos AZ).
2. Adjuntar el **Internet Gateway** y crear la **tabla de rutas pública** (`0.0.0.0/0`).
3. Crear el grupo `sg-web`: 80/443 públicos, SSH solo desde dentro de la VPC.
4. Crear el grupo `sg-db`: 5432 **solo desde `sg-web`**, sin `0.0.0.0/0`.
5. Comprobar que las subredes privadas no tienen IP pública ni ruta por defecto.
6. Autocontrol con `revisar` (5 de 5).

## 📦 Entregable

Estado final de la red en tu nube (plataforma) o el lab de desafíos del Módulo 7/8
en tu Learner Lab de AWS Academy, auto-calificado al terminar.

## 📊 Rúbrica (10 %)

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `vpc_subredes` | VPC `10.20.0.0/16` y 4 subredes con CIDR/AZ exactos | 1,0 |
| 2 | `salida_publica` | IGW adjunto; ruta pública `0.0.0.0/0`; 2 subredes públicas | 1,0 |
| 3 | `sg_web` | 80/443 públicos; SSH solo desde `10.20.0.0/16` | 1,0 |
| 4 | `sg_db` | 5432 solo desde `sg-web`; sin `0.0.0.0/0` | 1,0 |
| 5 | `privadas_sin_salida` | privadas sin IP pública ni ruta `0.0.0.0/0` | 1,0 |

## 🔗 Enlaces

- [Guía completa en la plataforma de labs](https://labs.proyectoasur.org/guia/lab-02-vpc-subredes)
- [Lab AWS — red VPC en AWS Academy](https://awsacademy.instructure.com/courses/181773/modules/items/17915781) (Módulos 7 y 8)
- [Acceso SSH al lab de VPC — PEM y PPK](../acceso-ssh-lab-vpc.html)
- [Plataforma de labs](https://labs.proyectoasur.org/)
