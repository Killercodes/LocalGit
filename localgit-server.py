from bottle import route, run, request, response, abort
import subprocess
import os

# Ensure this points to your folder containing app1.git
GIT_ROOT = "C:/localgit"

@route('/')
def index_dashboard():
    os.makedirs(GIT_ROOT, exist_ok=True)
    items = os.listdir(GIT_ROOT)
    # Exclude index.html itself from showing up as a repository
    repos = [i for i in items if i.endswith('.git') and os.path.isdir(os.path.join(GIT_ROOT, i))]
    
    repo_html_parts = []
    if not repos:
        repo_html_parts.append('<div class="empty-state"><h3>No repositories found</h3><p>Click "New repository" above to create your first bare git repository.</p></div>')
    else:
        base_url = "http://localhost:8080"
        for repo in sorted(repos):
            repo_url = f"{base_url}/{repo}"
            repo_html_parts.append(f"""
                <div class="repo-card" data-name="{repo}">
                    <div class="repo-info">
                        <a href="/{repo}/info/refs?service=git-upload-pack">{repo}</a>
                        <div class="repo-meta">Bare repository on disk ({GIT_ROOT}/{repo})</div>
                    </div>
                    <div class="url-box">
                        <input type="text" readonly value="{repo_url}" id="url-{repo}">
                        <button class="copy-btn" onclick="copyUrl('{repo_url}', this)">Copy</button>
                    </div>
                </div>
            """)
            
    # Read external index.html file
    html_path = os.path.join(GIT_ROOT, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            template = f.read()
        return template.replace('{{repo_list_html}}', "".join(repo_html_parts))
    else:
        return f"Error: index.html not found in {GIT_ROOT}"

@route('/new/<reponame:path>', method=['GET', 'POST'])
def create_repo(reponame):
    if not reponame.endswith('.git'):
        reponame += '.git'
    repo_path = os.path.join(GIT_ROOT, reponame)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        try:
            subprocess.run(['git', 'init', '--bare', repo_path], check=True)
        except Exception as e:
            response.status = 500
            return str(e)
    return f"Repository '{reponame}' created successfully"


@route('/<filepath:path>', method=['GET', 'POST'])
def git_gateway(filepath):
    env = os.environ.copy()
    env['GIT_PROJECT_ROOT'] = GIT_ROOT
    env['GIT_HTTP_EXPORT_ALL'] = '1'
    env['PATH_INFO'] = '/' + filepath
    env['REQUEST_METHOD'] = request.method
    env['QUERY_STRING'] = request.query_string
    env['CONTENT_TYPE'] = request.environ.get('CONTENT_TYPE', '')
    
    # Enable receive-pack service for pushes directly in python
    if 'git-receive-pack' in filepath or request.query.get('service') == 'git-receive-pack':
        env['SERVICE'] = 'git-receive-pack'
        # This overrides the repository-level config check in git-http-backend
        os.environ['GIT_CONFIG_PARAMETERS'] = "'http.receivepack=true'"
    
    body = request.body.read() if request.method == 'POST' else None
    env['CONTENT_LENGTH'] = str(len(body)) if body else '0'

    try:
        process = subprocess.Popen(
            ['git', 'http-backend'],
            stdin=subprocess.PIPE if body else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        stdout, stderr = process.communicate(input=body)
    except Exception as e:
        abort(500, f"Subprocess error: {str(e)}")

    # If git-http-backend threw an error, print it to your terminal console
    if stderr:
        print(f"GIT STDERR: {stderr.decode('latin1', errors='ignore')}")

    # Parse headers from git-http-backend output
    header_part, _, body_part = stdout.partition(b'\r\n\r\n')
    if not body_part:
        header_part, _, body_part = stdout.partition(b'\n\n')

    for line in header_part.decode('latin1', errors='ignore').split('\r\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            if key.lower() == 'status':
                response.status = int(val.strip().split()[0])
            else:
                response.set_header(key.strip(), val.strip())

    return body_part

if __name__ == '__main__':
    banner = """                                               
---------------------------------------------------------------------------------------                                                                                                                                                                                                                                                           
██      ▄▄▄   ▄▄▄▄  ▄▄▄  ▄▄    ▄████  ▄▄ ▄▄▄▄▄▄         ▄█████ ▄▄▄▄▄ ▄▄▄▄  ▄▄ ▄▄ ▄▄▄▄▄ ▄▄▄▄  
██     ██▀██ ██▀▀▀ ██▀██ ██   ██  ▄▄▄ ██   ██     ▄▄▄   ▀▀▀▄▄▄ ██▄▄  ██▄█▄ ██▄██ ██▄▄  ██▄█▄ 
██████ ▀███▀ ▀████ ██▀██ ██▄▄▄ ▀███▀  ██   ██           █████▀ ██▄▄▄ ██ ██  ▀█▀  ██▄▄▄ ██ ██    
______________________________________________________________________________                                                                                                                                                                               
"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    print(f"Starting Git HTTP server on http://localhost:8080 (Root: {GIT_ROOT})")
    run(host='localhost', port=8080, server='wsgiref')