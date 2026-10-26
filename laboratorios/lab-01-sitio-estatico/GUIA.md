# Lab 1 — Almacenamiento y sitio estático en la nube

**Asignatura:** Arquitectura en la Nube HEP · **Semana:** 1
**Duración estimada:** 75–90 min · **Entrega:** individual, en la plataforma
**Estación:** nube AWS simulada con `floci` (sin cuenta de AWS y sin Internet)

---

## 1. Qué vas a aprender

En este laboratorio vas a usar el almacenamiento de objetos de la nube como si
fuera Amazon S3:

- crear un **bucket** y comprobar su región;
- activar **versionado** y demostrar que un objeto tiene dos versiones;
- publicar un **sitio estático** con los **tipos MIME** correctos;
- comprobar el sitio por HTTP, tanto en la terminal como en la pestaña
  **Sitio web** de tu sesión;
- entender qué hace S3 real y qué no emula la nube de la estación.

No necesitas tarjeta de crédito, cuenta de AWS ni conexión a Internet. La nube
vive dentro de tu estación, en `http://127.0.0.1:4566`.

---

## 2. El entorno

Tu estación trae:

| Pieza | Para qué |
|---|---|
| `floci` | API local compatible con AWS, en `http://127.0.0.1:4566` |
| `aws` (wrapper) | AWS CLI que ya apunta al endpoint local |
| `curl`, `jq` | Comprobar el sitio y leer JSON |
| `docker` | Ver los contenedores internos de la nube (no hace falta tocarlos) |
| `revisar` | Autocontrol con los mismos 5 criterios del servidor |

Credenciales **dummy** (no son secretos, no hay cuenta real):

```text
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=us-east-1
AWS_ENDPOINT_URL=http://127.0.0.1:4566
```

En una terminal nueva ya vienen exportadas. Si abres una shell que no las tiene:

```bash
source /etc/profile.d/lab-aws.sh
```

El bucket de este laboratorio se llama **`sitio-hep`**. Ese nombre es fijo: la
vista web de la sesión lo usa para mostrar tu sitio.

Los archivos de partida están en `~/sitio` (`/workspace/sitio`):

```text
sitio/
├── index.html    ← página de inicio (ya trae la marca CaribeMart HEP)
├── error.html    ← página de error (ya trae "No encontrado")
├── estilo.css    ← hoja de estilos
└── LEEME.md
```

---

## 3. Antes de empezar

Comprueba que la nube responde y que todavía no hay buckets:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:4566/
aws s3 ls
```

La primera orden debe imprimir `200` (o `404`, según la versión de floci: lo
importante es que **algo** responda). La segunda no debe listar nada: tu nube
empieza vacía.

> **Si `aws` dice «Unable to locate credentials»**: ejecuta
> `source /etc/profile.d/lab-aws.sh` y vuelve a probar. El wrapper `aws` ya
> añade `--endpoint-url`; no hace falta escribirlo en cada comando.

---

## 4. Paso 1 — Crear el bucket

```bash
aws s3api create-bucket --bucket sitio-hep
aws s3api head-bucket --bucket sitio-hep && echo "bucket OK"
aws s3api get-bucket-location --bucket sitio-hep
```

`us-east-1` es la región por defecto y no necesita `LocationConstraint` (en
otras regiones sí). La respuesta de `get-bucket-location` puede traer
`LocationConstraint: null`: significa «us-east-1».

**Criterio 1:** el bucket `sitio-hep` existe en `us-east-1`.

---

## 5. Paso 2 — Activar versionado

```bash
aws s3api put-bucket-versioning \
  --bucket sitio-hep \
  --versioning-configuration Status=Enabled

aws s3api get-bucket-versioning --bucket sitio-hep
```

Debe responder `"Status": "Enabled"`. El versionado guarda **cada subida** de
un objeto; no se activa solo y no se puede «simular» subiendo dos archivos con
nombres distintos.

**Criterio 2:** versionado `Enabled` **y** `index.html` con al menos dos
versiones.

---

## 6. Paso 3 — Publicar los objetos con su Content-Type

S3 guarda el tipo MIME **en el momento de la subida**, como metadato del
objeto. Que el archivo se llame `.css` no basta: hay que declararlo. Usa
`s3api put-object` para no depender de lo que adivine la CLI:

```bash
cd ~/sitio

aws s3api put-object --bucket sitio-hep --key index.html \
  --body index.html --content-type "text/html; charset=utf-8"

aws s3api put-object --bucket sitio-hep --key error.html \
  --body error.html --content-type "text/html; charset=utf-8"

aws s3api put-object --bucket sitio-hep --key estilo.css \
  --body estilo.css --content-type "text/css; charset=utf-8"
```

Comprueba los metadatos:

```bash
aws s3api head-object --bucket sitio-hep --key index.html
aws s3api head-object --bucket sitio-hep --key estilo.css
```

**Criterio 3:** `index.html`, `error.html` y `estilo.css` existen y su
`ContentType` es `text/html…` para los dos primeros y `text/css…` para el
tercero.

---

## 7. Paso 4 — Segunda versión de index.html

El versionado se demuestra con **dos subidas distintas** del mismo objeto.
Edita `~/sitio/index.html`, busca la línea:

```html
Versión del sitio: <strong>borrador</strong>.
```

y cámbiala por algo como:

```html
Versión del sitio: <strong>1.0 — publicada</strong>.
```

Vuelve a subir el archivo:

```bash
aws s3api put-object --bucket sitio-hep --key index.html \
  --body index.html --content-type "text/html; charset=utf-8"
```

Y lista las versiones:

```bash
aws s3api list-object-versions --bucket sitio-hep --prefix index.html
```

Deben aparecer **dos** entradas en `Versions` para la clave `index.html`, con
`VersionId` distintos y la más reciente marcada como `"IsLatest": true`.

**Criterio 2 (completo):** versionado activo y dos versiones del index.

---

## 8. Paso 5 — Configurar el sitio web

En S3 real, el «website hosting» se configura en el bucket con un documento de
índice y uno de error. Hazlo también aquí:

```bash
aws s3api put-bucket-website --bucket sitio-hep \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"}
  }'

aws s3api get-bucket-website --bucket sitio-hep
```

### Una limitación que debes conocer (y explicar)

La nube de la estación **guarda** la configuración del sitio, pero **no la
aplica** al servir:

- `GET /sitio-hep/` devuelve el listado XML del bucket, no `index.html`;
- una clave inexistente devuelve un XML de error de S3, no tu `error.html`.

Por eso el laboratorio comprueba las URLs **directas** de los objetos:

```text
http://127.0.0.1:4566/sitio-hep/index.html
http://127.0.0.1:4566/sitio-hep/error.html
```

Esto es una diferencia entre el emulador y AWS real. En AWS real, con
`IndexDocument` y `ErrorDocument`, el sitio resolvería `/` y los 404 con tus
páginas. En la guía de entrega explica en una frase qué cambiaría en AWS real.

---

## 9. Paso 6 — Comprobar el sitio

Por HTTP, desde la terminal:

```bash
curl -i http://127.0.0.1:4566/sitio-hep/index.html
curl -i http://127.0.0.1:4566/sitio-hep/error.html
curl -i http://127.0.0.1:4566/sitio-hep/estilo.css
```

- `index.html` → `200 OK`, `Content-Type: text/html…`, cuerpo con
  `CaribeMart HEP`.
- `error.html` → `200 OK`, cuerpo con `No encontrado`.
- `estilo.css` → `200 OK`, `Content-Type: text/css…`.

En la pestaña **Sitio web** de la plataforma verás el mismo sitio a través del
proxy de la sesión (`http://127.0.0.1:8080/`); el proxy traduce `/` a
`index.html`.

Y el autocontrol:

```bash
revisar
```

Debe terminar con **5 de 5 criterios en verde**. Si falta alguno, el detalle te
dice exactamente qué corregir.

> `revisar` es un autocontrol formativo: aplica los mismos criterios que el
> servidor, pero la nota oficial la calcula el servidor **desde fuera** de tu
> sesión. No intentes «aprobar» el script: mira el estado real de tu nube.

---

## 10. Criterios de evaluación

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `bucket_creado` | `sitio-hep` existe en `us-east-1` | 1,0 |
| 2 | `versionado` | `Status=Enabled` y ≥2 versiones de `index.html` | 1,0 |
| 3 | `objetos` | los 3 objetos existen con su `Content-Type` | 1,0 |
| 4 | `sitio_responde` | `GET …/index.html` → 200 con `CaribeMart HEP` | 1,0 |
| 5 | `error_accesible` | `GET …/error.html` → 200 con `No encontrado` | 1,0 |

Total: **5,0**. Cada criterio vale 1,0 y es automático.

---

## 11. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `Unable to locate credentials` | shell sin el perfil del lab | `source /etc/profile.d/lab-aws.sh` |
| `head-bucket` da 404 | el bucket no se creó o se creó en otro endpoint | `aws s3 ls`; usa el wrapper `aws` |
| `head-object` da 404 | la clave no coincide (mayúsculas, ruta) | `aws s3api list-objects-v2 --bucket sitio-hep` |
| `ContentType` vacío o `binary/octet-stream` | subiste con `s3 cp` sin tipo | vuelve a subir con `--content-type` |
| `list-object-versions` muestra 1 | solo has subido el index una vez | edita el texto y súbelo otra vez |
| `curl` da 404 en el objeto | floci aún arrancando o clave mal escrita | `curl -s http://127.0.0.1:4566/`; espera unos segundos |
| La pestaña Sitio web da 503 | el proxy no encuentra el bucket/objeto | sube `index.html`; recarga |
| `revisar` dice 4/5 | lee el detalle del criterio en rojo | corrige y vuelve a ejecutar |

Si la nube no responde en absoluto:

```bash
curl -sv http://127.0.0.1:4566/ 2>&1 | head
docker ps
```

Y si sigue caída, avisa al docente: no reinicies nada de la plataforma.

---

## 12. Para ir más allá (opcional, no se califica)

- Añade una **bucket policy** que permita `s3:GetObject` solo a `index.html` y
  `error.html` (`aws s3api put-bucket-policy`).
- Crea una **regla de ciclo de vida** que expire versiones antiguas
  (`put-bucket-lifecycle-configuration`).
- Sube un cuarto objeto `aviso.txt` y comprueba que `Content-Type: text/plain`
  también se guarda.
- Compara `s3 cp` con `s3api put-object`: ¿en qué caso se adivina el MIME y en
  cuál lo declaras tú?

---

## 13. Entrega

No hay que subir archivos: el servidor evalúa el **estado de tu nube**. Antes
de cerrar la sesión, ejecuta `revisar` y asegúrate de ver **5 de 5**. La nota
del laboratorio se calcula con esos cinco criterios automáticos.

Si trabajas fuera de la plataforma, el verificador del host es:

```bash
python3 catalog/arquitectura-nube-hep/lab-01-sitio-estatico/bin/verificador.py \
  --contenedor <nombre-de-tu-estación>
```
