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
```

### 5. How to Run
1. Open your terminal or Command Prompt inside `C:\localgit`
2. Run the server script:
```bash
python git_server.py
```
3. The server will boot up on http://localhost:8080 and automatically open your default web browser to the LocalGit dashboard.
<img width="1012" height="306" alt="image" src="https://github.com/user-attachments/assets/e2261ee1-5d3a-4ee6-9ab7-69dee8b6d4bc" />

### Using the Dashboard
#### Searching Repositories
- Type any keyword into the top input field ("Find a repository or type name for a new one...").
- The repository list below will filter dynamically in real-time as you type.

#### Creating New Repositories
1. Type your desired repository name into the same top input field (e.g., my-cool-project).
2. Click the New repository button.
3. The server will initialize a bare repository instantly in the background, display a success notification, and add the repository card to your dashboard without reloading the page.

### Connecting & Pushing via Git Bash
Each repository card on your dashboard includes a pre-formatted HTTP URL and a Copy button.
To link an existing local project on your machine to your LocalGit server and push it, open Git Bash inside your project folder and run:
```bash
# 1. Initialize git if not already done
git init

# 2. Add all your files and commit
git add .
git commit -m "Initial commit"

# 3. Link to your LocalGit server (replace 'my-cool-project.git' with your repo name)
git remote add origin http://localhost:8080/my-cool-project.git

# 4. Push your code (this will automatically sync and push to your local server)
git push -u origin master
```
