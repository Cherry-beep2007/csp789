# TripGenie — Deployment Guide

This repository contains **TripGenie**, an AI-Assisted Mood-Based Tourism & Heritage Trip Planning Streamlit Web Application.

---

## 1. Local Run (Windows / Mac / Linux)

### Option A: Using `run_app.bat` (Windows)
Double-click `run_app.bat` in the project folder.

### Option B: Terminal / Command Prompt
```bash
pip install -r requirements.txt
streamlit run a.py
```
Access the application at `http://localhost:8501`.

---

## 2. Deploy Free on Streamlit Community Cloud (Recommended)

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and click **New App**.
4. Select your repository, branch (`main`), and set **Main file path** to `a.py`.
5. Click **Deploy!** Your app will be live with a shareable URL.

---

## 3. Deploy on Render.com (Free Cloud Hosting)

1. Create a free account on [Render.com](https://render.com/).
2. Create a **New Web Service** connected to your GitHub repository.
3. Set the environment to **Python 3**.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `streamlit run a.py --server.port=$PORT --server.address=0.0.0.0`
6. Click **Create Web Service**.

---

## 4. Deploy on Hugging Face Spaces

1. Create a Space on [Hugging Face Spaces](https://huggingface.co/spaces).
2. Select **Streamlit** as the SDK.
3. Upload/push all files from this directory.
4. Hugging Face will automatically build and host the app.

---

## 5. Deploy with Docker

```bash
docker build -t tripgenie-app .
docker run -p 8501:8501 tripgenie-app
```
Then visit `http://localhost:8501`.
