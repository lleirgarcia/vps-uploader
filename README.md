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
pip install -r requirements.txt
python server.py
```

## Cómo funciona

- Sirve `index.html` y una API en `http://localhost:7474`.
- `GET /api/projects` → lista las carpetas en `~/projects/` del VPS (vía `ssh`) o las locales en modo local.
- `POST /api/upload` → recibe `project` + `files[]`, detecta el tipo por extensión y los sube a:
  ```
  ~/media/<project>/<images|videos|docs|audio|other>/YYYYMMDD-HHMMSS-<nombre>.<ext>
  ```
  Si no se indica `project`, los deja directamente bajo `~/media/<tipo>/`.

Tipos detectados (primero por MIME type del navegador — desambigua `.webm` audio vs vídeo — y si no, por extensión):

- `images`: png, jpg, jpeg, gif, webp, heic, svg, bmp
- `videos`: mp4, mov, avi, mkv, webm, m4v
- `docs`: pdf, md, txt, doc, docx
- `audio`: webm, ogg, mp3, wav, m4a, opus, aac, flac
- `other`: cualquier otra extensión

## Grabación de audio y transcripción

- La web tiene una sección **Grabar audio** (MediaRecorder). Al parar, la grabación se añade a la lista de subida como un archivo más. Requiere contexto seguro (HTTPS o localhost) para que el navegador permita el micrófono; en el VPS se accede vía Tailscale Serve: `https://vps.tail31a1fc.ts.net:8443` (para quitarlo: `tailscale serve --https=8443 off`).
- En modo local, todo audio subido se **transcribe con faster-whisper** (modelo `small`, int8, CPU). La transcripción se guarda en un `.txt` junto al audio y se devuelve en la respuesta; la web la muestra y la copia al portapapeles automáticamente — lista para pegarla en una sesión de Claude Code.
- El modelo se carga en el primer audio (perezoso); la primera transcripción tarda unos segundos más.

Variables de entorno de transcripción: `WHISPER_MODEL` (default `small`), `WHISPER_LANG` (default `es`), `WHISPER_THREADS` (default `2`, para no acaparar los núcleos del VPS).

## Configuración

En `server.py`:

- `VPS_HOST = "vps"` — alias SSH del servidor.
- `VPS_MEDIA = "~/media"` — destino raíz en el VPS.
- Variables de entorno opcionales: `PORT` (por defecto `7474`), `HOST` (por defecto `0.0.0.0`).

<!-- AUTO-DOC START -->
## Estado actual

Mini app local (Flask + HTML estático) para subir ficheros al VPS por SCP, organizándolos automáticamente por proyecto y tipo. Funcional con soporte para pegado de imágenes desde portapapeles (Ctrl+V / ⌘+V) y modo local automático cuando se ejecuta dentro del VPS. Documentación completa; listo para usar.
<!-- AUTO-DOC END -->
