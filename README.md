# 🎨 AI Image Studio - Free Open-Source Text-to-Image Generation

[![Live Demo](https://img.shields.io/badge/Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://karaan-singh.github.io/Image-generation-for-free-model/)
[![Model](https://img.shields.io/badge/Model-Realistic%20Vision%20v6.0-purple?style=for-the-badge)](https://civitai.com/models/4201/realistic-vision-v60)
[![License](https://img.shields.io/badge/License-OpenRAIL--M-green?style=for-the-badge)](https://huggingface.co/spaces/CompVis/stable-diffusion-license)

**👉 [Try the Live Web App on GitHub Pages](https://karaan-singh.github.io/Image-generation-for-free-model/)**

A 100% free, private, and offline-capable AI Image Generation Web Application powered by **Python**, **Flask**, **PyTorch**, and Hugging Face **Diffusers**, running the state-of-the-art open-source **Realistic Vision v6.0 (HyperVAE)** model.

Generate high-detail photorealistic images from text prompts or transform existing photos with Image-to-Image guidance directly in your web browser — completely free with **no API keys, no subscriptions, and zero rate limits**.

---

## 🧠 About the Open-Source Model: Realistic Vision v6.0 (HyperVAE)

This project runs **Realistic Vision v6.0 B1 (HyperVAE)**, one of the most acclaimed open-source photorealistic checkpoint models in the generative AI community.

### 🔬 Architecture & Technology
- **Base Architecture**: Latent Diffusion Model (LDM) built upon **Stable Diffusion 1.5** (by RunwayML, CompVis, and Stability AI).
- **HyperVAE Technology**: Integrated fine-tuned Variational Autoencoder (VAE) engineered specifically to eliminate color banding, boost dynamic range, sharpen micro-textures (skin pores, fabric weaves, hair strands), and deliver accurate human eyes and anatomy.
- **Weights Format**: Packed in `.safetensors` format (developed by Hugging Face). Unlike legacy `.ckpt` (pickle) files, `safetensors` files are **safe against arbitrary code execution**, zero-copy loadable, and load significantly faster into memory.
- **Inference Pipeline**: Managed via Hugging Face `diffusers` (`StableDiffusionPipeline` & `StableDiffusionImg2ImgPipeline`), supporting attention slicing and VAE slicing for low memory footprints.

### 🌟 Why Open-Source Self-Hosted?
| Feature | Proprietary APIs (Midjourney / DALL-E) | Realistic Vision (This Project) |
| :--- | :--- | :--- |
| **Cost** | \$10 – \$60+ / month subscriptions | **100% Free Forever** |
| **Privacy** | Your prompts & images stored on remote servers | **100% Local & Private** (Never leaves your PC) |
| **Offline Capability**| Requires internet connection at all times | **Runs Completely Offline** once downloaded |
| **Content Censorship**| Strict cloud censorship & false-positive filters | **Unfiltered Creative Freedom** (No artificial blocks) |
| **Rate Limits** | Fast hours / credits / queue limits | **Unlimited generations** |

### 📜 Model License
Realistic Vision is distributed under the **CreativeML OpenRAIL-M** license, which grants full freedom for personal, research, and creative use while prohibiting harmful or malicious applications.

---

## ✨ Features

- **Text-to-Image (`txt2img`)**: Turn natural language prompts into high-resolution 512×512 photorealistic images.
- **Image-to-Image (`img2img`)**: Upload a base photo to restyle, enhance, or transform it according to your text prompt with adjustable transformation strength.
- **Modern Responsive Web UI**: Glassmorphic dark-mode web interface with real-time generation feedback, spinners, and responsive layouts.
- **Fine-Grained Controls**:
  - **Prompt & Negative Prompt**: Explicitly define what to feature and what to avoid.
  - **Inference Steps Slider**: Dial between speed and maximum detail (10–50 steps).
  - **Guidance Scale (CFG)**: Control how strictly the AI adheres to your text prompt.
  - **Image Strength Slider**: Seamlessly tune the balance between original image and new prompt in img2img.
- **Built-in Gallery & Downloads**: Review previously generated images in the session gallery and download full-resolution PNGs instantly.
- **Dual Interface Modes**: Run either as a **Flask Web Studio** (`app.py`) or as a **Desktop GUI** (`gui.py`).

---

## 📁 Project Structure

```text
Image-generation-for-free-model/
├── app.py                                    # Flask web application server
├── gui.py                                    # Desktop Tkinter GUI alternative
├── requirements.txt                          # Python package dependencies
├── realisticVisionV60B1_v51HyperVAE.safetensors # Model weights file (~2.1 GB)
├── templates/
│   └── index.html                           # Modern Web Studio UI
├── output/                                  # Generated images
├── static/
│   ├── uploads/                             # Uploaded base images for img2img
│   └── frames/                              # UI assets
└── README.md                                # Documentation & guide
```

---

## ⚙️ System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Python 3.10 or newer (tested and verified on Python 3.14)
- **RAM**: Minimum 8 GB (16 GB recommended)
- **Hardware Acceleration**:
  - **CPU**: Works out of the box using multi-threaded PyTorch execution.
  - **NVIDIA GPU (CUDA)**: Automatically detected if available for lightning-fast generations (2–5 seconds).

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/karaan-singh/Image-generation-for-free-model.git
cd Image-generation-for-free-model
```

### 2. (Optional) Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

Core libraries:
- `torch` & `torchvision` (Deep learning computation)
- `diffusers` & `transformers` (Diffusion pipeline & CLIP tokenizer)
- `accelerate` & `safetensors` (Fast tensor memory mapping)
- `flask` & `pillow` (Web backend & image processing)
- `omegaconf` & `huggingface_hub` (Model loaders)

---

### 4. Download Model Weights (~2.1 GB)

Because GitHub limits individual files to 100 MB, the 2.1 GB `.safetensors` model file is not committed directly into git history.

Download the model weights directly with this 1-line command:
```bash
python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='void-404x/realisticVisionV60B1_v51HyperVAE.safetensors', filename='realisticVisionV60B1_v51HyperVAE.safetensors', local_dir='.')"
```

*Alternatively, manually download `realisticVisionV60B1_v51HyperVAE.safetensors` from [Civitai](https://civitai.com/models/4201/realistic-vision-v60) or [Hugging Face](https://huggingface.co/void-404x/realisticVisionV60B1_v51HyperVAE.safetensors) and place it in the same directory as `app.py`.*

---

## 🖥️ How to Run

### Method 1: Web Studio (Recommended)
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and go to:
   ```text
   http://127.0.0.1:5000
   ```
3. Type your prompt and click **Generate Image**!

---

### Method 2: Desktop GUI
If you want to use the native desktop window instead:
```bash
python gui.py
```

---

## 💡 Prompting Tips for Realistic Vision

For best photorealistic results with this model, structure your prompts as follows:

- **Style keywords**: `photorealistic`, `8k resolution`, `cinematic lighting`, `high detail`, `RAW photo`, `fujifilm`, `shallow depth of field`.
- **Subject description**: Be specific about facial expressions, clothing, background elements, and textures.
- **Recommended Negative Prompt**:
  ```text
  ugly, deformed, disfigured, poor details, bad anatomy, bad hands, extra limbs, blurry, cartoon, illustration, low quality
  ```

---

## ⏱️ Generation Speed Guide

| Device | Inference Steps | Average Time | Best For |
| :--- | :--- | :--- | :--- |
| **CPU** | 10 – 15 steps | ~25 – 45 sec | Quick composition & prompt tests |
| **CPU** | 20 steps *(Default)* | ~50 – 80 sec | Optimal balance of speed and realism |
| **CPU** | 30 – 50 steps | ~2 – 3 min | Ultra-fine rendering |
| **NVIDIA GPU (CUDA)** | 20 – 30 steps | ~2 – 5 sec | Real-time creation |

---

## 👤 Author & Links

- **Author**: [karaan-singh](https://github.com/karaan-singh)
- **Repository**: [Image-generation-for-free-model](https://github.com/karaan-singh/Image-generation-for-free-model)
- **Model Creator**: SG161222 (Realistic Vision v6.0)
