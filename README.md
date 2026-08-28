© 2026 Paul Fergus. Free for student and research use — commercial use is strictly prohibited.

# Deep Learning Concepts and Techniques (Computer Vision)

Module container for the lab programme. Build once, then open one URL to access every lab.

---

## Quick start (Windows)

You need [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running, with the **WSL2 backend** enabled (this is the default on modern Windows installs).

Open a terminal in this folder (PowerShell or Command Prompt is fine) and run:

```powershell
docker compose up --build
```

The first build will take 5–10 minutes. Subsequent starts are near-instant.

When you see lines like:

```
deep-learning-cv  | * Running on all addresses (0.0.0.0)
deep-learning-cv  | * Running on http://127.0.0.1:7144
```

open your browser to:

> **http://localhost:7144**

That's the lab launcher. Click any lab to open it in JupyterLab.

To stop the container, press `Ctrl+C` in the terminal, then run:

```powershell
docker compose down
```

---

## What's inside

```
deep-learning-cv/
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── requirements.txt
├── README.md
├── launcher/                  # Flask app that serves the landing page
│   ├── app.py
│   ├── labs.py                # Lab catalogue (edit to add labs)
│   └── templates/index.html
└── labs/                      # Lab notebooks (bind-mounted: your edits persist)
    └── lab01_perceptron_mlp/
        ├── lab01.ipynb
        ├── assets/            # diagrams
        └── data/              # local datasets
```

The `labs/` folder is bind-mounted, which means **your edits to notebooks persist on your host machine** even after the container stops. You can also version-control your work with git directly from outside the container.

---

## Common operations

| What | Command |
|------|---------|
| Build + start | `docker compose up --build` |
| Start (already built) | `docker compose up` |
| Start in background | `docker compose up -d` |
| Stop | `docker compose down` |
| Rebuild from scratch | `docker compose build --no-cache` |
| Open a shell inside the container | `docker compose exec module bash` |
| View logs | `docker compose logs -f` |

---

## Going directly to JupyterLab

The launcher is the recommended entry point, but if you want to skip it and go straight to JupyterLab:

> **http://localhost:7154/lab?token=deep-learning-cv**

---

## Troubleshooting

**"port is already allocated"**
Another container or program is using 7144 or 7154. Stop it, or edit the `ports` section of `docker-compose.yml` to map to different host ports (e.g. `"9000:7144"`).

**"docker: command not found"**
Docker Desktop isn't installed or isn't running. Start Docker Desktop from the Start menu.

**Notebook says "Kernel error"**
Click *Kernel → Restart Kernel* in JupyterLab. If that fails, check the container logs with `docker compose logs -f`.

**My edits disappeared**
You probably edited inside the container but didn't bind-mount the folder. Make sure you're using `docker compose up`, not `docker run` without volume flags. Files inside `labs/` always persist.

---

## Updating the module

The lecturer may push updates to lab content. To pull the latest:

```powershell
git pull
docker compose build
docker compose up
```

Your own work inside `labs/` is not overwritten unless you have edited a file that has also changed upstream (git will tell you).
