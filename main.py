from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, StreamingResponse
import requests

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Meta Agent V1</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background: #0f172a; color: #f8fafc; }
            .container { max-width: 600px; margin: auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            h1 { color: #38bdf8; text-align: center; }
            input, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: none; box-sizing: border-box; }
            input { background: #334155; color: white; }
            button { background: #0ea5e9; color: white; font-weight: bold; cursor: pointer; }
            button:hover { background: #0284c7; }
            .result { margin-top: 20px; text-align: center; }
            img { max-width: 100%; border-radius: 8px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AGENT ACTIF</h1>
            <input type="text" id="prompt" placeholder="Entrez un prompt pour generer une image...">
            <button onclick="generateImage()">Generer l'image</button>
            <div class="result" id="result"></div>
        </div>
        <script>
            async function generateImage() {
                const prompt = document.getElementById('prompt').value;
                const resDiv = document.getElementById('result');
                if (!prompt) return;
                resDiv.innerHTML = "Generation en cours...";
                const response = await fetch(`/api/generate?prompt=${encodeURIComponent(prompt)}`);
                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    resDiv.innerHTML = `<img src="${url}" alt="Genere">`;
                } else {
                    resDiv.innerHTML = "Erreur lors de la generation.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/generate")
def generate_image(prompt: str):
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    resp = requests.get(url)
    return Response(content=resp.content, media_type="image/jpeg")

@app.get("/api/download")
def download_video(url: str):
    resp = requests.get(url, stream=True)
    return StreamingResponse(resp.raw, media_type="video/mp4")
