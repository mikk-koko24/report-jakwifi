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
        output_pdf,
        data
    )

    os.remove(temp_page)
    os.remove(temp_result)


def add_page_number(
    input_pdf,
    output_pdf,
    data=None
):

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    # =========================
    # BIKIN DAFTAR DARI DATA ASLI
    # (bukan tulisan manual lagi)
    # =========================

    apps_list = []

    if data:

        total = sum(
            value for _, value in data
        )

        for i, (nama, nilai) in enumerate(data):

            if total > 0:
                persen = round(
                    (nilai / total) * 100,
                    1
                )
            else:
                persen = 0

            apps_list.append(
                (
                    str(i + 1),
                    nama,
                    f"{persen}%"
                )
            )

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
        # DAFTAR 5 KIRI 5 KANAN
        # HALAMAN TERAKHIR
        # =========================

        if index == total_pages - 1 and apps_list:

            c.setFillColorRGB(
                0,
                0,
                0
            )

            left_apps = apps_list[:5]
            right_apps = apps_list[5:]

            start_y = 210
            line_height = 28

            left_x = 70
            right_x = width / 2 + 40

            c.setFont(
                "Helvetica",
                13
            )

            for i, app in enumerate(left_apps):

                y = start_y - (i * line_height)

                c.drawString(
                    left_x,
                    y,
                    f"{app[0]}. {app[1]}"
                )

                c.drawRightString(
                    width / 2 - 20,
                    y,
                    app[2]
                )

            for i, app in enumerate(right_apps):

                y = start_y - (i * line_height)

                c.drawString(
                    right_x,
                    y,
                    f"{app[0]}. {app[1]}"
                )

                c.drawRightString(
                    width - 55,
                    y,
                    app[2]
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
