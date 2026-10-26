# 🧪 Lab 6 — Alta disponibilidad, escalado e IaC

**Asignatura:** Arquitectura en la Nube 2026-2 · **Semana del curso:** 10 (Unidad 2)
**Valor:** 10 % · Corte 2 · Actividad 3
**Módulo AWS Academy:** Módulo 10 — High Availability (lab de desafíos «entorno escalable/HA»)

## 🎯 Objetivo

Desplegar con **CloudFormation** una red de dos zonas con un **balanceador ALB**
y completar el despliegue con un **launch template** y un **Auto Scaling Group**
que sirve la página desde dos instancias: escalado horizontal con redundancia y
cambios repetibles.

## ✅ Prerrequisitos

- Semana 10: [deck Elasticidad, HA y monitorización](../../2026-2-S10-arquitectura-nube-elasticidad-ha-monitorizacion.html) · [PDF](../../2026-2-S10-arquitectura-nube-elasticidad-ha-monitorizacion.pdf) · [video parte 1](../../videos/2026-2-S10-arquitectura-nube-elasticidad-ha-monitorizacion-parte1.mp4) · [parte 2](../../videos/2026-2-S10-arquitectura-nube-elasticidad-ha-monitorizacion-parte2.mp4) · [parte 3](../../videos/2026-2-S10-arquitectura-nube-elasticidad-ha-monitorizacion-parte3.mp4)
- Haber hecho los Labs 2 y 4 (red por capas y servidor web).
- Leer una plantilla de CloudFormation: pila, recursos, parámetros y salidas.

## 🛠️ Pasos

**[Guía completa del Lab 6 — Alta disponibilidad, escalado e IaC](https://labs.proyectoasur.org/guia/lab-06-alta-disponibilidad)**:

1. **Leer la plantilla** de CloudFormation (red, ALB, grupos y salidas).
2. **Crear la pila** y esperar el `CREATE_COMPLETE`.
3. Crear el **launch template** (AMI y `user-data` con la página).
4. Crear el **Auto Scaling Group** (mínimo 2, máximo 4, deseado 2).
5. Comprobar el **ALB** y que las dos instancias sirven la página (HTTP 200).
6. Autocontrol con `revisar` (5 de 5).

## 📦 Entregable

Pila desplegada con ALB y dos instancias sirviendo la página (plataforma), o el
lab de desafíos «entorno escalable/HA» del Módulo 10 en tu Learner Lab.

## 📊 Rúbrica (10 %)

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `stack` | la pila está en `CREATE_COMPLETE` | 1,0 |
| 2 | `asg` | mínimo 2 / máximo 4 / deseado 2, con ≥ 2 instancias | 1,0 |
| 3 | `launch_template` | plantilla con su AMI y `user-data` con la página | 1,0 |
| 4 | `alb` | 2 zonas, listener 80 y target group HTTP/80 | 1,0 |
| 5 | `instancias_sirven` | ≥ 2 instancias responden 200 con la marca | 1,0 |

## 🔗 Enlaces

- [Guía completa en la plataforma de labs](https://labs.proyectoasur.org/guia/lab-06-alta-disponibilidad)
- [Lab AWS — entorno escalable/HA en AWS Academy](https://awsacademy.instructure.com/courses/181773/modules/items/17915863) (Módulo 10)
- [Plataforma de labs](https://labs.proyectoasur.org/)
