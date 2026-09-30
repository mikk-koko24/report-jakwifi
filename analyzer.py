import fitz
import re

from filters import detect_application



def extract_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text("text")

    doc.close()

    return text



def analyze_pdf(pdf_path):

    text = extract_pdf_text(pdf_path)

    lines = [
        x.strip()
        for x in text.split("\n")
        if x.strip()
    ]


    results = {}


    for i, line in enumerate(lines):

        if "." in line and not line.isdigit():

            domain = line.lower()


            for next_line in lines[i+1:i+5]:

                if next_line.isdigit():

                    visit = int(next_line)

                    app = detect_application(domain)


                    if app:

                        results[app] = (
                            results.get(app, 0)
                            + visit
                        )

                    break



    ranking = sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )


    return ranking[:10]