#!/usr/bin/env python3
"""Extract text and images from a PDF file for Marp PPT generation."""

import sys
import os
import json
import fitz  # PyMuPDF


def extract_pdf(pdf_path, output_dir="output"):
    """Extract text (with structure) and images from PDF.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images

    Returns:
        dict with 'pages' (list of page text) and 'images' (list of image paths)
    """
    doc = fitz.open(pdf_path)

    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    result = {"pages": [], "images": [], "metadata": {}}
    result["metadata"]["page_count"] = len(doc)
    result["metadata"]["title"] = doc.metadata.get("title", "")

    for page_num, page in enumerate(doc):
        # Extract text with structure
        text = page.get_text("text")
        result["pages"].append({
            "page": page_num + 1,
            "text": text.strip()
        })

        # Extract images
        for img_idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            if base_image:
                img_ext = base_image["ext"]
                img_bytes = base_image["image"]
                img_filename = f"page{page_num+1}_img{img_idx+1}.{img_ext}"
                img_path = os.path.join(output_dir, "images", img_filename)

                with open(img_path, "wb") as f:
                    f.write(img_bytes)

                result["images"].append({
                    "page": page_num + 1,
                    "path": img_path,
                    "filename": img_filename,
                    "width": base_image.get("width", 0),
                    "height": base_image.get("height", 0)
                })

    # Save structured text to JSON
    json_path = os.path.join(output_dir, "extracted.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(doc)} pages, {len(result['images'])} images")
    print(f"Text saved to: {json_path}")
    print(f"Images saved to: {os.path.join(output_dir, 'images')}/")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    extract_pdf(pdf_path, output_dir)
