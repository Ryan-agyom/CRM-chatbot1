# Free CPU Deployment Guide for Chatbot + CRM

> Note: There is no truly unlimited free cloud inference service for modern Llama3 models. This guide shows the most practical way to run the project on free CPU-based cloud infrastructure while using `llama3.2:3b` and attempting `llama3` where possible. Expect limited performance and resource constraints.

## 1. Recommendation: Use Oracle Cloud Free Tier

Oracle Cloud provides an always-free compute instance that can run a CPU inference stack. It is the most reliable free option for a CPU-only deployment.

### 1.1 Sign up for Oracle Cloud Free Tier

1. Visit https://www.oracle.com/cloud/free/
2. Create an account and verify your identity.
3. Use the Free Tier offering with "Always Free" compute instances.

### 1.2 Create a Compute Instance

1. In the Oracle Cloud Console, go to **Compute > Instances**.
2. Create a new instance using Ubuntu 22.04 or a similar Linux image.
3. Choose the always-free VM shape (for example, Ampere A1 or an eligible Arm-based/Intel-based free CPU instance).
4. Add a public SSH key so you can connect via SSH.
5. Open HTTP/HTTPS and TCP port `8000` and `11434` in the instance's security rules.

## 2. Install the project and Ollama on the VM

SSH into the VM and run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git python3 python3-venv python3-pip npm
```

### 2.1 Install Ollama

If Ollama supports your VM's architecture, install it with the official script:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Then verify:

```bash
ollama version
```

### 2.2 Pull the required models

For CPU inference, `llama3.2:3b` is the practical choice. Pull it first:

```bash
ollama pull llama3.2:3b
```

If your instance has enough RAM and you want to test a larger model on a paid machine, do so only after the CPU-friendly setup works. This guide is focused on `llama3.2:3b`.

### 2.3 Start the Ollama daemon

Run the Ollama daemon and make it listen on all addresses:

```bash
ollama daemon --listen 0.0.0.0:11434
```

Leave this running, or convert it to a background process using `tmux`, `screen`, or a systemd service.

## 3. Deploy the backend on the same VM

### 3.1 Clone the repository

```bash
cd /home/ubuntu
git clone <your-github-repo-url> chatbot-crm
cd chatbot-crm/backend1
```

### 3.2 Install backend dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Configure backend environment variables

Create `backend1/.env` with these values:

```env
PORT=8000
OLLAMA_API_URL=http://127.0.0.1:11434
OLLAMA_API_KEY=
OLLAMA_CHAT_MODEL=llama3.2:3b
OLLAMA_INTENT_MODEL=llama3.2:3b
OLLAMA_SQL_MODEL=llama3.2:3b
```

If you manage to run a larger model successfully, update the model settings accordingly and keep the other CPU-safe models on `llama3.2:3b`.

### 3.4 Start the backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 4. Deploy the frontend using Vercel (free tier)

### 4.1 Create a Vercel account

1. Visit https://vercel.com/
2. Sign up with GitHub.
3. Import your repository.

### 4.2 Configure the frontend deployment

- Project root: `frontend`
- Build command: `npm install && npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_URL`
  - Example: `http://<your-vm-ip>:8000/api`

### 4.3 Deploy

Deploy the project. Vercel will give you a public frontend URL.

## 5. Alternative: Serve the frontend from the same VM

If you want to avoid Vercel, build the frontend locally and serve it from the VM:

```bash
cd /home/ubuntu/chatbot-crm/frontend
npm install
npm run build
npm install -g serve
serve -s dist -l 3000
```

Then point your browser to `http://<your-vm-ip>:3000`.

## 6. Update the frontend API URL

If the frontend is served externally, set `VITE_API_URL` to `http://<your-vm-ip>:8000/api` or your backend domain.

If the frontend is served on the same VM, add a simple proxy or use the full backend URL from `chatService.js`.

## 7. Validate the deployment

1. Open the frontend URL.
2. Use the chat widget.
3. Ask a sample prediction request:

```text
Predict conversion probability for a lead with budget 15000, industry saas, interest high.
```

4. Ask a sample CRUD request:

```text
Add lead: name=John Doe, email=john@example.com, industry=saas
```

5. Confirm the backend receives requests.

## 8. Important caveats

- **Unlimited usage is not real**: Free tiers and always-free VMs are limited by the provider. You can run the project without paying, but expect slow CPU inference and possible provider restrictions.
- **`llama3.2:3b` is the reliable CPU model**. Larger models are almost certainly too heavy for a small free CPU instance and will likely fail or be unusably slow.
- **CSV persistence is ephemeral on cloud VMs**. If the VM reboots, your dataset changes may be lost unless you use a persistent disk or migrate to a real database.
- **If you need better capacity**, consider a small paid instance or a paid hosted LLM service.

## 9. Recommended final setup

- Use `llama3.2:3b` for production CPU inference.
- Keep larger models only for offline testing or when you have a larger paid VM.
- Use Vercel for frontend and Oracle Cloud for the backend + Ollama stack.
- Save your backend's API URL in Vercel as `VITE_API_URL`.

## 10. What to do if the model fails

- If a larger model fails to load, switch to `llama3.2:3b`.
- If `ollama daemon` crashes, check available RAM and swap.
- If backend cannot connect, confirm `OLLAMA_API_URL` and open ports.

---

### Summary

This guide gives you the safest free path: use an always-free CPU VM, install Ollama, run `llama3.2:3b`, and host the frontend with Vercel. True unlimited cloud use for `llama3` on CPU does not exist for free, but this approach gives you a usable, no-cost deployment for experimentation.
