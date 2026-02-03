#!/bin/bash
# Hugging Face Spaces Deployment Script

echo "🚀 Hugging Face Spaces Deployment Helper"
echo "=========================================="
echo ""

# Check if HF CLI is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "📦 Installing Hugging Face CLI..."
    pip install -q huggingface_hub[cli]
fi

echo "Please provide your Hugging Face details:"
echo ""

# Get username
read -p "Hugging Face Username: " HF_USERNAME
read -p "Space Name (default: yt-web-summarizer): " SPACE_NAME
SPACE_NAME=${SPACE_NAME:-yt-web-summarizer}

echo ""
echo "🔐 Login to Hugging Face (you'll need your access token)"
echo "Get your token from: https://huggingface.co/settings/tokens"
echo ""

huggingface-cli login

echo ""
echo "📁 Creating Space repository..."

# Create the space
huggingface-cli repo create --type=space --space_sdk=streamlit "$SPACE_NAME" || echo "Space already exists, continuing..."

# Clone the space
SPACE_REPO="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
TEMP_DIR="/tmp/hf-space-$SPACE_NAME"

if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

git clone "$SPACE_REPO" "$TEMP_DIR"
cd "$TEMP_DIR"

echo ""
echo "📋 Copying project files..."

# Copy files
cp /workspaces/yt-web-summarizer/app.py .
cp /workspaces/yt-web-summarizer/config.py .
cp /workspaces/yt-web-summarizer/services.py .
cp /workspaces/yt-web-summarizer/utils.py .
cp /workspaces/yt-web-summarizer/logger.py .
cp /workspaces/yt-web-summarizer/exceptions.py .
cp /workspaces/yt-web-summarizer/requirements.txt .
cp /workspaces/yt-web-summarizer/packages.txt .
cp /workspaces/yt-web-summarizer/HF_README.md ./README.md

# Create .streamlit directory if needed
mkdir -p .streamlit
if [ -f /workspaces/yt-web-summarizer/.streamlit/config.toml ]; then
    cp /workspaces/yt-web-summarizer/.streamlit/config.toml .streamlit/
fi

echo ""
echo "✅ Files copied successfully!"
echo ""
echo "📤 Pushing to Hugging Face..."

# Git operations
git add .
git commit -m "Deploy YT Web Summarizer to Hugging Face Spaces"
git push

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "Your app will be available at:"
echo "https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "⏳ Build time: 2-5 minutes"
echo "📊 Monitor build: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME/logs"
echo ""
echo "🌟 Don't forget to:"
echo "  1. Star the space if you like it!"
echo "  2. Share with others"
echo "  3. Add relevant tags in settings"
echo ""
