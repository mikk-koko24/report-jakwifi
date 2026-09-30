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


@app.get("/", response_class=HTMLResponse)
def home():

    html = (
        "<html>"
        "<head><title>Network Report Analyzer</title></head>"
        "<body style='font-family:Arial;text-align:center;padding-top:100px;'>"

        "<h1>NETWORK REPORT ANALYZER</h1>"

        "<p>Upload PDF untuk membuat TOP 10 Aplikasi</p>"

        "<form action='/analyze' method='post' enctype='multipart/form-data'>"

        "<input type='file' name='file' accept='.pdf' required>"

        "<br><br>"

        "<button type='submit'>ANALYZE</button>"

        "</form>"

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
        "<head><title>Hasil Analisis</title></head>"
        "<body style='font-family:Arial;text-align:center;padding-top:100px;'>"

        "<h1>HASIL ANALISIS</h1>"

        "<br>"

        "<a href='/download/png/"
        + original_name
        + "'>"
        "<button style='padding:15px 30px;'>"
        "DOWNLOAD PNG TOP 10"
        "</button>"
        "</a>"

        "<br><br>"

        "<a href='/download/pdf/"
        + original_name
        + "'>"
        "<button style='padding:15px 30px;'>"
        "DOWNLOAD PDF LENGKAP"
        "</button>"
        "</a>"

        "<br><br>"

        "<a href='/'>Analisis PDF lain</a>"

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