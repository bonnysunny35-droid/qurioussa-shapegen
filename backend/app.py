import os
from pathlib import Path
from fastapi import FastAPI, Form, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from ai_svg import generate_svg_from_prompt
from svg_to_stl import svg_string_to_stl
from storage import local_output_dir, upload_s3_if_enabled

app = FastAPI(title="Qurioussa ShapeGen")

# Open CORS for MVP (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

OUTPUT_DIR = local_output_dir()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate_svg")
async def generate_svg(prompt: str = Form(...)):
    svg_text = generate_svg_from_prompt(prompt)
    return PlainTextResponse(svg_text, media_type="image/svg+xml")

@app.post("/svg_to_stl")
async def svg_to_stl(svg: UploadFile = File(...), height: float = Form(2.0)):
    svg_text = (await svg.read()).decode("utf-8", "ignore")
    out_path = OUTPUT_DIR / f"{Path(svg.filename).stem}_h{int(height*10)}.stl"
    path = svg_string_to_stl(svg_text, str(out_path), height=height)
    s3_url = upload_s3_if_enabled(path)
    return {"stl_url": s3_url} if s3_url else {"stl_path": path}

@app.post("/generate")  # prompt -> svg -> stl (one shot)
async def generate(prompt: str = Form(...), height: float = Form(2.0)):
    svg_text = generate_svg_from_prompt(prompt)
    safe = "".join(c for c in prompt[:24] if c.isalnum() or c in "-_").strip() or "shape"
    out_path = OUTPUT_DIR / f"{safe}.stl"
    path = svg_string_to_stl(svg_text, str(out_path), height=height)
    s3_url = upload_s3_if_enabled(path)
    return {"stl_url": s3_url} if s3_url else {"stl_path": path}

@app.get("/download")
def download(file: str = Query(...)):
    p = Path(file)
    if not p.exists() or p.suffix.lower() != ".stl":
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(str(p), media_type="model/stl", filename=p.name)
