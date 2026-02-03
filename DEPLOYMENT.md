# 🚀 Deployment Guide

## Streamlit Cloud Deployment (Recommended)

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Production-ready release"
git push origin main
```

### Step 2: Create Streamlit Account
1. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign up with GitHub account
3. Authorize Streamlit

### Step 3: Deploy
1. Click "New app"
2. Select repository: `yt-web-summarizer`
3. Main file path: `app.py`
4. Click "Deploy"

### Step 4: Configure Secrets
1. Go to app settings (gear icon)
2. Click "Secrets"
3. Add Groq API key:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## Docker Deployment

### Option 1: Docker Hub

```bash
# Build image
docker build -t yourusername/yt-summarizer:latest .

# Login to Docker Hub
docker login

# Push image
docker push yourusername/yt-summarizer:latest

# Pull and run
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e ENVIRONMENT=production \
  yourusername/yt-summarizer:latest
```

### Option 2: Docker Compose

```bash
# Create .env file
cp .env.example .env
# Edit .env with your API key

# Run
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop
docker-compose down
```

## Server Deployment (VPS/Cloud VM)

### 1. SSH into Server
```bash
ssh user@your_server_ip
```

### 2. Install Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3-pip ffmpeg git curl

# Create directory
mkdir -p /opt/yt-summarizer
cd /opt/yt-summarizer
```

### 3. Clone Repository
```bash
git clone https://github.com/reethj-07/yt-web-summarizer.git .
```

### 4. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your API key
```

### 6. Create Systemd Service
```bash
sudo tee /etc/systemd/system/yt-summarizer.service > /dev/null <<EOF
[Unit]
Description=YT Web Summarizer
After=network.target

[Service]
Type=simple
User=nobody
WorkingDirectory=/opt/yt-summarizer
Environment="PATH=/opt/yt-summarizer/venv/bin"
ExecStart=/opt/yt-summarizer/venv/bin/streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --logger.level=info
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable yt-summarizer
sudo systemctl start yt-summarizer
```

### 7. Setup Nginx Reverse Proxy
```bash
sudo tee /etc/nginx/sites-available/yt-summarizer > /dev/null <<EOF
server {
    listen 80;
    server_name your_domain.com;

    client_max_body_size 100M;
    proxy_read_timeout 3600s;
    proxy_connect_timeout 75s;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/yt-summarizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Setup SSL (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

## Kubernetes Deployment

### 1. Create Docker Image
```bash
docker build -t yourusername/yt-summarizer:v1.0 .
docker push yourusername/yt-summarizer:v1.0
```

### 2. Create Deployment YAML
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yt-summarizer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: yt-summarizer
  template:
    metadata:
      labels:
        app: yt-summarizer
    spec:
      containers:
      - name: app
        image: yourusername/yt-summarizer:v1.0
        ports:
        - containerPort: 8501
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: yt-summarizer-secrets
              key: groq-api-key
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: yt-summarizer-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: yt-summarizer
```

### 3. Deploy to Kubernetes
```bash
# Create secret
kubectl create secret generic yt-summarizer-secrets \
  --from-literal=groq-api-key=your_key

# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl logs -f pod/yt-summarizer-xxxxx
```

## AWS Deployment (EC2 + ALB)

### 1. Launch EC2 Instance
- AMI: Ubuntu Server 22.04 LTS
- Instance type: t3.medium (or larger)
- Security group: Allow 80, 443, 22

### 2. Connect and Setup
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install -y python3.11 python3-pip ffmpeg git nginx

# Clone and setup (follow Server Deployment steps)
```

### 3. Create Application Load Balancer
- Create ALB in EC2 console
- Add listener on port 80
- Create target group pointing to EC2 instance:8501
- Add SSL certificate (ACM)

## Monitoring & Maintenance

### Health Checks
```bash
# Check service status
curl http://localhost:8501/_stcore/health

# Check logs
tail -f logs/app.log

# Monitor resources
docker stats  # For Docker
systemctl status yt-summarizer  # For Systemd
```

### Backup Strategy
```bash
# Backup configuration
tar -czf backups/config-$(date +%Y%m%d).tar.gz .env logs/

# Set up cron backup
0 2 * * * tar -czf /backups/yt-summarizer-$(date +\%Y\%m\%d).tar.gz /opt/yt-summarizer
```

### Update & Rollback
```bash
# Pull latest changes
git pull origin main

# Restart service
systemctl restart yt-summarizer

# Or with Docker
docker-compose down
docker-compose up -d
```

## Performance Tuning

### Streamlit Configuration
```bash
# Optimize Streamlit
streamlit run app.py \
  --client.showErrorDetails=false \
  --logger.level=warning \
  --client.toolbarMode=minimal
```

### Cache Configuration
```env
CACHE_TTL_SECONDS=3600  # 1 hour
MAX_CACHE_SIZE_MB=100   # Maximum cache size
ENABLE_CACHE=true
```

### Rate Limiting
```env
RATE_LIMIT_CALLS=10         # Requests
RATE_LIMIT_PERIOD_SECONDS=60  # Per period
```

## Security Hardening

### 1. Firewall Rules
```bash
# UFW
sudo ufw default deny incoming
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. API Key Management
- Use environment variables or secret managers
- Rotate keys regularly
- Never commit `.env` files
- Use IAM roles in cloud environments

### 3. HTTPS/SSL
- Always use HTTPS in production
- Use strong certificates (Let's Encrypt)
- Enable HSTS headers

### 4. Rate Limiting & DDoS Protection
- Enable Cloudflare DDoS protection
- Configure rate limits
- Use WAF rules

## Troubleshooting

### Service Won't Start
```bash
# Check logs
journalctl -u yt-summarizer -n 50

# Check Python environment
source venv/bin/activate
python -c "import streamlit; print(streamlit.__version__)"
```

### High Memory Usage
- Reduce `CACHE_TTL_SECONDS`
- Lower `MAX_CACHE_SIZE_MB`
- Disable unnecessary features

### Slow Performance
- Check network latency to Groq API
- Verify Whisper model size
- Monitor CPU/GPU usage

---

For more help, see [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
