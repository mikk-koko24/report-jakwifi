from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse

import shutil
import os
import re

from analyzer import analyze_pdf
from chart_generator import create_chart
from pdf_generator import create_pdf_report


app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


STYLE = (
    "<style>"
    "* { margin:0; padding:0; box-sizing:border-box; }"
    "body {"
    "font-family:'Segoe UI', Arial, sans-serif;"
    "min-height:100vh;"
    "background:linear-gradient(135deg, #1e3c72, #2a5298);"
    "display:flex;"
    "align-items:center;"
    "justify-content:center;"
    "padding:20px;"
    "}"
    ".card {"
    "background:#ffffff;"
    "padding:50px 40px;"
    "border-radius:24px;"
    "box-shadow:0 20px 60px rgba(0,0,0,0.3);"
    "text-align:center;"
    "max-width:600px;"
    "width:100%;"
    "}"
    ".logo { font-size:42px; margin-bottom:10px; }"
    "h1 { color:#2C3E50; font-size:28px; letter-spacing:1px; }"
    ".accent {"
    "width:60px; height:4px;"
    "background:linear-gradient(90deg, #E74C3C, #E67E22);"
    "border-radius:2px;"
    "margin:15px auto 20px auto;"
    "}"
    ".subtitle { color:#7F8C8D; font-size:15px; margin-bottom:30px; }"
    "input[type=file] {"
    "width:100%;"
    "padding:14px;"
    "border:2px dashed #cbd5e1;"
    "border-radius:12px;"
    "background:#f8fafc;"
    "cursor:pointer;"
    "margin-bottom:25px;"
    "}"
    ".btn {"
    "background:linear-gradient(135deg, #E74C3C, #E67E22);"
    "color:white;"
    "border:none;"
    "padding:16px 70px;"
    "font-size:16px;"
    "font-weight:bold;"
    "border-radius:50px;"
    "cursor:pointer;"
    "letter-spacing:1px;"
    "transition:all .3s;"
    "box-shadow:0 8px 20px rgba(231,76,60,0.35);"
    "}"
    ".btn:hover {"
    "transform:translateY(-2px);"
    "box-shadow:0 12px 28px rgba(231,76,60,0.5);"
    "}"
    ".check {"
    "width:70px; height:70px;"
    "background:linear-gradient(135deg, #2ECC71, #27AE60);"
    "color:white;"
    "border-radius:50%;"
    "font-size:36px;"
    "line-height:70px;"
    "margin:0 auto 20px auto;"
    "}"
    ".site-name {"
    "color:#E74C3C;"
    "font-size:18px;"
    "font-weight:bold;"
    "margin-bottom:25px;"
    "}"
    ".btn-download {"
    "display:inline-block;"
    "text-decoration:none;"
    "color:white;"
    "padding:16px 36px;"
    "border-radius:14px;"
    "font-weight:bold;"
    "font-size:15px;"
    "margin:8px 4px;"
    "transition:all .3s;"
    "}"
    ".btn-png { background:linear-gradient(135deg, #3498DB, #2ECC71); }"
    ".btn-pdf { background:linear-gradient(135deg, #E74C3C, #E67E22); }"
    ".btn-download:hover {"
    "transform:translateY(-2px);"
    "box-shadow:0 10px 22px rgba(0,0,0,0.25);"
    "}"
    ".back {"
    "display:inline-block;"
    "margin-top:25px;"
    "color:#3498DB;"
    "text-decoration:none;"
    "font-weight:bold;"
    "}"
    ".back:hover { text-decoration:underline; }"
    "</style>"
)


@app.get("/", response_class=HTMLResponse)
def home():

    html = (
        "<html>"
        "<head>"
        "<title>Network Report Analyzer</title>"
        + STYLE +
        "</head>"
        "<body>"
        "<div class='card'>"
        "<div class='logo'>📊</div>"
        "<h1>NETWORK REPORT ANALYZER</h1>"
        "<div class='accent'></div>"
        "<p class='subtitle'>Upload PDF untuk membuat laporan TOP 10 Aplikasi</p>"
        "<form action='/analyze' method='post' enctype='multipart/form-data'>"
        "<input type='file' name='file' accept='.pdf' required>"
        "<br>"
        "<button class='btn' type='submit'>ANALYZE</button>"
        "</form>"
        "</div>"
        "</body>"
        "</html>"
    )

    return html


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    original_name = os.path.splitext(
        os.path.basename(file.filename)
    )[0]

    site = original_name.replace("_", " ")

    site = re.sub(
        r"\b\d{8}\b",
        "",
        site
    )

    site = " ".join(site.split())

    data = analyze_pdf(pdf_path)

    image_output = os.path.join(
        OUTPUT_FOLDER,
        original_name + ".png"
    )

    create_chart(
        site,
        data,
        image_output
    )

    pdf_output = os.path.join(
        OUTPUT_FOLDER,
        original_name + ".pdf"
    )

    create_pdf_report(
        pdf_path,
        image_output,
        pdf_output
    )

    html = (
        "<html>"
        "<head>"
        "<title>Hasil Analisis</title>"
        + STYLE +
        "</head>"
        "<body>"
        "<div class='card'>"
        "<div class='check'>✓</div>"
        "<h1>HASIL ANALISIS</h1>"
        "<p class='site-name'>" + site + "</p>"
        "<a class='btn-download btn-png' href='/download/png/"
        + original_name
        + "'>DOWNLOAD PNG TOP 10</a>"
        "<br>"
        "<a class='btn-download btn-pdf' href='/download/pdf/"
        + original_name
        + "'>DOWNLOAD PDF LENGKAP</a>"
        "<br>"
        "<a class='back' href='/'>← Analisis PDF lain</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return html


@app.get("/download/png/{filename}")
def download_png(filename: str):

    image_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".png"
    )

    return FileResponse(
        image_path,
        media_type="image/png",
        filename=filename + ".png"
    )


@app.get("/download/pdf/{filename}")
def download_pdf(filename: str):

    pdf_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".pdf"
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=filename + ".pdf"
    )
