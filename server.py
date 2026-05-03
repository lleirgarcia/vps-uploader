#!/usr/bin/env python3
import sys, os, shutil
from flask import Flask, request, jsonify, send_from_directory

import subprocess as sp
import datetime
import tempfile
import threading
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

VPS_HOST = "vps"
VPS_MEDIA = "~/media"

LOCAL_PROJECTS_DIR = "/home/claude/projects"
LOCAL_MEDIA_DIR = os.path.expanduser("~/media")
LOCAL_MODE = os.path.isdir(LOCAL_PROJECTS_DIR)

TYPES = {
    "images": {"png","jpg","jpeg","gif","webp","heic","svg","bmp"},
    "videos": {"mp4","mov","avi","mkv","webm","m4v"},
    "docs":   {"pdf","md","txt","doc","docx"},
}

def detect_subdir(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    for subdir, exts in TYPES.items():
        if ext in exts:
            return subdir
    return "other"

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/api/projects")
def list_projects():
    try:
        if LOCAL_MODE:
            projects = sorted(
                d for d in os.listdir(LOCAL_PROJECTS_DIR)
                if os.path.isdir(os.path.join(LOCAL_PROJECTS_DIR, d))
            )
            return jsonify(projects)
        r = sp.run(["ssh", VPS_HOST, "ls /home/claude/projects/"],
                   capture_output=True, text=True, timeout=5)
        projects = [p for p in r.stdout.strip().splitlines() if p]
        return jsonify(projects)
    except Exception:
        return jsonify([])

@app.route("/api/upload", methods=["POST"])
def upload():
    project = request.form.get("project", "").strip()
    files = request.files.getlist("files")
    results = []

    for f in files:
        if not f.filename:
            continue

        subdir = detect_subdir(f.filename)
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        if "." in f.filename:
            name, _, ext = f.filename.rpartition(".")
            new_name = f"{ts}-{name}.{ext}"
        else:
            new_name = f"{ts}-{f.filename}"

        if LOCAL_MODE:
            dest_dir  = os.path.join(LOCAL_MEDIA_DIR, project, subdir) if project else os.path.join(LOCAL_MEDIA_DIR, subdir)
            dest_path = os.path.join(dest_dir, new_name)
            try:
                os.makedirs(dest_dir, exist_ok=True)
                f.save(dest_path)
                results.append({"file": f.filename, "path": dest_path,
                                 "subdir": subdir, "ok": True})
            except Exception as e:
                results.append({"file": f.filename, "error": str(e), "ok": False})
            continue

        dest_dir  = f"{VPS_MEDIA}/{project}/{subdir}" if project else f"{VPS_MEDIA}/{subdir}"
        dest_path = f"{dest_dir}/{new_name}"

        sp.run(["ssh", VPS_HOST, f"mkdir -p {dest_dir}"],
               capture_output=True, timeout=10)

        suffix = os.path.splitext(f.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            f.save(tmp.name)
            tmp_path = tmp.name

        try:
            r = sp.run(["scp", tmp_path, f"{VPS_HOST}:{dest_path}"],
                       capture_output=True, text=True, timeout=120)
            if r.returncode == 0:
                results.append({"file": f.filename, "path": dest_path,
                                 "subdir": subdir, "ok": True})
            else:
                results.append({"file": f.filename, "error": r.stderr.strip(),
                                 "ok": False})
        finally:
            os.unlink(tmp_path)

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7474))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"\n  VPS Uploader → http://localhost:{port}\n  Ctrl+C para salir\n")
    app.run(host=host, port=port, debug=False, use_reloader=False)
