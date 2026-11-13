import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt

from .formatting import (
    configure_header,
    set_style_font,
)


def create_apa_template(template_path):
    """Create a Pandoc reference DOCX with APA-oriented styles."""
    template_path = Path(template_path).resolve()
    template_path.parent.mkdir(parents=True, exist_ok=True)

    with template_path.open("wb") as template_file:
        subprocess.run(
            ["pandoc", "--print-default-data-file=reference.docx"],
            stdout=template_file,
            check=True,
        )

    # Set the main Word styles and page margins.
    doc = Document(template_path)

    # Page layout.
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

        configure_header(section)

    # General paragraph and list styles.
    general_styles = (
        "Normal",
        "Body Text",
        "First Paragraph",
        "Compact",
        "List Paragraph",
        "List Bullet",
        "List Number",
        "Caption",
        "Bibliography",
    )

    for style_name in general_styles:
        try:
            style = doc.styles[style_name]
        except KeyError:
            continue

        set_style_font(style)
        style.paragraph_format.line_spacing = 2
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(0)

    # Ordinary body paragraphs use a half-inch first-line indent.
    doc.styles["Normal"].paragraph_format.first_line_indent = Inches(0.5)

    # Heading styles.
    heading_settings = {
        1: (True, False, WD_ALIGN_PARAGRAPH.CENTER),
        2: (True, False, WD_ALIGN_PARAGRAPH.LEFT),
        3: (True, True, WD_ALIGN_PARAGRAPH.LEFT),
        4: (True, False, WD_ALIGN_PARAGRAPH.LEFT),
        5: (True, True, WD_ALIGN_PARAGRAPH.LEFT),
    }

    for level, (bold, italic, alignment) in heading_settings.items():
        style = doc.styles[f"Heading {level}"]

        set_style_font(style)
        style.font.bold = bold
        style.font.italic = italic

        fmt = style.paragraph_format
        fmt.alignment = alignment
        fmt.line_spacing = 2
        fmt.space_before = Pt(0)
        fmt.space_after = Pt(0)
        fmt.keep_with_next = True

    # Block quotation style.
    for style_name in ("Block Text", "Block Quote"):
        try:
            style = doc.styles[style_name]
        except KeyError:
            continue

        set_style_font(style)
        style.paragraph_format.left_indent = Inches(0.5)
        style.paragraph_format.first_line_indent = Inches(0)
        style.paragraph_format.line_spacing = 2
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(0)

    doc.save(template_path)
    return template_path
