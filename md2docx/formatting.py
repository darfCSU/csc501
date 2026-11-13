import copy

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


def set_run_font(run):
    """Apply Times New Roman 12 pt without changing bold or italic."""
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.rFonts

    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)

    for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{attribute}"), "Times New Roman")


def set_style_font(style):
    """Set a style's font, including its Word font declarations."""
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    rpr = style._element.get_or_add_rPr()
    rfonts = rpr.rFonts

    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)

    for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{attribute}"), "Times New Roman")


def set_paragraph_spacing(paragraph):
    """Apply APA double spacing with no additional paragraph spacing."""
    fmt = paragraph.paragraph_format
    fmt.line_spacing = 2
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(0)


def insert_page_number(paragraph):
    """Insert a Word PAGE field in the header."""
    paragraph.clear()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    paragraph.paragraph_format.first_line_indent = Inches(0)

    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    field.set(qn("w:dirty"), "true")

    run_element = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")

    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "Times New Roman")
    fonts.set(qn("w:hAnsi"), "Times New Roman")
    rpr.append(fonts)

    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "24")
    rpr.append(size)

    run_element.append(rpr)

    text_element = OxmlElement("w:t")
    text_element.text = "1"
    run_element.append(text_element)

    field.append(run_element)
    paragraph._p.append(field)


def configure_header(section):
    """Configure the APA page-number header."""
    section.header_distance = Inches(0.5)
    section.header.is_linked_to_previous = False

    paragraph = section.header.paragraphs[0]
    insert_page_number(paragraph)


def add_title_page(
    doc,
    title,
    student,
    institution,
    course,
    instructor,
    due_date,
):
    """Insert an APA 7 student title page before the paper body."""

    # No title page is generated unless a title is supplied.
    if not title:
        if any((student, course, instructor, due_date)):
            raise ValueError(
                "A paper title is required when title-page information "
                "is supplied."
            )
        return

    # Remove an identical opening Markdown title, if present.
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            if paragraph.text.strip() == str(title).strip():
                paragraph._element.getparent().remove(paragraph._element)
            break

    # Locate the first document body element.
    body = doc.element.body
    anchor = next(
        (
            element
            for element in body
            if element.tag != qn("w:sectPr")
        ),
        None,
    )

    if anchor is None:
        anchor = doc.add_paragraph()._p

    fields = [
        student,
        institution,
        course,
        instructor,
        due_date,
    ]

    # Build the title-page paragraphs.
    new_paragraphs = []

    # APA title placement: three double-spaced lines below the top margin.
    for _ in range(3):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        set_paragraph_spacing(p)
        new_paragraphs.append(p)

    # Title.
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Inches(0)
    set_paragraph_spacing(p)

    run = p.add_run(str(title))
    run.bold = True
    set_run_font(run)
    new_paragraphs.append(p)

    # APA requires one blank double-spaced line after the title.
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(0)
    set_paragraph_spacing(p)
    new_paragraphs.append(p)

    # Author, affiliation, course, instructor, and due date.
    for value in fields:
        if not value:
            continue

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0)
        p.paragraph_format.right_indent = Inches(0)
        set_paragraph_spacing(p)

        run = p.add_run(str(value))
        set_run_font(run)
        new_paragraphs.append(p)

    # Repeat the paper title at the top of page two.
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.page_break_before = True
    set_paragraph_spacing(p)

    run = p.add_run(str(title))
    run.bold = True
    set_run_font(run)
    new_paragraphs.append(p)

    # Move the new paragraphs before the existing document content.
    for paragraph in new_paragraphs:
        anchor.addprevious(paragraph._p)


def is_list_item(paragraph):
    """Identify numbered or bulleted paragraphs without altering them."""
    p_pr = paragraph._p.pPr

    if p_pr is not None and p_pr.find(qn("w:numPr")) is not None:
        return True

    style = paragraph.style

    while style is not None:
        style_p_pr = style.element.pPr

        if (
            style_p_pr is not None
            and style_p_pr.find(qn("w:numPr")) is not None
        ):
            return True

        style_name = style.name.casefold()

        if "list" in style_name or "bullet" in style_name:
            return True

        style = style.base_style

    return False


def is_block_quote(paragraph):
    """Identify block quotation paragraphs."""
    style_name = paragraph.style.name.casefold()

    return (
        "block text" in style_name
        or "block quote" in style_name
        or "blockquote" in style_name
    )


def format_body(doc):
    """Format body paragraphs while preserving list indentation."""
    abstract = False

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        style_name = paragraph.style.name

        # Apply font to all runs without removing bold or italic.
        for run in paragraph.runs:
            set_run_font(run)

        if not text:
            continue

        set_paragraph_spacing(paragraph)

        if style_name.startswith("Heading"):
            paragraph.paragraph_format.first_line_indent = Inches(0)
            paragraph.paragraph_format.keep_with_next = True
            abstract = text.casefold() == "abstract"
            continue

        if abstract:
            paragraph.paragraph_format.first_line_indent = Inches(0)
            paragraph.paragraph_format.left_indent = Inches(0)
            continue

        if style_name == "Caption":
            paragraph.paragraph_format.first_line_indent = Inches(0)
            continue

        if is_list_item(paragraph):
            # Preserve Word/Pandoc bullet and numbering indents.
            # Only spacing and font are standardized.
            continue

        if is_block_quote(paragraph):
            paragraph.paragraph_format.left_indent = Inches(0.5)
            paragraph.paragraph_format.first_line_indent = Inches(0)
            continue

        if style_name == "Title":
            paragraph.paragraph_format.first_line_indent = Inches(0)
            continue

        paragraph.paragraph_format.left_indent = Inches(0)
        paragraph.paragraph_format.first_line_indent = Inches(0.5)

    # Table paragraphs should not receive body-paragraph indentation.
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    set_paragraph_spacing(paragraph)
                    paragraph.paragraph_format.left_indent = Inches(0)
                    paragraph.paragraph_format.first_line_indent = Inches(0)

                    for run in paragraph.runs:
                        set_run_font(run)


def format_run_in_headings(doc):
    """Convert APA heading levels 4 and 5 into run-in headings."""
    paragraphs = list(doc.paragraphs)

    for index, heading in enumerate(paragraphs[:-1]):
        style_name = heading.style.name

        if style_name not in ("Heading 4", "Heading 5"):
            continue

        following = paragraphs[index + 1]

        # A run-in heading must be followed by ordinary paragraph text.
        if not following.text.strip():
            continue

        if following.style.name.startswith("Heading"):
            continue

        if not heading.runs:
            continue

        # APA run-in headings end with a period.
        last_run = heading.runs[-1]

        if not last_run.text.endswith("."):
            last_run.text = last_run.text.rstrip() + "."

        # The heading and paragraph must occupy the same paragraph.
        heading.add_run(" ")

        for element in list(following._p):
            if element.tag == qn("w:pPr"):
                continue

            heading._p.append(copy.deepcopy(element))

        # Remove the separate paragraph after merging its content.
        following._p.getparent().remove(following._p)

        heading.paragraph_format.left_indent = Inches(0)
        heading.paragraph_format.first_line_indent = Inches(0.5)
        heading.paragraph_format.keep_with_next = False
        set_paragraph_spacing(heading)


def format_references(doc):
    """Apply APA hanging indents to reference entries."""
    in_references = False

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text.casefold() == "references":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.left_indent = Inches(0)
            paragraph.paragraph_format.first_line_indent = Inches(0)
            paragraph.paragraph_format.keep_with_next = True

            for run in paragraph.runs:
                run.bold = True
                set_run_font(run)

            set_paragraph_spacing(paragraph)
            in_references = True
            continue

        if not in_references:
            continue

        if paragraph.style.name.startswith("Heading"):
            in_references = False
            continue

        if not text:
            continue

        paragraph.paragraph_format.left_indent = Inches(0.5)
        paragraph.paragraph_format.first_line_indent = Inches(-0.5)
        set_paragraph_spacing(paragraph)

        for run in paragraph.runs:
            set_run_font(run)
