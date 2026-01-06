# 🎧 VIBEtui

> A terminal-based music streaming client built for people who actually live in the terminal.

VIBEtui is a **Textual-powered TUI music player** that lets you search, queue, and stream music directly from your terminal using **mpv** as the playback engine. It streams audio only (no video) and is designed for keyboard-first usage.

No browsers.  
No bloated UI.  
Just vibes.

---

## ✨ Features (v1.0)

- 🔍 Search music directly from YouTube — no account, no official API required  
- 🎶 Play audio directly via `mpv`
- 📜 Queue management (add, play, pause, next/previous)
- 🧭 Keyboard-driven navigation
- 🖥️ Clean, minimal TUI built with [Textual](https://textual.textualize.io/)
- 🎨 Custom styling with CSS
- 🧠 Simple, readable architecture (no overengineering)

---

## Platform Support

**VIBEtui** currently supports:

- Arch Linux
- Ubuntu
- Debian
- Android (via Termux)

Windows support is **not yet available** due to mpv IPC differences.
It is planned for a future release.

---

## 🧱 Project Structure

```text
vibetui/
├── assets/             # Static ASCII title assets
│   ├── logo.txt        # Static ASCII title for home page
│   ├── queue.txt       # Static ASCII title for queue page
│   ├── trending.txt    # Static ASCII title for trending page
│   └── search.txt      # Static ASCII title for search page
├── mpv.py              # mpv controller
├── music_services.py   # Music data fetch controllers
├── VIBEtui.py          # Main TUI application
├── style.css           # Textual UI styling
├── requirements.txt    # pip requirements
├── README.md
├── LICENSE
└── .gitignore
```
Each component has a **clear responsibility**, keeping the codebase easy to understand and extend.

---

## 🚀 Installation & Usage

### Prerequisites

- Python 3.10+ and `pip` package manager
- `mpv` installed and available in **PATH**
- If using android, install `termux` from Google play store.

### System Dependencies

Before setting up the Python environment, install the required system packages:

**On Ubuntu/Debian:**
```bash
sudo apt install git python3 python3-pip python3-venv libmpv-dev mpv yt-dlp
```

**On Fedora/RHEL:**
```bash
sudo dnf install git python3-virtualenv mpv-libs-devel mpv
```

**On Arch Linux:**
```bash
sudo pacman -S git python python-pip mpv yt-dlp 
```

**On macOS:**
```bash
brew install git mpv yt-dlp
```

**On Android:**
```bash
pkg install git python python-pip mpv yt-dlp
```

**NOTE:** I have not yet tested on macOS or fedora as of yet.

### Setup

```bash
git clone https://github.com/AdityaNath1221/vibetui.git
cd vibetui

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install Python dependencies
pip install -r requirements.txt

```

### Run

```bash
source env/bin/activate
python3 VIBEtui.py
```

**Note:** Make sure all system dependencies (`mpv`, `libmpv-dev`) and Python packages are installed before running. In case of systems with `python` instead of `python3` just replace `python3` with `python`  

**Special Note:** For easier access, creating a bash script for automating the above running process is recommended for a better User Experience

---

## ⌨️ Controls

Navigation and actions are fully keyboard-driven.

- Move between sections using key bindings shown in the footer
- Select songs to add them to the queue
- Control playback without leaving the terminal

(Exact bindings may evolve as the project grows.)

--- 


## 🛠️ Tech Stack

- Python

- Textual – TUI framework

- mpv – media playback

- IPC – communication with mpv

--- 

## 🎯 Why This Project?

This project wasn’t built to chase trends or pad a résumé.
It’s part of my personality — it reflects what I actually want from a music streaming app.

VIBEtui isn’t a SaaS product.
It’s an **opinionated, terminal-first music player** built for people who enjoy owning their tools.

It was built to:

- Learn how real TUIs work
- Understand UI state management
- Integrate external processes via IPC
- Build something genuinely useful and fun

Sometimes, the best projects are the ones you build for yourself.
This is `v1.0` — the first of many versions to come.

---

## 📜 License

This project is licensed under the GNU General Public License (GPL).
You’re free to use, modify, and distribute it — as long as it stays open.

---

## 🙌 Acknowledgements

- [mpv](https://mpv.io/)

- [Textual](https://textual.textualize.io/)