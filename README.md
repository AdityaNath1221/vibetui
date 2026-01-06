# 🎧 VIBEtui

> A terminal-based music streaming client built for people who actually live in the terminal.

VIBEtui is a **Textual-powered TUI music player** that lets you search, queue, and stream music directly from your terminal using **mpv** as the playback engine.

No browsers.  
No bloated UI.  
Just vibes.

---

## ✨ Features (v1.0)

- 🔍 Search music directly from YouTube — no account, no official API required  
- 🎶 Play audio directly via `mpv`
- 📜 Queue management (play, pause, next)
- 🧭 Keyboard-driven navigation
- 🖥️ Clean, minimal TUI built with [Textual](https://textual.textualize.io/)
- 🎨 Custom styling with CSS
- 🧠 Simple, readable architecture (no overengineering)

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
├── vibetui.sh          # Shell script to run the application with just one command
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
- Linux / macOS (Windows users can run via WSL or using virtual machine)

### Setup

```bash
git clone https://github.com/AdityaNath1221/vibetui.git
cd vibetui
chmod +x ./vibetui.sh
```

> The shell script handles virtual environment setup and dependency installation.


### Run

```bash
./vibetui.sh
```

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