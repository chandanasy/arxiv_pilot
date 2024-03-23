from typing import List
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
import base64
from PIL import Image


def get_pdf_data(pdfDocs):
    text = ""
    images = []
    for pdf in pdfDocs:
        pdfReader = PdfReader(pdf)
        for page in pdfReader.pages:
            text += page.extract_text()
            images.extend(page.images)
    return text, images


def get_pdf_images(pdfDocs):
    images = set()
    output_dir = "./images"
    for i, pdf in enumerate(pdfDocs):
        pdfReader = PdfReader(pdf)
        for j, page in enumerate(pdfReader.pages):
            for image_obj in page.images:
                # image_name = f"image_{i+1}_{j+1}.jpg"
                image_path = f"{output_dir}/{i}_{image_obj.name}"
                images.add(image_path)
                with open(image_path, "wb") as fp:
                    fp.write(image_obj.data)
    return list(images)


def get_pdf_pages(filePaths: List[str]):
    pdf_pages = []
    for pdf in filePaths:
        loader = PyPDFLoader(pdf)
        pdf_pages.extend(loader.load_and_split())
    return pdf_pages


def make_claude_messages(pdfDocs):
    message_content = []
    countimgs = 0
    for pdf in pdfDocs:
        pdfReader = PdfReader(pdf)
        for page in pdfReader.pages:
            text_content = [{"type": "text", "text": page.extract_text()}]
            image_content = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64.b64encode(img.data).decode("utf-8"),
                    },
                }
                for img in page.images
            ]
            message_content.extend(text_content)
            if countimgs + len(image_content) <= 20:
                message_content.extend(image_content)
                countimgs += len(image_content)

    return message_content
