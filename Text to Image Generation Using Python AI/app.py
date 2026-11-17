import os
import uuid
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

model_path = os.path.join(BASE_DIR, "realisticVisionV60B1_v51HyperVAE.safetensors")
device = "cuda" if torch.cuda.is_available() else "cpu"

def dummy_checker(images, **kwargs):
    return images, [False] * len(images)

print(f"Loading Realistic Vision model on {device}...")
pipe = StableDiffusionPipeline.from_single_file(
    model_path,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None
).to(device)
pipe.safety_checker = dummy_checker
if hasattr(pipe, "enable_attention_slicing"):
    pipe.enable_attention_slicing()
if hasattr(pipe, "enable_vae_slicing"):
    pipe.enable_vae_slicing()
elif hasattr(pipe.vae, "enable_slicing"):
    pipe.vae.enable_slicing()
print("Txt2Img Pipeline loaded successfully!")

img2img_pipe = None
pipe_lock = threading.Lock()

def get_img2img_pipe():
    global img2img_pipe
    if img2img_pipe is None:
        print("Initializing Img2Img pipeline (sharing components)...")
        img2img_pipe = StableDiffusionImg2ImgPipeline(
            vae=pipe.vae,
            text_encoder=pipe.text_encoder,
            tokenizer=pipe.tokenizer,
            unet=pipe.unet,
            scheduler=pipe.scheduler,
            safety_checker=dummy_checker,
            feature_extractor=pipe.feature_extractor
        )
    return img2img_pipe

def get_gallery_images():
    if not os.path.exists(OUTPUT_DIR):
        return []
    files = [f for f in os.listdir(OUTPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
    return files

@app.route("/")
def index():
    gallery = get_gallery_images()
    return render_template("index.html", device=device.upper(), gallery=gallery)

@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt", "").strip()
    negative_prompt = request.form.get("negative_prompt", "").strip()
    steps = int(request.form.get("steps", 20))
    guidance = float(request.form.get("guidance", 7.5))
    strength = float(request.form.get("strength", 0.75))
    base_image_file = request.files.get("base_image")

    if not prompt:
        return jsonify({"success": False, "error": "Prompt cannot be empty"}), 400

    filename = f"{uuid.uuid4().hex}.png"
    save_path = os.path.join(OUTPUT_DIR, filename)

    try:
        with pipe_lock:
            if base_image_file and base_image_file.filename:
                # Image-to-Image
                upload_filename = f"upload_{uuid.uuid4().hex}_{base_image_file.filename}"
                upload_path = os.path.join(UPLOAD_DIR, upload_filename)
                base_image_file.save(upload_path)

                init_image = Image.open(upload_path).convert("RGB").resize((512, 512))
                i2i = get_img2img_pipe()
                result = i2i(
                    prompt=prompt,
                    negative_prompt=negative_prompt if negative_prompt else None,
                    image=init_image,
                    strength=strength,
                    num_inference_steps=steps,
                    guidance_scale=guidance
                ).images[0]
            else:
                # Text-to-Image
                result = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt if negative_prompt else None,
                    height=512,
                    width=512,
                    num_inference_steps=steps,
                    guidance_scale=guidance
                ).images[0]

            result.save(save_path)

        return jsonify({
            "success": True,
            "filename": filename,
            "image_url": f"/output/{filename}"
        })

    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask Web UI on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=False)
