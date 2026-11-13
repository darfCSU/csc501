import json
import subprocess
import tempfile
from pathlib import Path

from docx import Document

from .formatting import (
    add_title_page,
    configure_header,
    format_body,
    format_references,
    format_run_in_headings,
)
from .template import create_apa_template


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
    def create_apa_template(template_path):
        """Create an APA reference DOCX template."""
        MarkdownToDocx.check_pandoc()
        return create_apa_template(template_path)

    @staticmethod
    def _prepare_markdown(markdown):
        """Replace {{PAGEBREAK}} markers with Word page breaks."""
        page_break = (
            '\n\n```{=openxml}\n'
            '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n'
            '```\n\n'
        )
        return markdown.replace("{{PAGEBREAK}}", page_break)

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
                Path(__file__).resolve().parent.parent / "apa-reference.docx"
            )

        if not template.is_file():
            raise FileNotFoundError(
                f"APA reference template not found: {template}\n"
                "Create it with: python -c "
                "'from md2docx import MarkdownToDocx; "
                "MarkdownToDocx.create_apa_template(\"apa-reference.docx\")'"
            )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            encoding="utf-8",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            markdown = input_path.read_text(encoding="utf-8")
            temp_file.write(self._prepare_markdown(markdown))

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

        # Ensure all sections have the correct page-number header.
        for section in doc.sections:
            configure_header(section)

        # Apply document formatting.
        format_body(doc)
        format_run_in_headings(doc)
        format_references(doc)

        # Save before adding the title page.
        doc.save(output_path)

        # Insert the title page and repeat the title on page two.
        doc = Document(output_path)

        add_title_page(
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

        # Relative paths resolve from the script's directory.
        base_dir = Path(__file__).resolve().parent.parent

        def resolve_path(value, default=None):
            if value is None:
                return default

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    "Configured paths must be non-empty strings."
                )

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
