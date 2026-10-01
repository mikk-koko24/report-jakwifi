from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO
import os


def create_pdf_report(
    original_pdf,
    chart_image,
    output_pdf,
    data=None
):

    temp_page = "temp_chart_page.pdf"
    temp_result = "temp_result.pdf"

    reader = PdfReader(original_pdf)

    first_page = reader.pages[0]

    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)

    c = canvas.Canvas(
        temp_page,
        pagesize=(
            page_width,
            page_height
        )
    )

    img = Image.open(chart_image)

    img_width, img_height = img.size

    margin = 40

    ratio = min(
        (page_width - margin * 2) / img_width,
        (page_height - margin * 2) / img_height
    )

    new_width = img_width * ratio
    new_height = img_height * ratio

    x = (page_width - new_width) / 2
    y = (page_height - new_height) / 2

    y = y + 100

    c.drawImage(
        chart_image,
        x,
        y,
        width=new_width,
        height=new_height
    )

    c.save()

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    chart_reader = PdfReader(temp_page)

    writer.add_page(
        chart_reader.pages[0]
    )

    with open(
        temp_result,
        "wb"
    ) as f:
        writer.write(f)

    add_page_number(
        temp_result,
        output_pdf
    )

    os.remove(temp_page)
    os.remove(temp_result)


def add_page_number(
    input_pdf,
    output_pdf
):

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    for index, page in enumerate(reader.pages):

        packet = BytesIO()

        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        c = canvas.Canvas(
            packet,
            pagesize=(
                width,
                height
            )
        )

        # =========================
        # FOOTER HITAM FULL LEBAR
        # =========================

        c.setFillColorRGB(
            0.02,
            0.08,
            0.18
        )

        c.rect(
            0,
            0,
            width,
            25,
            fill=1,
            stroke=0
        )

        # =========================
        # NOMOR HALAMAN PUTIH
        # =========================

        c.setFillColorRGB(
            1,
            1,
            1
        )

        c.setFont(
            "Helvetica",
            12
        )

        c.drawCentredString(
            width / 2,
            12,
            f"{index + 1}/{total_pages}"
        )

        c.save()

        packet.seek(0)

        overlay = PdfReader(packet).pages[0]

        page.merge_page(
            overlay
        )

        writer.add_page(
            page
        )

    with open(
        output_pdf,
        "wb"
    ) as f:
        writer.write(f)
