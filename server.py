# server.py

import io
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler



# ─── Configuration ─────────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID = "stabilityai/stable-diffusion-2-base"

# When we call .from_pretrained, we’ll swap in a faster scheduler:
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=(torch.float16 if DEVICE.startswith("cuda") else torch.float32),
    safety_checker=None,
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_attention_slicing()
pipe = pipe.to(DEVICE)

# A small global blacklist: we never want these in any pattern
BASE_NEGATIVE = "faces, text, logo, background blur, photorealistic, watermark, signature"

# ─── FastAPI setup ─────────────────────────────────────────
app = FastAPI()
@app.get("/")
def root():
    return {"message": "App is live"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down in prod!
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str          # we’ll build it client-side from style/colors/elements
    width: int = 256     # default down-res for faster CPU inference
    height: int = 256
    steps: int = 20
    guidance_scale: float = 8.0
    seed: int | None = None

@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse("index.html", media_type="text/html")

@app.post("/generate")
async def generate(req: GenerateRequest):
    # build our final negative string
    neg = BASE_NEGATIVE

    # reproducible seed if provided
    gen = (
        torch.Generator(device=DEVICE).manual_seed(req.seed)
        if req.seed is not None
        else None
    )

    # now run the pipeline
    try:
        out = pipe(
            req.prompt,
            negative_prompt=neg,
            width=req.width,
            height=req.height,
            guidance_scale=req.guidance_scale,
            num_inference_steps=req.steps,
            generator=gen,
        )
        img = out.images[0]
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)
