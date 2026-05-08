# vps-uploader

Mini app local (Flask + HTML estático) para subir ficheros al VPS por SCP, organizándolos automáticamente por proyecto y tipo.

## Cómo funciona

- Sirve `index.html` y una API en `http://localhost:7474`.
- `GET /api/projects` → lista las carpetas en `~/projects/` del VPS (vía `ssh`).
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

## Requisitos

- Python 3 con `flask`.
- Acceso SSH configurado al host alias `vps` (en `~/.ssh/config`) con clave sin passphrase o agente cargado.
- En el VPS debe existir `~/projects/` (para el listado) y permisos de escritura en `~/media/`.

## Uso

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python server.py
```

Abre el navegador en `http://localhost:7474` (se abre solo al arrancar).

## Configuración

En `server.py`:

- `VPS_HOST = "vps"` — alias SSH del servidor.
- `VPS_MEDIA = "~/media"` — destino raíz en el VPS.
