from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, StreamingResponse
import requests
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Meta Agent V1</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); width: 400px; text-align: center; }
            input, button { width: 100%; padding: 0.75rem; margin-top: 1rem; border-radius: 6px; border: none; font-size: 1rem; }
            input { background: #334155; color: white; }
            button { background: #3b82f6; color: white; cursor: pointer; font-weight: bold; }
            button:hover { background: #2563eb; }
            img { margin-top: 1rem; max-width: 100%; border-radius: 6px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>AGENT ACTIF</h1>
            <p>Générez une image via l'API Pollinations</p>
            <input type="text" id="prompt" placeholder="Entrez votre prompt ici...">
            <button onclick="generateImage()">Générer l'image</button>
            <div id="result"></div>
        </div>
        <script>
            async function generateImage() {
                const prompt = document.getElementById('prompt').value;
                if (!prompt) return;
                const resDiv = document.getElementById('result');
                resDiv.innerHTML = "Génération en cours...";
                const response = await fetch(`/api/generate?prompt=${encodeURIComponent(prompt)}`);
                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    resDiv.innerHTML = `<img src="${url}" alt="Generated Image">`;
                } else {
                    resDiv.innerHTML = "Erreur lors de la génération.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/generate")
def generate_image(prompt: str):
    pollinations_url = f"https://image.pollinations.ai/prompt/{prompt}"
    resp = requests.get(pollinations_url, stream=True)
    return StreamingResponse(resp.raw, media_type="image/jpeg")

@app.get("/api/download")
def download_video(url: str):
    resp = requests.get(url, stream=True)
    return StreamingResponse(resp.raw, media_type="video/mp4", headers={"Content-Disposition": "attachment; filename=downloaded_video.mp4"})
