# FrameForge AI

A Streamlit web app that forges a simple idea into a five-scene visual story — generating narrative text with Groq (Llama 3.3) and images with Stable Diffusion, then stitching them into a short video.

## Features

- Generates a 5-scene story narrative from a single prompt using **Groq (Llama 3.3 70B)**
- Creates one image per scene using **Stability AI (SDXL 1.0)**
- Compiles images into an MP4 video with **MoviePy**
- Per-run output saved under `data/runs/` so runs don't overwrite each other
- Download buttons for individual scene images

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/frameforge-ai.git
cd frameforge-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** MoviePy video export requires [FFmpeg](https://ffmpeg.org/download.html) to be installed and on your PATH. If it is missing, the app still works and skips video creation.

### 4. Configure API keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Where to get it |
|---|---|
| `GROQ_API_KEY` | [Groq Console](https://console.groq.com) |
| `STABILITY_API_KEY` | [Stability AI](https://platform.stability.ai/account/keys) |

### 5. Run the app

```bash
streamlit run app.py
```

## Project Structure

```
frameforge-ai/
├── app.py                        # Streamlit entry point
├── src/
│   ├── narrative_generator.py    # Gemini story generation
│   └── image_generator.py        # Stability AI image generation
├── requirements.txt
├── .env.example
├── .gitignore
└── data/                         # Generated images & videos (git-ignored)
```

## Tech Stack

- [Streamlit](https://streamlit.io/)
- [Groq API (Llama 3.3 70B)](https://console.groq.com)
- [Stability AI SDK](https://github.com/Stability-AI/stability-sdk)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Pillow](https://python-pillow.org/)
