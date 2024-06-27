from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import portrait, landscape, A4

import time


def split_pdf(input_file, offset: int = 0, landscape_mode: bool = False):
    # time.sleep(3)
    # raise ValueError
    input1 = PdfReader(input_file)
    output = PdfWriter()

    print(len(input1.pages), "pages")
    org_page = input1.pages[0]
    # Get original page dimensions
    original_width = float(org_page.mediabox.width)
    original_height = float(org_page.mediabox.height)

    # Define the height of the new pages (portrait orientation)
    a4_width, a4_height = portrait(A4)
    if landscape_mode:
        a4_width, a4_height = a4_height, a4_width

    new_page_height = original_width * (a4_height / a4_width)

    print(original_width, new_page_height)

    i = 0

    while True:
        i += 1
        print("Processing page", i)
        page = org_page

        page.cropbox.upper_left = (0, original_height - (i - 1) * new_page_height - offset)
        page.cropbox.lower_right = (original_width, original_height - i * new_page_height - offset)

        output.add_page(page)

        if original_height < i * new_page_height:
            break

    return output
