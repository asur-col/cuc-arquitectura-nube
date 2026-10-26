# 🧪 Lab 7 — Automatización de infraestructura (IaC)

**Asignatura:** Arquitectura en la Nube 2026-2 · **Semana del curso:** 11 (Unidad 2)
**Valor:** 10 % · Corte 2 · Actividad 4
**Módulo AWS Academy:** Módulo 11 — CloudFormation (lab de automatización, en tu Learner Lab)

> **Nota honesta:** este laboratorio **no tiene guía en la plataforma de labs de
> la universidad** (el catálogo llega hasta el Lab 6). Su fuente es el material
> del curso: la semana 11 (láminas 53–56 del deck y su video, parte 3) y el lab
> del Módulo 11 de AWS Academy. Los pasos de abajo son los de esas láminas; los
> criterios exactos de la rúbrica los publica el docente con la guía del lab.

## 🎯 Objetivo

Escribir, desplegar, **cambiar** y **vigilar** tú mismo una **pila de
CloudFormation**: dentro de una VPC de laboratorio, un servidor web en subred
pública protegido por un grupo de seguridad y un bucket de S3 cuyo nombre depende
de un **parámetro de entorno**, todo desde una sola plantilla YAML que entrega
salidas útiles (la dirección pública del servidor y el nombre del bucket).

## ✅ Prerrequisitos

- Semana 11: [deck IaC + repaso U2](../../2026-2-S11-arquitectura-nube-iac-repaso-u2.html) · [PDF](../../2026-2-S11-arquitectura-nube-iac-repaso-u2.pdf) · [video parte 1](../../videos/2026-2-S11-arquitectura-nube-iac-repaso-u2-parte1.mp4) · [parte 2](../../videos/2026-2-S11-arquitectura-nube-iac-repaso-u2-parte2.mp4) · [parte 3](../../videos/2026-2-S11-arquitectura-nube-iac-repaso-u2-parte3.mp4)
- Haber hecho el Lab 6 (ya desplegaste una pila completa).
- Saber qué es declarativo, idempotente, un conjunto de cambios y la deriva.

## 🛠️ Pasos (lámina «Laboratorio paso a paso», semana 11)

Seis comandos recorren todo el ciclo — validar, crear, consultar, cambiar,
vigilar y limpiar:

1. **Validar** la plantilla: `aws cloudformation validate-template --template-body file:…`
2. **Crear** la pila: `create-stack` con nombre, plantilla y parámetros (p. ej. `Entorno=dev`).
3. **Consultar** estado y salidas con `describe-stacks`, y verificar el servidor en el navegador.
4. **Cambiar** con un **conjunto de cambios** (p. ej. otro tamaño de instancia), revisarlo y solo entonces ejecutarlo.
5. **Vigilar la deriva**: modifica una regla del grupo de seguridad en la consola, ejecuta `detect-stack-drift` y consulta `describe-stack-resource-drifts`.
6. **Limpiar**: elimina la pila con `delete-stack` (dejar recursos activos cuesta dinero y es una mala práctica).

Si la pila termina en `ROLLBACK_COMPLETE`: abre los **eventos**, lee el **primer**
`CREATE_FAILED` (los demás suelen ser consecuencia), corrige, elimina y crea de
nuevo. Causas frecuentes: un AMI de otra región, permisos insuficientes (en AWS
Academy no se pueden crear roles: usa el rol y el perfil de instancia que indica
la guía) o un nombre de recurso que ya existe.

## 📦 Entregables (lámina «Entregables del laboratorio»)

1. **Plantilla YAML comentada** (parámetros, recursos y salidas).
2. Captura de la pila en `CREATE_COMPLETE` con las salidas visibles.
3. El **conjunto de cambios**: vista previa y tu decisión sobre si hubo reemplazo y por qué.
4. **Informe de deriva**: recurso modificado, valor esperado y valor real.
5. Evidencia de que **eliminaste la pila**, sin recursos residuales.

Consejo del deck: que tus capturas muestren el nombre de la pila y su estado; es
lo primero que se revisa.

## 📊 Rúbrica (10 %)

El laboratorio vale el **10 % de la nota**. Los criterios exactos **los publica
el docente con la guía**; como buenas prácticas se espera una plantilla válida y
legible, un despliegue reproducible, que expliques tus decisiones y que no
queden recursos activos.

## 🔗 Enlaces

- [Módulo 11 en AWS Academy](https://awsacademy.instructure.com/courses/181773/modules) (curso «Arquitectura en la Nube 2026-2», Learner Lab)
- [Deck de la semana 11](../../2026-2-S11-arquitectura-nube-iac-repaso-u2.html) — láminas «Laboratorio de IaC», «Laboratorio paso a paso», «Entregables del laboratorio» y «Cuando la pila falla»
- [Plataforma de labs](https://labs.proyectoasur.org/) (Labs 1–6, para practicar sin costo)
