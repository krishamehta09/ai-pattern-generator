# AI Pattern Generator 🎨

This is a **FastAPI + Stable Diffusion** powered AI Pattern Generator.  
It uses Hugging Face `diffusers` to generate unique patterns and serves them via a web UI.

---

## 🚀 Running Locally

To run this app locally:

```bash
git clone https://github.com/krishamehta09/ai-pattern-generator.git
cd ai-pattern-generator

# Build the Docker image
docker build -t ai-pattern-generator .

# Run the container
docker run -p 7860:7860 ai-pattern-generator

🌐 Deployment (Hugging Face Spaces)

This app is designed to be deployed on Hugging Face Spaces using Docker.

Base image: python:3.10-slim

Framework: FastAPI

Entry point: server.py

Exposed port: 7860 (Spaces default)

📦 Requirements

The app installs the following main dependencies:

fastapi==0.103.0

uvicorn==0.22.0

diffusers==0.16.1

transformers==4.30.2

torch==2.0.1+cpu

huggingface_hub==0.25.2

numpy<2

Full list is in requirements.txt.

⚙️ Configuration

The app will launch with:

uvicorn server:app --host 0.0.0.0 --port 7860


This is required for Hugging Face Spaces Docker deployments.
📜 License

MIT License