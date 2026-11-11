# LocalGit

LocalGit is a zero-dependency local Git server powered by Python and `git-http-backend`, featuring a responsive, GitHub-styled dashboard for managing and creating repositories locally.

---

## 💡 The Idea Behind LocalGit

Most self-hosted Git solutions (like Gitea, GitLab, or full-blown server setups) are heavy, require external databases, or take too much configuration to run locally. 

**LocalGit** solves this by acting as a lightweight, single-folder hub. It uses your system's native `git` utility via a Python Bottle CGI gateway, giving you a clean, GitHub-like web interface right on your machine (`http://localhost:8080`). It's perfect for offline development, testing hooks, or managing local scratchpads without internet dependency.

---

## 🛠️ Setup Guide

### 1. Prerequisites
Ensure you have the following installed and added to your system's PATH:
- **Python** (3.x)
- **Git**

### 2. Prepare the Directory
Create a folder on your drive named `C:\localgit`.

### 3. Get Bottle (Zero-Install Option)
Since LocalGit is designed to be self-contained without needing global `pip install` commands, you can make it completely portable:
1. Download the single-file micro-framework from [bottlepy.org/bottle.py](https://bottlepy.org/bottle.py).
2. Save it directly as `bottle.py` inside your `C:\localgit\` folder.

*(Alternatively, you can install it globally via terminal: `pip install bottle`)*

### 4. Project Files Structure
Your `C:\localgit\` folder should look like this:
```text
C:\localgit\
│
├── bottle.py         # Bottle micro-framework (or installed via pip)
├── index.html        # GitHub-styled web dashboard
└── localgit-server.py     # Python server & git-http-backend gateway
