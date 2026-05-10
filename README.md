# vps-uploader

Mini app local (Flask + HTML estático) para subir ficheros al VPS por SCP, organizándolos automáticamente por proyecto y tipo.

## Inicio rápido

```bash
./start.sh
```

Abre http://localhost:7474. El script crea `.venv/` e instala Flask si no existen. Asegúrate de cumplir los prerrequisitos de abajo antes de lanzarlo.

## Prerrequisitos

1. **Python 3.8+** con `venv`.
   - macOS: incluido (o `brew install python3`).
   - Debian/Ubuntu: `sudo apt install python3 python3-venv python3-pip`.

2. **Cliente SSH (`ssh`) y `scp`** — solo en modo remoto.
   - macOS: incluidos.
   - Debian/Ubuntu: `sudo apt install openssh-client`.

3. **Alias SSH `vps`** en `~/.ssh/config` — solo en modo remoto. Ejemplo:
   ```
   Host vps
     HostName <IP_O_DOMINIO>
     User <usuario>
     IdentityFile ~/.ssh/<tu_clave>
   ```
   La clave debe estar sin passphrase, o el agente SSH cargado:
   ```bash
   ssh-add ~/.ssh/<tu_clave>
   ```
   Verifica con `ssh vps echo ok`.

4. **En el VPS**: que exista `~/projects/` (para listar proyectos) y permisos de escritura en `~/media/` (destino de los ficheros).

> Si se ejecuta dentro del VPS (existe `/home/claude/projects`), el servidor entra automáticamente en **modo local**: escribe en `~/media/` directamente, sin ssh/scp. Solo hace falta el prerrequisito 1.

## Setup manual (alternativa a `start.sh`)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python server.py
```

## Cómo funciona

- Sirve `index.html` y una API en `http://localhost:7474`.
- `GET /api/projects` → lista las carpetas en `~/projects/` del VPS (vía `ssh`) o las locales en modo local.
- `POST /api/upload` → recibe `project` + `files[]`, detecta el tipo por extensión y los sube a:
  ```
  ~/media/<project>/<images|videos|docs|other>/YYYYMMDD-HHMMSS-<nombre>.<ext>
  ```
  Si no se indica `project`, los deja directamente bajo `~/media/<tipo>/`.

Tipos detectados:

- `images`: png, jpg, jpeg, gif, webp, heic, svg, bmp
- `videos`: mp4, mov, avi, mkv, webm, m4v
- `docs`: pdf, md, txt, doc, docx
- `other`: cualquier otra extensión

## Configuración

En `server.py`:

- `VPS_HOST = "vps"` — alias SSH del servidor.
- `VPS_MEDIA = "~/media"` — destino raíz en el VPS.
- Variables de entorno opcionales: `PORT` (por defecto `7474`), `HOST` (por defecto `0.0.0.0`).
