#!/usr/bin/env bash
# =============================================================================
# devstack-lab-install.sh - OpenStack (DevStack) para laboratorio, Ubuntu 24.04
# Arquitectura en la Nube - CUC 2026-2
#
# Fuentes oficiales:
#  - DevStack: https://docs.openstack.org/devstack/latest/
#    ("Ubuntu 24.04 (Noble) is the most tested"; usuario stack:
#     useradd -s /bin/bash -d /opt/stack -m stack; sudoers NOPASSWD;
#     local.conf [[local|localrc]] con ADMIN_PASSWORD/DATABASE_PASSWORD/
#     RABBIT_PASSWORD/SERVICE_PASSWORD; luego ./stack.sh como usuario stack)
#  - Series y estado: https://releases.openstack.org/
#  - Runtime probado 2026.1 (Ubuntu 24.04): 
#    https://governance.openstack.org/tc/reference/runtimes/2026.1.html
#  Rama por defecto: stable/2026.1 (SLURP, mantenida; existe en opendev.org).
#
# Uso:  bash devstack-lab-install.sh [--aws] [--lite] [--public-ip IP] [--ip IP] [--branch RAMA]
#                                    [--password CLAVE] [--iface IFACE] [--no-post] [--yes] [--help]
#  --lite: para 4-5 GB de RAM (sin Cinder, un proceso por servicio, swap de 8 GB).
#  --aws: --lite + IP publica de la EC2 (Sandbox de AWS Academy, t3.medium, 35 GB).
#  --public-ip: IP con la que el navegador llega a la VM (consola de Horizon y resumen).
# Variables de entorno equivalentes: HOST_IP, BRANCH, ADMIN_PASSWORD, IFACE.
# Ejecutar como usuario normal con sudo (NO como root). Crea el usuario "stack".
# =============================================================================
set -Eeuo pipefail

BRANCH="${BRANCH:-stable/2026.1}"
HOST_IP="${HOST_IP:-}"
IFACE="${IFACE:-}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-}"
DO_POST=1
LITE=0
AWS=0
PUBLIC_IP="${PUBLIC_IP:-}"
ASSUME_YES=0
STACK_USER="stack"
STACK_HOME="/opt/stack"
DEVSTACK_DIR="${STACK_HOME}/devstack"
LOG_FILE="${LOG_FILE:-$HOME/devstack-install.log}"
MIN_RAM_MB=7500      # ~8 GB reales
MIN_DISK_GB=40

C_R=$'\033[0;31m'; C_G=$'\033[0;32m'; C_Y=$'\033[1;33m'; C_C=$'\033[0;36m'; C_N=$'\033[0m'
log()  { printf '%s\n' "$*" >>"$LOG_FILE"; }
info() { printf '%s[INFO]%s %s\n' "$C_C" "$C_N" "$*"; log "[INFO] $*"; }
ok()   { printf '%s[OK]%s   %s\n' "$C_G" "$C_N" "$*"; log "[OK] $*"; }
warn() { printf '%s[AVISO]%s %s\n' "$C_Y" "$C_N" "$*"; log "[AVISO] $*"; }
die()  { printf '%s[ERROR]%s %s\n' "$C_R" "$C_N" "$*" >&2; log "[ERROR] $*"; exit 1; }
trap 'die "Fallo en la linea $LINENO. Revisa el log: $LOG_FILE"' ERR

uso() { sed -n '/^# Uso:/,/^# Ejecutar/p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    --ip)       HOST_IP="${2:?falta valor}"; shift 2 ;;
    --branch)   BRANCH="${2:?falta valor}"; shift 2 ;;
    --password) ADMIN_PASSWORD="${2:?falta valor}"; shift 2 ;;
    --iface)    IFACE="${2:?falta valor}"; shift 2 ;;
    --no-post)  DO_POST=0; shift ;;
    --lite)     LITE=1; shift ;;
    --aws)      AWS=1; LITE=1; shift ;;
    --public-ip) PUBLIC_IP="${2:?falta valor}"; shift 2 ;;
    --yes|-y)   ASSUME_YES=1; shift ;;
    -h|--help)  uso ;;
    *) die "Opcion desconocida: $1 (usa --help)" ;;
  esac
done

: >>"$LOG_FILE" 2>/dev/null || die "No puedo escribir el log en $LOG_FILE"

# ---------------------------------------------------------------- Chequeos ---
[ "$LITE" -eq 0 ] || { MIN_RAM_MB=3500; MIN_DISK_GB=25; }
info "Chequeos previos..."
[ "$(id -u)" -ne 0 ] || die "No ejecutes como root. Usa un usuario normal con sudo; el script crea el usuario '$STACK_USER'."
sudo true || die "Se necesita sudo."
# shellcheck disable=SC1091
. /etc/os-release
[ "${ID:-}" = "ubuntu" ] && [ "${VERSION_ID:-}" = "24.04" ] \
  || die "Este script es para Ubuntu 24.04 LTS (detectado: ${PRETTY_NAME:-desconocido})."
[ "$(uname -m)" = "x86_64" ] || warn "Arquitectura $(uname -m): DevStack se prueba en x86_64."

RAM_MB=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
[ "$RAM_MB" -ge "$MIN_RAM_MB" ] || {
  warn "RAM detectada: ${RAM_MB} MB (recomendado >= 8 GB). Puede fallar o ir muy lento."
  if [ "$ASSUME_YES" -ne 1 ]; then read -rp "Continuar de todos modos? [s/N] " r; [[ "$r" =~ ^[sSyY]$ ]] || exit 1; fi; }
DISK_GB=$(df -BG --output=avail / | tail -1 | tr -dc '0-9')
[ "$DISK_GB" -ge "$MIN_DISK_GB" ] || die "Disco libre en /: ${DISK_GB} GB (minimo ${MIN_DISK_GB} GB)."
NCPU=$(nproc); [ "$LITE" -eq 1 ] || [ "$NCPU" -ge 4 ] || warn "Solo $NCPU vCPU (recomendado 4)."
getent hosts opendev.org >/dev/null || die "Sin DNS/Internet (no resuelve opendev.org)."
curl -fsI --max-time 15 https://opendev.org >/dev/null || die "Sin salida HTTPS a opendev.org."
ok "Ubuntu ${VERSION_ID}, ${RAM_MB} MB RAM, ${NCPU} vCPU, ${DISK_GB} GB libres."

# ------------------------------------------------- Deteccion de red/host ---
if [ -z "$IFACE" ]; then
  IFACE=$(ip -4 route show default | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1); exit}}')
fi
[ -n "$IFACE" ] || die "No encontre interfaz con ruta por defecto. Usa --iface."
if [ -z "$HOST_IP" ]; then
  HOST_IP=$(ip -4 -o addr show dev "$IFACE" scope global | awk '{print $4}' | cut -d/ -f1 | head -n1)
fi
[[ "$HOST_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "IP invalida o no detectada ('$HOST_IP'). Usa --ip."
ip -4 -o addr show | grep -qw "$HOST_IP" || warn "La IP $HOST_IP no esta en ninguna interfaz local."
if [ "$AWS" -eq 1 ] && [ -z "$PUBLIC_IP" ]; then
  TOKEN=$(curl -fsS -m 5 -X PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 60')
  PUBLIC_IP=$(curl -fsS -m 5 -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4) \
    || die "No pude leer la IP publica de la EC2. Usa --public-ip."
fi
BROWSER_IP="${PUBLIC_IP:-$HOST_IP}"
HOSTNAME_NOW=$(hostname)
ok "Interfaz: $IFACE | IP: $HOST_IP | hostname: $HOSTNAME_NOW"

# Contrasena: la dada, la ya usada en un local.conf previo, o una aleatoria.
PREV_CONF="${DEVSTACK_DIR}/local.conf"
if [ -z "$ADMIN_PASSWORD" ] && sudo test -f "$PREV_CONF"; then
  ADMIN_PASSWORD=$(sudo awk -F= '/^ADMIN_PASSWORD=/{print $2; exit}' "$PREV_CONF")
  [ -n "$ADMIN_PASSWORD" ] && info "Reutilizo la contrasena del local.conf existente."
fi
if [ -z "$ADMIN_PASSWORD" ]; then
  ADMIN_PASSWORD=$(openssl rand -hex 12)
  info "Contrasena de admin generada aleatoriamente."
fi
[[ "$ADMIN_PASSWORD" =~ ^[A-Za-z0-9._@+-]{8,}$ ]] \
  || die "La contrasena debe tener >= 8 caracteres y solo A-Z a-z 0-9 . _ @ + - (DevStack falla con otros)."

# ----------------------------------------------------------- Confirmacion ---
if [ "$ASSUME_YES" -ne 1 ]; then
  printf '\nSe instalara OpenStack (%s) en %s. Tarda 30-60 min. Log: %s\n' "$BRANCH" "$HOST_IP" "$LOG_FILE"
  read -rp "Continuar? [s/N] " r; [[ "$r" =~ ^[sSyY]$ ]] || exit 0
fi

# ------------------------------------------------------ Sistema (idempotente)
info "Preparando sistema (apt, hostname, usuario $STACK_USER)..."
# El hostname debe resolver localmente (DevStack/RabbitMQ lo requieren). No se cambia el hostname.
grep -qw "$HOSTNAME_NOW" /etc/hosts || echo "127.0.1.1 $HOSTNAME_NOW" | sudo tee -a /etc/hosts >/dev/null
sudo systemctl disable --now unattended-upgrades >>"$LOG_FILE" 2>&1 || true
while sudo fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do warn "apt ocupado, espero 5 s..."; sleep 5; done
sudo apt-get update -y >>"$LOG_FILE" 2>&1
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git curl openssl iproute2 lsb-release >>"$LOG_FILE" 2>&1
id -u "$STACK_USER" >/dev/null 2>&1 || sudo useradd -s /bin/bash -d "$STACK_HOME" -m "$STACK_USER"
echo "$STACK_USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack >/dev/null
sudo chmod 0440 /etc/sudoers.d/stack
sudo chmod 755 "$STACK_HOME"     # DevStack falla si /opt/stack es 700
if [ "$LITE" -eq 1 ] && [ "$(swapon --noheadings | wc -l)" -eq 0 ]; then
  info "Creando swap de 8 GB (modo lite)..."
  sudo fallocate -l 8G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile >>"$LOG_FILE" 2>&1 && sudo swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi
ok "Sistema listo."

# ----------------------------------------------------------- DevStack git ---
info "DevStack rama $BRANCH..."
if [ ! -d "$DEVSTACK_DIR/.git" ]; then
  sudo -u "$STACK_USER" -H git clone https://opendev.org/openstack/devstack -b "$BRANCH" "$DEVSTACK_DIR" >>"$LOG_FILE" 2>&1 \
    || die "No pude clonar la rama '$BRANCH'. Ramas: git ls-remote --heads https://opendev.org/openstack/devstack"
else
  CUR=$(sudo -u "$STACK_USER" git -C "$DEVSTACK_DIR" rev-parse --abbrev-ref HEAD)
  [ "$CUR" = "$BRANCH" ] || die "DevStack ya esta en '$CUR' y pediste '$BRANCH'. Borra $DEVSTACK_DIR (o usa --branch $CUR)."
  sudo -u "$STACK_USER" -H git -C "$DEVSTACK_DIR" pull --ff-only >>"$LOG_FILE" 2>&1 || warn "git pull fallo; sigo con lo local."
fi
ok "DevStack listo."

# -------------------------------------------------------------- local.conf ---
# Con DevStack en rama stable/X, los demas proyectos usan la misma rama
# automaticamente (no se fijan *_BRANCH). Red por defecto de DevStack: OVN,
# red publica 172.24.4.0/24 y privada 10.0.0.0/22 (accesibles desde esta VM).
info "Generando local.conf..."
sudo -u "$STACK_USER" tee "$PREV_CONF" >/dev/null <<CONF
[[local|localrc]]
HOST_IP=${HOST_IP}
ADMIN_PASSWORD=${ADMIN_PASSWORD}
DATABASE_PASSWORD=${ADMIN_PASSWORD}
RABBIT_PASSWORD=${ADMIN_PASSWORD}
SERVICE_PASSWORD=${ADMIN_PASSWORD}
LOGFILE=${STACK_HOME}/logs/stack.sh.log
LOG_COLOR=False
enable_service horizon
disable_service tempest
$( [ "$LITE" -eq 1 ] && printf 'disable_service c-api c-vol c-sch c-bak\nAPI_WORKERS=1' )
$( [ -n "$PUBLIC_IP" ] && printf 'NOVNCPROXY_URL=http://%s:6080/vnc_lite.html' "$PUBLIC_IP" )
CONF
sudo chmod 600 "$PREV_CONF"

# ---------------------------------------------------------------- stack.sh ---
MARK="${STACK_HOME}/.stack-done-${BRANCH//\//_}"
if sudo test -f "$MARK"; then
  ok "stack.sh ya se ejecuto con exito antes (marca $MARK). Omito la instalacion."
else
  info "Ejecutando stack.sh (30-60 min). Salida completa en $LOG_FILE"
  set +e
  sudo -u "$STACK_USER" -H bash -c "cd '$DEVSTACK_DIR' && ./stack.sh" 2>&1 | tee -a "$LOG_FILE" \
    | grep --line-buffered -E '^\+ ?functions|=====|stack.sh completed|ERROR|Error'
  rc_stack=${PIPESTATUS[0]}
  set -e
  [ "$rc_stack" -eq 0 ] && sudo test -f "$DEVSTACK_DIR/openrc" \
    || die "stack.sh no termino bien. Revisa $LOG_FILE y ${STACK_HOME}/logs/stack.sh.log. Puedes relanzar este script (es reanudable)."
  sudo touch "$MARK"
  ok "OpenStack instalado."
fi

# ----------------------------------------------------- Recursos opcionales ---
if [ "$DO_POST" -eq 1 ]; then
  info "Creando imagen Cirros, flavor, red, grupo de seguridad y keypair..."
  POST=$(mktemp); chmod 755 "$POST"
  cat >"$POST" <<'POSTEOF'
#!/usr/bin/env bash
set -Eeuo pipefail
cd /opt/stack/devstack
# shellcheck disable=SC1091
set +u   # openrc de DevStack no tolera set -u
source openrc admin admin >/dev/null
set -u
has() { "$@" >/dev/null 2>&1; }
# Imagen Cirros (DevStack ya sube una; si no, la descargo con la version de su stackrc)
if ! openstack image list -f value -c Name | grep -qi '^cirros'; then
  VER=$(grep -oE 'CIRROS_VERSION:-[0-9.]+' stackrc | head -1 | cut -d- -f2)
  [ -n "$VER" ] || { echo "No pude determinar CIRROS_VERSION; subo la imagen a mano."; exit 0; }
  curl -fsSL -o /tmp/cirros.img "https://download.cirros-cloud.net/${VER}/cirros-${VER}-x86_64-disk.img"
  openstack image create cirros --disk-format qcow2 --container-format bare --public --file /tmp/cirros.img
fi
has openstack flavor show m1.tiny || openstack flavor create m1.tiny --vcpus 1 --ram 512 --disk 1
has openstack network show lab-net || openstack network create lab-net
has openstack subnet show lab-subnet || openstack subnet create lab-subnet --network lab-net \
  --subnet-range 192.168.50.0/24 --dns-nameserver 8.8.8.8
has openstack router show lab-router || {
  openstack router create lab-router
  openstack router set lab-router --external-gateway public
  openstack router add subnet lab-router lab-subnet; }
if ! has openstack security group show lab-ssh-icmp; then
  openstack security group create lab-ssh-icmp --description "SSH e ICMP"
  openstack security group rule create lab-ssh-icmp --protocol icmp
  openstack security group rule create lab-ssh-icmp --protocol tcp --dst-port 22
fi
if ! has openstack keypair show lab-key; then
  openstack keypair create lab-key > /opt/stack/lab-key.pem
  chmod 600 /opt/stack/lab-key.pem
fi
POSTEOF
  if sudo -u "$STACK_USER" -H bash "$POST" >>"$LOG_FILE" 2>&1; then
    [ -f "${STACK_HOME}/lab-key.pem" ] && { sudo cp "${STACK_HOME}/lab-key.pem" "$HOME/lab-key.pem"; sudo chown "$(id -u):$(id -g)" "$HOME/lab-key.pem"; chmod 600 "$HOME/lab-key.pem"; }
    ok "Recursos creados (imagen cirros, m1.tiny, lab-net, lab-router, lab-ssh-icmp, lab-key)."
  else
    warn "Fallo la creacion de recursos; puedes crearlos desde Horizon. Detalle en $LOG_FILE"
  fi
  rm -f "$POST"
fi

# ---------------------------------------------------------------- Resumen ----
CRED="$HOME/devstack-credenciales.txt"
umask 077
cat >"$CRED" <<RES
Horizon : http://${BROWSER_IP}/dashboard
Usuario : admin   (tambien existe 'demo')
Clave   : ${ADMIN_PASSWORD}
Dominio : Default
Proyecto: admin
Llave SSH de las VMs: $HOME/lab-key.pem (keypair 'lab-key')
RES
printf '\n%s================ INSTALACION TERMINADA ================%s\n' "$C_G" "$C_N"
cat "$CRED"
printf '\nGuardado en %s | Log: %s\n' "$CRED" "$LOG_FILE"
printf 'Nota: DevStack es para laboratorio. Tras reiniciar la VM los servicios pueden no volver: ejecute de nuevo\n'
printf '      sudo -u stack -H bash -c "cd %s && ./stack.sh"  (o tome un snapshot de la VM al terminar).\n' "$DEVSTACK_DIR"
