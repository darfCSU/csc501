#!/usr/bin/env python3
"""Convert Markdown to DOCX with APA 7 student-paper formatting."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


class MarkdownToDocx:
    """Convert Markdown documents to APA-style Word documents."""

    APA_FIELDS = {
        "title",
        "student",
        "institution",
        "course",
        "instructor",
        "due_date",
    }

    def __init__(self, reference_doc=None):
        self.reference_doc = Path(reference_doc) if reference_doc else None

    @staticmethod
    def check_pandoc():
        """Verify that Pandoc is installed."""
        try:
            subprocess.run(
                ["pandoc", "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            raise RuntimeError(
                "Pandoc is required. Install it with: sudo apt install pandoc"
            ) from exc

    @staticmethod
    def _set_run_font(run):
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

        rpr = run._element.get_or_add_rPr()
        rfonts = rpr.rFonts

        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.insert(0, rfonts)

        for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
            rfonts.set(qn(f"w:{attribute}"), "Times New Roman")

    @staticmethod
    def _set_paragraph_spacing(paragraph):
        fmt = paragraph.paragraph_format
        fmt.line_spacing = 2
        fmt.space_before = Pt(0)
        fmt.space_after = Pt(0)

    @staticmethod
    def create_apa_template(template_path):
        """Create a basic Pandoc reference DOCX if none exists."""
        MarkdownToDocx.check_pandoc()

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
        section = doc.sections[0]
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

        for style_name in ("Normal", "Body Text", "First Paragraph"):
            try:
                style = doc.styles[style_name]
            except KeyError:
                continue

            style.font.name = "Times New Roman"
            style.font.size = Pt(12)
            style.paragraph_format.line_spacing = 2
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.space_after = Pt(0)

        for style_name in ("Heading 1", "Heading 2", "Heading 3"):
            style = doc.styles[style_name]
            style.font.name = "Times New Roman"
            style.font.size = Pt(12)
            style.font.bold = True
            style.paragraph_format.line_spacing = 2
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.space_after = Pt(0)
            style.paragraph_format.keep_with_next = True

        doc.styles["Heading 1"].paragraph_format.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )
        doc.styles["Heading 2"].paragraph_format.alignment = (
            WD_ALIGN_PARAGRAPH.LEFT
        )

        heading3 = doc.styles["Heading 3"]
        heading3.font.italic = True
        heading3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Add a page-number field to the header.
        header = section.header
        paragraph = header.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        run = paragraph.add_run()
        MarkdownToDocx._set_run_font(run)

        field = OxmlElement("w:fldSimple")
        field.set(qn("w:instr"), "PAGE")
        run._r.addnext(field)

        doc.save(template_path)
        return template_path

    @staticmethod
    def _insert_page_number(paragraph):
        """Insert a Word page-number field."""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        paragraph.paragraph_format.first_line_indent = Inches(0)

        run = paragraph.add_run()
        MarkdownToDocx._set_run_font(run)

        field = OxmlElement("w:fldSimple")
        field.set(qn("w:instr"), "PAGE")
        run._r.addnext(field)

    @staticmethod
    def _add_title_page(
        doc,
        title,
        student,
        institution,
        course,
        instructor,
        due_date,
    ):
        """Insert an APA 7 student title page at the beginning."""
        # Insert paragraphs in reverse order before the current first paragraph.
        first = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()

        # Remove a duplicate opening title if Markdown already begins with it.
        if title and first.text.strip() == title.strip():
            first._element.getparent().remove(first._element)

        first = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()

        # Use a page break before the body; the title page is built separately.
        fields = [
            (title, True),
            (student, False),
            (institution, False),
            (course, False),
            (instructor, False),
            (due_date, False),
        ]

        # Insert an explicit page break and the title-page content before body.
        anchor = first._p
        parent = anchor.getparent()
        index = parent.index(anchor)

        # Create a temporary title-page document so its paragraphs can be
        # inserted before the existing document body without losing content.
        title_doc = Document()
        title_section = title_doc.sections[0]
        title_section.top_margin = Inches(1)
        title_section.bottom_margin = Inches(1)
        title_section.left_margin = Inches(1)
        title_section.right_margin = Inches(1)

        # Match the header's page-number treatment.
        title_section.header.is_linked_to_previous = False
        title_section.header.paragraphs[0].clear()
        MarkdownToDocx._insert_page_number(
            title_section.header.paragraphs[0]
        )

        # APA student title pages position the title block about three
        # double-spaced lines below the top margin.
        for _ in range(2):
            p = title_doc.add_paragraph()
            MarkdownToDocx._set_paragraph_spacing(p)
            p.paragraph_format.first_line_indent = Inches(0)

        for value, is_title in fields:
            if not value:
                continue

            p = title_doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.right_indent = Inches(0)
            MarkdownToDocx._set_paragraph_spacing(p)

            run = p.add_run(str(value))
            MarkdownToDocx._set_run_font(run)
            run.bold = is_title

        # Import title-page paragraphs and section header into the output.
        # XML copying preserves formatting and the page-number field.
        title_elements = [
            element
            for element in title_doc.element.body
            if element.tag == qn("w:p")
        ]

        for offset, element in enumerate(title_elements):
            parent.insert(index + offset, element)

        # Add a page break immediately before the body.
        break_paragraph = OxmlElement("w:p")
        break_run = OxmlElement("w:r")
        break_element = OxmlElement("w:br")
        break_element.set(qn("w:type"), "page")
        break_run.append(break_element)
        break_paragraph.append(break_run)
        parent.insert(index + len(title_elements), break_paragraph)

        # Ensure the paper title appears at the top of page two.
        body_title = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")

        alignment = OxmlElement("w:jc")
        alignment.set(qn("w:val"), "center")
        ppr.append(alignment)

        spacing = OxmlElement("w:spacing")
        spacing.set(qn("w:line"), "480")
        spacing.set(qn("w:lineRule"), "auto")
        spacing.set(qn("w:before"), "0")
        spacing.set(qn("w:after"), "0")
        ppr.append(spacing)
        body_title.append(ppr)

        if title:
            run_element = OxmlElement("w:r")
            rpr = OxmlElement("w:rPr")

            fonts = OxmlElement("w:rFonts")
            fonts.set(qn("w:ascii"), "Times New Roman")
            fonts.set(qn("w:hAnsi"), "Times New Roman")
            rpr.append(fonts)

            size = OxmlElement("w:sz")
            size.set(qn("w:val"), "24")
            rpr.append(size)

            bold = OxmlElement("w:b")
            rpr.append(bold)
            run_element.append(rpr)

            text_element = OxmlElement("w:t")
            text_element.text = str(title)
            run_element.append(text_element)
            body_title.append(run_element)

        parent.insert(index + len(title_elements) + 1, body_title)

    @staticmethod
    def _format_references(doc):
        """Apply APA-style heading and hanging indents to references."""
        in_references = False

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()

            if text.casefold() == "references":
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.first_line_indent = Inches(0)
                paragraph.paragraph_format.left_indent = Inches(0)
                MarkdownToDocx._set_paragraph_spacing(paragraph)

                for run in paragraph.runs:
                    run.bold = True

                in_references = True
                continue

            if in_references:
                if paragraph.style.name.startswith("Heading"):
                    in_references = False
                    continue

                if text:
                    paragraph.paragraph_format.left_indent = Inches(0.5)
                    paragraph.paragraph_format.first_line_indent = Inches(-0.5)
                    MarkdownToDocx._set_paragraph_spacing(paragraph)

    @staticmethod
    def _format_body(doc):
        """Apply APA font and spacing to document paragraphs."""
        for paragraph in doc.paragraphs:
            if paragraph.style.name.startswith("Heading"):
                paragraph.paragraph_format.first_line_indent = Inches(0)
                paragraph.paragraph_format.keep_with_next = True
                MarkdownToDocx._set_paragraph_spacing(paragraph)
            elif paragraph.text.strip():
                paragraph.paragraph_format.line_spacing = 2
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(0)

                if paragraph.style.name not in ("Title",):
                    paragraph.paragraph_format.first_line_indent = Inches(0.5)

            for run in paragraph.runs:
                if run.font.size is None:
                    run.font.size = Pt(12)
                if run.font.name is None:
                    run.font.name = "Times New Roman"

    def apply_apa_formatting(
        self,
        input_path,
        output_path,
        title=None,
        student=None,
        institution="Colorado State University Global",
        course=None,
        instructor=None,
        due_date=None,
        template_path=None,
    ):
        """Convert Markdown to DOCX and apply APA student-paper formatting."""
        self.check_pandoc()

        input_path = Path(input_path).resolve()
        output_path = Path(output_path).resolve()

        if not input_path.is_file():
            raise FileNotFoundError(
                f"Markdown file not found: {input_path}"
            )

        if input_path == output_path:
            raise ValueError("Input and output files must be different.")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        template = (
            Path(template_path).resolve()
            if template_path
            else self.reference_doc
        )

        if template is None:
            template = (
                Path(__file__).resolve().parent / "apa-reference.docx"
            )

        if not template.is_file():
            raise FileNotFoundError(
                f"APA reference template not found: {template}\n"
                "Create it with: ./create_apa_template.py"
            )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            encoding="utf-8",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(input_path.read_text(encoding="utf-8"))

        try:
            subprocess.run(
                [
                    "pandoc",
                    str(temp_path),
                    "--from=markdown",
                    "--to=docx",
                    "--standalone",
                    f"--reference-doc={template}",
                    "-o",
                    str(output_path),
                ],
                check=True,
            )
        finally:
            temp_path.unlink(missing_ok=True)

        doc = Document(output_path)

        # Ensure the header includes a page-number field.
        for section in doc.sections:
            header = section.header
            if not header.paragraphs[0]._p.xpath(".//w:instrText"):
                header.paragraphs[0].clear()
                self._insert_page_number(header.paragraphs[0])

        self._format_body(doc)
        self._format_references(doc)

        # Save body formatting before inserting the title page.
        doc.save(output_path)

        doc = Document(output_path)
        self._add_title_page(
            doc,
            title=title,
            student=student,
            institution=institution,
            course=course,
            instructor=instructor,
            due_date=due_date,
        )

        doc.save(output_path)
        return output_path

    def convert(self, input_path, output_path=None, **kwargs):
        """Convert a Markdown file to DOCX."""
        input_path = Path(input_path)

        if output_path is None:
            output_path = input_path.with_suffix(".docx")

        return self.apply_apa_formatting(
            input_path,
            output_path,
            **kwargs,
        )

    def convert_config(self, config_path):
        """Convert a document using settings from a JSON configuration."""
        config_path = Path(config_path).expanduser().resolve()

        if not config_path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with config_path.open(encoding="utf-8") as config_file:
            config = json.load(config_file)

        if not isinstance(config, dict):
            raise ValueError("JSON configuration must contain an object.")

        # Relative paths always resolve from the script's directory.
        base_dir = Path(__file__).resolve().parent

        def resolve_path(value, default=None):
            if value is None:
                return default

            if not isinstance(value, str) or not value.strip():
                raise ValueError("Configured paths must be non-empty strings.")

            path = Path(value).expanduser()

            if not path.is_absolute():
                path = base_dir / path

            return path.resolve()

        input_path = resolve_path(config.get("input"))

        if input_path is None:
            raise ValueError("Configuration must specify 'input'.")

        output_path = resolve_path(
            config.get("output"),
            input_path.with_suffix(".docx"),
        )

        template_path = resolve_path(config.get("template"))
        apa = config.get("apa", {})

        if not isinstance(apa, dict):
            raise ValueError("'apa' must be a JSON object.")

        unknown_fields = set(apa) - self.APA_FIELDS
        if unknown_fields:
            raise ValueError(
                "Unknown APA configuration field(s): "
                + ", ".join(sorted(unknown_fields))
            )

        if "institution" not in apa:
            apa["institution"] = "Colorado State University Global"

        converter = MarkdownToDocx(template_path)

        return converter.convert(
            input_path,
            output_path,
            template_path=template_path,
            **apa,
        )


def main():
    if len(sys.argv) != 2:
        print(
            f"Usage: {Path(sys.argv[0]).name} config.json",
            file=sys.stderr,
        )
        return 2

    try:
        converter = MarkdownToDocx()
        output = converter.convert_config(Path(sys.argv[1]))
        print(f"Created: {output}")
        return 0

    except (
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

