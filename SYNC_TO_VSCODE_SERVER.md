# Syncing BlockDAG Project to VS Code Server

**Your VS Code Server**: `http://noctusoft.dev:8443`  
**Access Token**: `kn8Dyd6zBClPU2kA`  
**GitHub Repo**: `https://github.com/rvegajr/BlockDAGAnal.git`

---

## Method 1: Clone on Server and Access via VS Code Server (Recommended)

### Step 1: SSH into Your Server

```bash
ssh your-username@noctusoft.dev
```

### Step 2: Navigate to Your Workspace Directory

```bash
# Create or navigate to your workspace directory
mkdir -p ~/workspaces
cd ~/workspaces
```

### Step 3: Clone the Repository

```bash
# Clone the BlockDAG repository
git clone https://github.com/rvegajr/BlockDAGAnal.git BlockDAG
cd BlockDAG
```

### Step 4: Access via VS Code Server

1. **Open your browser** and go to: `http://noctusoft.dev:8443`
2. **Enter your access token** if prompted: `kn8Dyd6zBClPU2kA`
3. **Click "Open Folder"** or use File → Open Folder
4. **Navigate to**: `/home/your-username/workspaces/BlockDAG`
5. **Click "OK"** to open the workspace

---

## Method 2: Use VS Code Remote SSH Extension (Alternative)

### Step 1: Install Remote SSH Extension

1. Open VS Code locally
2. Go to Extensions (Cmd+Shift+X)
3. Search for "Remote - SSH"
4. Install the extension

### Step 2: Configure SSH Connection

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Remote-SSH: Open SSH Configuration File"
3. Select your SSH config file (usually `~/.ssh/config`)
4. Add your server configuration:

```
Host noctusoft
    HostName noctusoft.dev
    User your-username
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

### Step 3: Connect to Server

1. Press `Cmd+Shift+P`
2. Type "Remote-SSH: Connect to Host"
3. Select "noctusoft"
4. Enter your SSH password if prompted
5. VS Code will connect to your server

### Step 4: Clone Repository on Server

1. In VS Code terminal (now connected to server):
```bash
cd ~/workspaces
git clone https://github.com/rvegajr/BlockDAGAnal.git BlockDAG
```

2. **Open Folder**: File → Open Folder → `/home/your-username/workspaces/BlockDAG`

---

## Method 3: Push from Local and Pull on Server

### Step 1: Ensure Local Repo is Up to Date

```bash
cd /Users/admin/Dev/Crypto/BlockDAG
git push origin main
```

### Step 2: On Your Server

```bash
# SSH into server
ssh your-username@noctusoft.dev

# Navigate to workspace
cd ~/workspaces

# Clone or pull latest
git clone https://github.com/rvegajr/BlockDAGAnal.git BlockDAG
# OR if already cloned:
cd BlockDAG
git pull origin main
```

### Step 3: Access via VS Code Server

Open `http://noctusoft.dev:8443` and open the BlockDAG folder.

---

## Setting Up VS Code Server Workspace

### Create Workspace File (Optional)

Create `BlockDAG.code-workspace` in the project root:

```json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "/usr/bin/python3",
    "files.exclude": {
      "**/__pycache__": true,
      "**/*.pyc": true,
      "**/node_modules": true
    }
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "ms-python.vscode-pylance",
      "ms-vscode.vscode-markdown"
    ]
  }
}
```

### Install Recommended Extensions

In VS Code Server, install:
- Python (for running simulation scripts)
- Pylance (Python language server)
- Markdown Preview Enhanced (for documentation)

---

## Syncing Changes

### From Local to Server

```bash
# On your local machine
cd /Users/admin/Dev/Crypto/BlockDAG
git add .
git commit -m "Your changes"
git push origin main

# On server (via VS Code Server terminal or SSH)
cd ~/workspaces/BlockDAG
git pull origin main
```

### From Server to Local

```bash
# On server (via VS Code Server terminal)
cd ~/workspaces/BlockDAG
git add .
git commit -m "Changes made on server"
git push origin main

# On local machine
cd /Users/admin/Dev/Crypto/BlockDAG
git pull origin main
```

---

## Troubleshooting

### VS Code Server Not Accessible

1. **Check if code-server is running:**
```bash
ssh your-username@noctusoft.dev
ps aux | grep code-server
```

2. **Start code-server if not running:**
```bash
# If using systemd
sudo systemctl start code-server

# Or manually
code-server --bind-addr 0.0.0.0:8443 --auth password
```

### Authentication Issues

- Verify the access token: `kn8Dyd6zBClPU2kA`
- Check if code-server requires password instead of token
- Review code-server configuration: `~/.config/code-server/config.yaml`

### Git Authentication

If you need to push from server:

```bash
# Set up SSH key or use HTTPS with token
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# For HTTPS (use GitHub personal access token)
git remote set-url origin https://YOUR_TOKEN@github.com/rvegajr/BlockDAGAnal.git
```

---

## Quick Setup Script

Save this as `setup-vscode-server.sh` on your server:

```bash
#!/bin/bash

# BlockDAG VS Code Server Setup Script

WORKSPACE_DIR="$HOME/workspaces"
PROJECT_DIR="$WORKSPACE_DIR/BlockDAG"
REPO_URL="https://github.com/rvegajr/BlockDAGAnal.git"

# Create workspace directory
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"

# Clone repository
if [ -d "$PROJECT_DIR" ]; then
    echo "Repository already exists. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO_URL" BlockDAG
fi

echo "✅ Setup complete!"
echo "📁 Project location: $PROJECT_DIR"
echo "🌐 Access VS Code Server: http://noctusoft.dev:8443"
echo "🔑 Access token: kn8Dyd6zBClPU2kA"
```

Run it:
```bash
chmod +x setup-vscode-server.sh
./setup-vscode-server.sh
```

---

## Recommended Workflow

### Daily Workflow

1. **Work locally** on your Mac
2. **Commit and push** changes to GitHub
3. **Pull on server** when you want to work via VS Code Server
4. **Or work directly on server** via VS Code Server and push from there

### Best Practice

- Keep GitHub as the **single source of truth**
- Always pull before starting work on server
- Always push before switching between local/server
- Use descriptive commit messages

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Access Token**: The token `kn8Dyd6zBClPU2kA` should be kept secure
2. **HTTPS**: Consider using HTTPS for code-server (port 8443 suggests HTTP)
3. **Firewall**: Ensure only trusted IPs can access port 8443
4. **SSH Keys**: Use SSH keys instead of passwords for server access
5. **Git Credentials**: Use SSH keys or GitHub tokens, not passwords

---

## Next Steps

Once synced:

1. ✅ Open project in VS Code Server
2. ✅ Install recommended extensions
3. ✅ Set up Python environment (if needed)
4. ✅ Configure git credentials
5. ✅ Start working!

---

*Last Updated: January 22, 2026*
