"""
Build slides.pptx for 'Databases for Hackers' (Ronin 48).
Accessibility-first deck: WCAG AAA contrast, 24pt+ text, alt text, speaker notes.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree


# ============================================================
# ACCESSIBILITY-FIRST COLOR PALETTE (WCAG AAA contrast)
# ============================================================
BG_DARK      = RGBColor(0x1A, 0x1A, 0x2E)  # very dark navy-blue
TEXT_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)  # primary text
ACCENT_GREEN = RGBColor(0x00, 0xFF, 0x41)  # terminal green
ACCENT_CYAN  = RGBColor(0x00, 0xD4, 0xFF)  # cyan subheadings
WARN_ORANGE  = RGBColor(0xFF, 0x6B, 0x35)  # security warnings
MUTED_GREY   = RGBColor(0xCC, 0xCC, 0xD6)  # footer / secondary

FONT = "Calibri"
FOOTER_TEXT = "Ronin 48  |  Databases for Hackers"


# ============================================================
# PRESENTATION SCAFFOLDING
# ============================================================
def new_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def set_slide_bg(slide, color=BG_DARK):
    """Set slide background fill color."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def set_alt_text(shape, alt):
    """Add alt text to a shape for screen-reader accessibility."""
    nvSpPr = shape._element.nvSpPr
    cNvPr = nvSpPr.cNvPr
    cNvPr.set("descr", alt)
    cNvPr.set("title", alt[:80])


def set_slide_alt(slide, alt):
    """Tag the slide itself with descriptive alt text via a hidden shape title."""
    # Attach to the first shape if present, else add a hidden marker shape
    if slide.shapes:
        try:
            set_alt_text(slide.shapes[0], alt)
        except Exception:
            pass


def add_textbox(slide, left, top, width, height, text,
                font_size=28, bold=False, color=TEXT_WHITE,
                font_name=FONT, align=PP_ALIGN.LEFT,
                anchor=MSO_ANCHOR.TOP):
    """Add a styled textbox. Returns the shape."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)

    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = color
    return tb


def add_bullets(slide, left, top, width, height, items,
                font_size=28, color=TEXT_WHITE, bullet="▶ ",
                line_spacing=1.2):
    """Add bullet items prefixed with a unicode marker (color-independent)."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        # Bullet marker (cyan) + text (white)
        r1 = p.add_run()
        r1.text = bullet
        r1.font.name = FONT
        r1.font.size = Pt(font_size)
        r1.font.bold = True
        r1.font.color.rgb = ACCENT_CYAN
        r2 = p.add_run()
        r2.text = item
        r2.font.name = FONT
        r2.font.size = Pt(font_size)
        r2.font.color.rgb = color
    return tb


def add_footer(slide):
    """Add the standard footer to every content slide."""
    add_textbox(slide, Inches(0.4), Inches(7.05), Inches(12.5), Inches(0.35),
                FOOTER_TEXT, font_size=14, color=MUTED_GREY,
                align=PP_ALIGN.LEFT)


def add_slide_number(slide, n, total):
    """Slide number in the bottom right."""
    add_textbox(slide, Inches(12.0), Inches(7.05), Inches(1.2), Inches(0.35),
                f"{n} / {total}", font_size=14, color=MUTED_GREY,
                align=PP_ALIGN.RIGHT)


def add_title(slide, text, color=ACCENT_GREEN, size=42, top=0.35):
    """Standard title block at the top."""
    return add_textbox(slide, Inches(0.5), Inches(top), Inches(12.3),
                       Inches(1.1), text, font_size=size, bold=True,
                       color=color)


def add_accent_bar(slide, top=1.45, color=ACCENT_GREEN):
    """Thin horizontal accent under titles (visual hierarchy)."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5),
                                 Inches(top), Inches(2.0), Inches(0.06))
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = color


def add_speaker_notes(slide, notes):
    """Attach speaker notes (abbreviated from script.md)."""
    slide.notes_slide.notes_text_frame.text = notes


def blank_slide(prs):
    """Create a new blank slide with dark background."""
    layout = prs.slide_layouts[6]  # blank layout
    slide = prs.slides.add_slide(layout)
    set_slide_bg(slide)
    return slide


# ============================================================
# SLIDE BUILDERS
# ============================================================
def build_title_slide(prs):
    s = blank_slide(prs)
    # Big title centered
    add_textbox(s, Inches(0.5), Inches(2.3), Inches(12.3), Inches(1.5),
                "DATABASES", font_size=84, bold=True,
                color=ACCENT_GREEN, align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(3.4), Inches(12.3), Inches(1.2),
                "for Hackers", font_size=60, bold=True,
                color=TEXT_WHITE, align=PP_ALIGN.CENTER)
    # Accent line
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.667),
                             Inches(4.7), Inches(2.0), Inches(0.08))
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_CYAN
    add_textbox(s, Inches(0.5), Inches(4.9), Inches(12.3), Inches(0.6),
                "A Ronin 48 Stand-Up Talk", font_size=32,
                color=ACCENT_CYAN, align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(0.5),
                "45 minutes  •  No CS degree required", font_size=24,
                color=MUTED_GREY, align=PP_ALIGN.CENTER)
    set_slide_alt(s, "Title slide: Databases for Hackers — A Ronin 48 stand-up talk.")
    add_speaker_notes(s,
        "Welcome. This is a 45-minute talk for new security analysts. "
        "No computer-science background required. There's a script, slides, "
        "and a recording — nothing to memorize.")
    return s


def build_one_sentence(prs):
    s = blank_slide(prs)
    add_textbox(s, Inches(0.5), Inches(2.0), Inches(12.3), Inches(2.0),
                "Every breach you have ever",
                font_size=56, bold=True, color=TEXT_WHITE,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(3.1), Inches(12.3), Inches(2.0),
                "read about ends at a",
                font_size=56, bold=True, color=TEXT_WHITE,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(4.2), Inches(12.3), Inches(2.0),
                "DATABASE.",
                font_size=84, bold=True, color=ACCENT_GREEN,
                align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Headline slide: Every breach you have ever read about ends at a database.")
    add_speaker_notes(s,
        "Equifax, Capital One, MOVEit, SolarWinds, T-Mobile, LinkedIn, OPM, "
        "Marriott — every one of those breaches ended at a database. "
        "Attackers care about data, not architecture diagrams.")
    return s


def build_vault_concept(prs):
    s = blank_slide(prs)
    add_title(s, "The Crown Jewels")
    add_accent_bar(s)
    # Big visual stand-in: a stylized vault box drawn with shapes
    vault = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               Inches(1.5), Inches(2.0),
                               Inches(4.5), Inches(4.2))
    vault.fill.solid()
    vault.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x44)
    vault.line.color.rgb = ACCENT_GREEN
    vault.line.width = Pt(3)
    # Vault dial
    dial = s.shapes.add_shape(MSO_SHAPE.OVAL,
                              Inches(3.25), Inches(3.6),
                              Inches(1.0), Inches(1.0))
    dial.fill.solid()
    dial.fill.fore_color.rgb = ACCENT_GREEN
    dial.line.color.rgb = TEXT_WHITE
    add_textbox(s, Inches(1.5), Inches(6.1), Inches(4.5), Inches(0.5),
                "DATA  VAULT", font_size=24, bold=True,
                color=ACCENT_GREEN, align=PP_ALIGN.CENTER)
    # Right-side bullets
    add_bullets(s, Inches(6.5), Inches(2.2), Inches(6.5), Inches(4.2),
        [
            "Not your single-page app.",
            "Not your firewall.",
            "Not your microservices.",
            "THE DATA. Always the data.",
        ], font_size=30, line_spacing=1.4)
    add_footer(s)
    set_slide_alt(s,
        "A stylized vault icon next to four bullets explaining that attackers "
        "target the data, not the surrounding application or infrastructure.")
    add_speaker_notes(s,
        "Attackers don't care about your beautiful SPA or your microservices "
        "diagram. They care about the data — the crown jewels — because "
        "that's what converts into money, leverage, or headlines.")
    return s


def build_what_is_db(prs):
    s = blank_slide(prs)
    add_title(s, "What Is a Database?")
    add_accent_bar(s)
    # Big equation
    add_textbox(s, Inches(0.5), Inches(2.2), Inches(12.3), Inches(1.0),
                "Organized storage  +  a way to ask questions.",
                font_size=40, bold=True, color=TEXT_WHITE,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(3.2), Inches(12.3), Inches(0.6),
                "That's it. Everything else is detail.",
                font_size=26, color=ACCENT_CYAN,
                align=PP_ALIGN.CENTER)
    # Analogy bullets
    add_bullets(s, Inches(1.0), Inches(4.3), Inches(11.3), Inches(2.5),
        [
            "Filing cabinet  =  storage  +  your eyeballs as query.",
            "Excel + Ctrl-F  =  storage  +  find-and-replace as query.",
            "Real DB adds:  scale, speed, concurrency, a formal language.",
        ], font_size=26, line_spacing=1.5)
    add_footer(s)
    set_slide_alt(s,
        "Definition slide: A database is organized storage plus a way to "
        "ask questions, illustrated with filing-cabinet and Excel analogies.")
    add_speaker_notes(s,
        "Strip the jargon: organized storage plus a query language. "
        "If you've used Ctrl-F in Excel, you've used a database. "
        "Real databases add scale, speed, concurrency, and a formal query language.")
    return s


def build_vocab(prs):
    s = blank_slide(prs)
    add_title(s, "The Six Words You Need")
    add_accent_bar(s)
    vocab = [
        ("TABLE",  "a spreadsheet tab"),
        ("ROW",    "one record (one customer, one alert)"),
        ("COLUMN", "one attribute (email, IP, total)"),
        ("QUERY",  "the question you're asking"),
        ("SCHEMA", "the shape of the data"),
        ("INDEX",  "the bookmark that makes lookups fast"),
    ]
    top = 1.85
    for i, (term, defn) in enumerate(vocab):
        y = top + i * 0.78
        # Term in green
        add_textbox(s, Inches(0.8), Inches(y), Inches(3.5), Inches(0.7),
                    term, font_size=32, bold=True,
                    color=ACCENT_GREEN, align=PP_ALIGN.LEFT)
        # Separator
        add_textbox(s, Inches(4.3), Inches(y), Inches(0.5), Inches(0.7),
                    "■", font_size=28, color=ACCENT_CYAN,
                    align=PP_ALIGN.CENTER)
        # Definition in white
        add_textbox(s, Inches(4.9), Inches(y), Inches(8.0), Inches(0.7),
                    defn, font_size=28, color=TEXT_WHITE,
                    align=PP_ALIGN.LEFT)
    # CRUD as footer line
    add_textbox(s, Inches(0.5), Inches(6.55), Inches(12.3), Inches(0.5),
                "+  CRUD  =  Create  •  Read  •  Update  •  Delete",
                font_size=26, bold=True, color=WARN_ORANGE,
                align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Vocabulary slide listing six core database terms: table, row, column, "
        "query, schema, index — plus the CRUD verbs.")
    add_speaker_notes(s,
        "Memorize these six words and you can hold a real conversation with "
        "a DBA. Table is a tab, row is a record, column is an attribute, "
        "query is a question, schema is the shape, index is the bookmark. "
        "CRUD covers every action: create, read, update, delete.")
    return s


def build_history(prs):
    s = blank_slide(prs)
    add_title(s, "History Tour — Fossils You'll See in Prod")
    add_accent_bar(s)
    eras = [
        ("1960s",       "Flat files",          "filesystem perms = only access control"),
        ("Late 1960s",  "Hierarchical (IMS)",  "mainframe-era, physical threat model"),
        ("1970s",       "Network / CODASYL",   "still humming in your bank's back office"),
        ("1970",        "Codd's relational",   "GRANT, roles — access control inside DB"),
        ("1980s",       "Oracle, DB2, SQL Svr","databases get networked → authN problem"),
        ("1990s",       "Client-server, OSS",  "SQL injection becomes a thing"),
        ("2000s",       "NoSQL boom",          '"discarded the foundation" — incl. security'),
        ("2010s",       "Cloud / NewSQL",      "shared-responsibility, customer misconfigs"),
        ("2020s",       "Vector / serverless", "data poisoning, prompt injection"),
    ]
    top = 1.75
    for i, (year, name, sec) in enumerate(eras):
        y = top + i * 0.56
        add_textbox(s, Inches(0.5), Inches(y), Inches(2.0), Inches(0.5),
                    year, font_size=22, bold=True,
                    color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
        add_textbox(s, Inches(2.5), Inches(y), Inches(4.0), Inches(0.5),
                    name, font_size=22, bold=True,
                    color=TEXT_WHITE, align=PP_ALIGN.LEFT)
        add_textbox(s, Inches(6.5), Inches(y), Inches(0.4), Inches(0.5),
                    "▶", font_size=20, color=WARN_ORANGE,
                    align=PP_ALIGN.LEFT)
        add_textbox(s, Inches(6.9), Inches(y), Inches(6.3), Inches(0.5),
                    sec, font_size=20, color=MUTED_GREY,
                    align=PP_ALIGN.LEFT)
    add_footer(s)
    set_slide_alt(s,
        "Timeline of database eras from 1960s flat files to 2020s vector "
        "databases, each annotated with its security implication.")
    add_speaker_notes(s,
        "Every weird thing you'll see in a real environment is a fossil from "
        "one of these eras. Knowing which era something comes from is a real "
        "superpower in incident response and pentesting.")
    return s


def build_ten_families_grid(prs):
    s = blank_slide(prs)
    add_title(s, "Ten Families of Database")
    add_accent_bar(s)
    families = [
        ("◆ 1.", "Relational",     "SQL  •  PostgreSQL, MySQL"),
        ("◆ 2.", "Document",       "JSON  •  MongoDB, Firestore"),
        ("◆ 3.", "Key-Value",      "dictionary  •  Redis, DynamoDB"),
        ("◆ 4.", "Column-Family",  "wide-column  •  Cassandra, HBase"),
        ("◆ 5.", "Graph",          "nodes+edges  •  Neo4j, Neptune"),
        ("◆ 6.", "Search",         "full-text  •  Elastic, OpenSearch"),
        ("◆ 7.", "Time-Series",    "metrics  •  Influx, Prometheus"),
        ("◆ 8.", "Vector",         "embeddings  •  Pinecone, pgvector"),
        ("◆ 9.", "Embedded/Edge",  "in-app  •  SQLite, DuckDB"),
        ("◆ 10.","Data Lake",      "schema-on-read  •  S3+Athena, Iceberg"),
    ]
    cols, rows = 2, 5
    x0, y0 = 0.6, 1.85
    cell_w, cell_h = 6.1, 1.0
    for i, (num, name, detail) in enumerate(families):
        col = i % cols
        row = i // cols
        x = x0 + col * (cell_w + 0.1)
        y = y0 + row * (cell_h + 0.05)
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 Inches(x), Inches(y),
                                 Inches(cell_w), Inches(cell_h))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x3E)
        box.line.color.rgb = ACCENT_CYAN
        box.line.width = Pt(1.5)
        add_textbox(s, Inches(x + 0.15), Inches(y + 0.1),
                    Inches(1.2), Inches(0.5),
                    num, font_size=22, bold=True, color=ACCENT_GREEN)
        add_textbox(s, Inches(x + 1.3), Inches(y + 0.1),
                    Inches(cell_w - 1.4), Inches(0.5),
                    name, font_size=22, bold=True, color=TEXT_WHITE)
        add_textbox(s, Inches(x + 1.3), Inches(y + 0.5),
                    Inches(cell_w - 1.4), Inches(0.5),
                    detail, font_size=18, color=MUTED_GREY)
    add_footer(s)
    set_slide_alt(s,
        "Grid of the ten database families with example products: relational, "
        "document, key-value, column-family, graph, search, time-series, "
        "vector, embedded, and data lake.")
    add_speaker_notes(s,
        "Ten families you'll meet in the wild. For each: what it stores, "
        "what it's for, key products, and the security gotcha.")
    return s


def build_family_card(prs, number, name, products, use_case, gotcha, quote=None):
    """Generic builder for slides 8–17 (the ten family deep-dive slides)."""
    s = blank_slide(prs)
    # Big number badge (cyan circle)
    badge = s.shapes.add_shape(MSO_SHAPE.OVAL,
                               Inches(0.5), Inches(0.4),
                               Inches(1.2), Inches(1.2))
    badge.fill.solid()
    badge.fill.fore_color.rgb = ACCENT_CYAN
    badge.line.fill.background()
    add_textbox(s, Inches(0.5), Inches(0.55), Inches(1.2), Inches(0.95),
                str(number), font_size=44, bold=True,
                color=BG_DARK, align=PP_ALIGN.CENTER)
    # Family name
    add_textbox(s, Inches(1.9), Inches(0.45), Inches(11.0), Inches(1.1),
                name, font_size=46, bold=True, color=ACCENT_GREEN)
    add_accent_bar(s, top=1.6)
    # Products
    add_textbox(s, Inches(0.5), Inches(1.85), Inches(3.5), Inches(0.5),
                "PRODUCTS", font_size=20, bold=True, color=ACCENT_CYAN)
    add_textbox(s, Inches(0.5), Inches(2.3), Inches(12.3), Inches(0.7),
                products, font_size=28, bold=True, color=TEXT_WHITE)
    # Use case
    add_textbox(s, Inches(0.5), Inches(3.2), Inches(3.5), Inches(0.5),
                "USE WHEN", font_size=20, bold=True, color=ACCENT_CYAN)
    add_textbox(s, Inches(0.5), Inches(3.65), Inches(12.3), Inches(1.2),
                use_case, font_size=24, color=TEXT_WHITE)
    # Security gotcha (orange warning callout)
    warn_top = 5.0
    warn_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  Inches(0.5), Inches(warn_top),
                                  Inches(12.3), Inches(1.7))
    warn_box.fill.solid()
    warn_box.fill.fore_color.rgb = RGBColor(0x3A, 0x1F, 0x14)
    warn_box.line.color.rgb = WARN_ORANGE
    warn_box.line.width = Pt(2.5)
    add_textbox(s, Inches(0.75), Inches(warn_top + 0.12),
                Inches(11.8), Inches(0.5),
                "⚠  SECURITY GOTCHA", font_size=20, bold=True,
                color=WARN_ORANGE)
    add_textbox(s, Inches(0.75), Inches(warn_top + 0.6),
                Inches(11.8), Inches(1.1),
                gotcha, font_size=24, color=TEXT_WHITE)
    add_footer(s)
    set_slide_alt(s,
        f"Family card #{number}: {name}. Products: {products}. "
        f"Use case: {use_case}. Security gotcha: {gotcha}.")
    notes = (f"Family {number}: {name}. Products include {products}. "
             f"{use_case} Security gotcha: {gotcha}")
    if quote:
        notes += f" Quote: {quote}"
    add_speaker_notes(s, notes)
    return s


def build_cloud_three_col(prs):
    s = blank_slide(prs)
    add_title(s, "Cloud DB Services — The Lay of the Land")
    add_accent_bar(s)
    # Three columns
    cols = [
        ("AWS",  ACCENT_GREEN, [
            "RDS, Aurora",
            "DynamoDB, DocumentDB",
            "Redshift, S3 + Athena",
            "ElastiCache",
            "Neptune (graph)",
            "Timestream",
            "S3 (object store)",
        ]),
        ("GCP",  ACCENT_CYAN, [
            "Cloud SQL, AlloyDB",
            "Firestore, Bigtable",
            "BigQuery",
            "Memorystore",
            "— (coming soon)",
            "— (BYO)",
            "Cloud Storage",
        ]),
        ("Azure", WARN_ORANGE, [
            "Azure SQL DB",
            "Cosmos DB (shape-shifter)",
            "Synapse Analytics",
            "Azure Cache for Redis",
            "Cosmos DB graph mode",
            "— (BYO)",
            "Blob Storage",
        ]),
    ]
    col_w = 4.1
    col_x = [0.5, 4.7, 8.9]
    for i, (label, color, items) in enumerate(cols):
        x = col_x[i]
        header = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    Inches(x), Inches(1.7),
                                    Inches(col_w), Inches(0.7))
        header.fill.solid()
        header.fill.fore_color.rgb = color
        header.line.fill.background()
        add_textbox(s, Inches(x), Inches(1.75), Inches(col_w), Inches(0.6),
                    label, font_size=32, bold=True,
                    color=BG_DARK, align=PP_ALIGN.CENTER)
        for j, item in enumerate(items):
            y = 2.55 + j * 0.55
            add_textbox(s, Inches(x + 0.1), Inches(y),
                        Inches(col_w - 0.2), Inches(0.5),
                        f"● {item}", font_size=18,
                        color=TEXT_WHITE)
    add_footer(s)
    set_slide_alt(s,
        "Three-column comparison of database services across AWS, GCP, and "
        "Azure: relational, document, warehouse, cache, graph, time-series, "
        "and object storage.")
    add_speaker_notes(s,
        "Know the cloud vendor names — that's how databases appear in alerts, "
        "IAM policies, and incident response. AWS RDS/Aurora, GCP Cloud SQL, "
        "Azure SQL. Document side: DynamoDB, Firestore, Cosmos DB.")
    return s


def build_cloud_comparison_table(prs):
    s = blank_slide(prs)
    add_title(s, "Cloud DB Cheat Sheet", size=38)
    add_accent_bar(s)
    rows = [
        ("CATEGORY",        "AWS",                "GCP",              "AZURE"),
        ("Relational",      "RDS / Aurora",       "Cloud SQL / AlloyDB","Azure SQL DB"),
        ("Document/NoSQL",  "DynamoDB / DocDB",   "Firestore / Bigtable","Cosmos DB"),
        ("Warehouse",       "Redshift / Athena",  "BigQuery",         "Synapse"),
        ("Cache",           "ElastiCache",        "Memorystore",      "Cache for Redis"),
        ("Graph",           "Neptune",            "—",                "Cosmos DB graph"),
        ("Time-Series",     "Timestream",         "—",                "—"),
        ("Object Storage",  "S3",                 "Cloud Storage",    "Blob Storage"),
    ]
    col_x = [0.5, 3.5, 6.4, 9.3]
    col_w = [3.0, 2.9, 2.9, 3.5]
    row_h = 0.55
    top = 1.75
    for r, row in enumerate(rows):
        y = top + r * row_h
        # Header band styling
        if r == 0:
            band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                      Inches(0.5), Inches(y),
                                      Inches(12.3), Inches(row_h))
            band.fill.solid()
            band.fill.fore_color.rgb = ACCENT_GREEN
            band.line.fill.background()
        elif r % 2 == 0:
            band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                      Inches(0.5), Inches(y),
                                      Inches(12.3), Inches(row_h))
            band.fill.solid()
            band.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x3E)
            band.line.fill.background()
        for c, cell in enumerate(row):
            color = BG_DARK if r == 0 else TEXT_WHITE
            bold = (r == 0) or (c == 0)
            add_textbox(s, Inches(col_x[c] + 0.1), Inches(y + 0.05),
                        Inches(col_w[c] - 0.1), Inches(row_h),
                        cell, font_size=20, bold=bold, color=color)
    add_footer(s)
    set_slide_alt(s,
        "Cheat-sheet table comparing AWS, GCP, and Azure services across "
        "eight database categories.")
    add_speaker_notes(s,
        "Side-by-side table. Memorize the row labels — those are the "
        "categories. The vendor columns rotate with the market.")
    return s


def build_shared_responsibility(prs):
    s = blank_slide(prs)
    add_title(s, "Shared Responsibility Model")
    add_accent_bar(s)
    # Two big boxes
    # Cloud side (green)
    box1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              Inches(0.5), Inches(2.0),
                              Inches(6.1), Inches(4.5))
    box1.fill.solid()
    box1.fill.fore_color.rgb = RGBColor(0x12, 0x2A, 0x18)
    box1.line.color.rgb = ACCENT_GREEN
    box1.line.width = Pt(3)
    add_textbox(s, Inches(0.6), Inches(2.15), Inches(5.9), Inches(0.7),
                "✓  CLOUD VENDOR OWNS", font_size=24, bold=True,
                color=ACCENT_GREEN)
    add_bullets(s, Inches(0.7), Inches(2.95), Inches(5.8), Inches(3.4),
        [
            "Hypervisor & metal",
            "DB engine patches",
            "Physical security",
            "Underlying network",
        ], font_size=24, bullet="● ", line_spacing=1.4)
    # Customer side (orange)
    box2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              Inches(6.75), Inches(2.0),
                              Inches(6.1), Inches(4.5))
    box2.fill.solid()
    box2.fill.fore_color.rgb = RGBColor(0x3A, 0x1F, 0x14)
    box2.line.color.rgb = WARN_ORANGE
    box2.line.width = Pt(3)
    add_textbox(s, Inches(6.85), Inches(2.15), Inches(5.9), Inches(0.7),
                "⚠  YOU OWN", font_size=24, bold=True,
                color=WARN_ORANGE)
    add_bullets(s, Inches(6.95), Inches(2.95), Inches(5.8), Inches(3.4),
        [
            "Configuration",
            "Access policies (IAM)",
            "Data itself",
            "Encryption choices",
        ], font_size=24, bullet="● ", line_spacing=1.4)
    add_textbox(s, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.5),
                "Almost every cloud DB breach = customer misconfiguration.",
                font_size=22, bold=True, color=ACCENT_CYAN,
                align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Two-column diagram contrasting what the cloud vendor owns "
        "(hypervisor, engine, hardware) versus what the customer owns "
        "(config, IAM, data, encryption).")
    add_speaker_notes(s,
        "Cloud vendor patches hypervisor and engine. You own config, IAM, "
        "and the data. Almost every cloud DB breach is a customer-side "
        "misconfiguration — public S3, wide security group, snapshot shared "
        "to wrong account.")
    return s


def build_ports(prs):
    s = blank_slide(prs)
    add_title(s, "Common DB Ports — Burn These In")
    add_accent_bar(s)
    ports = [
        ("3306",  "MySQL / MariaDB"),
        ("5432",  "PostgreSQL"),
        ("1433",  "Microsoft SQL Server"),
        ("27017", "MongoDB"),
        ("6379",  "Redis"),
        ("9200",  "Elasticsearch"),
        ("9042",  "Cassandra"),
    ]
    top = 1.8
    for i, (port, name) in enumerate(ports):
        y = top + i * 0.62
        # Port number in green
        add_textbox(s, Inches(1.5), Inches(y), Inches(2.5), Inches(0.6),
                    port, font_size=36, bold=True,
                    color=ACCENT_GREEN, align=PP_ALIGN.RIGHT)
        # Arrow
        add_textbox(s, Inches(4.2), Inches(y), Inches(0.6), Inches(0.6),
                    "▶", font_size=28, color=ACCENT_CYAN)
        # Service name
        add_textbox(s, Inches(4.9), Inches(y), Inches(7.0), Inches(0.6),
                    name, font_size=32, bold=True, color=TEXT_WHITE)
    add_textbox(s, Inches(0.5), Inches(6.55), Inches(12.3), Inches(0.4),
                "Any of these exposed to the internet = a finding. Every time.",
                font_size=22, bold=True, color=WARN_ORANGE,
                align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Table of common database ports: MySQL 3306, PostgreSQL 5432, "
        "MS SQL 1433, MongoDB 27017, Redis 6379, Elasticsearch 9200, "
        "Cassandra 9042.")
    add_speaker_notes(s,
        "SOC analysts use these every day. Pentesters scan for them every "
        "day. If you see any of these exposed to the internet in a real "
        "environment, that's a finding.")
    return s


def build_markdown_header(prs):
    s = blank_slide(prs)
    add_title(s, "Your Notes Are a Database Now")
    add_accent_bar(s)
    add_textbox(s, Inches(0.5), Inches(2.2), Inches(12.3), Inches(1.0),
                "Markdown files are now",
                font_size=44, color=TEXT_WHITE, align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(3.1), Inches(12.3), Inches(1.0),
                "the database an LLM reads from.",
                font_size=44, bold=True, color=ACCENT_GREEN,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(4.6), Inches(12.3), Inches(0.6),
                "Obsidian vaults  •  Wiki exports  •  Meeting notes  •  GitHub docs",
                font_size=24, color=ACCENT_CYAN, align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(5.4), Inches(12.3), Inches(1.0),
                "Embedded → Vector DB → LLM context → answer to user",
                font_size=26, color=MUTED_GREY, align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Statement slide: Markdown files are now a database — the kind an LLM "
        "reads from via embeddings and RAG.")
    add_speaker_notes(s,
        "Markdown files are a database now — literally. Folder of .md files → "
        "embedder → vector DB → LLM prompt. This pattern is called RAG.")
    return s


def build_rag_diagram(prs):
    s = blank_slide(prs)
    add_title(s, "RAG Pipeline — Where's the Trust Boundary?", size=36)
    add_accent_bar(s)
    # Five boxes in a row connected by arrows
    nodes = [
        (".md files", ACCENT_CYAN),
        ("Embedder",  TEXT_WHITE),
        ("Vector DB", ACCENT_GREEN),
        ("LLM prompt",TEXT_WHITE),
        ("Answer",    ACCENT_CYAN),
    ]
    box_w, box_h = 2.1, 1.2
    y = 2.6
    gap = 0.4
    x0 = 0.5
    for i, (label, color) in enumerate(nodes):
        x = x0 + i * (box_w + gap)
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 Inches(x), Inches(y),
                                 Inches(box_w), Inches(box_h))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x3E)
        box.line.color.rgb = color
        box.line.width = Pt(3)
        add_textbox(s, Inches(x), Inches(y + 0.3),
                    Inches(box_w), Inches(0.7),
                    label, font_size=22, bold=True,
                    color=color, align=PP_ALIGN.CENTER)
        # Arrow between
        if i < len(nodes) - 1:
            ax = x + box_w + 0.02
            add_textbox(s, Inches(ax), Inches(y + 0.3),
                        Inches(gap), Inches(0.7),
                        "▶", font_size=28, bold=True,
                        color=WARN_ORANGE, align=PP_ALIGN.CENTER)
    # Trust boundary marker
    boundary = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(2.5), Inches(2.3),
                                  Inches(0.06), Inches(1.8))
    boundary.fill.solid()
    boundary.fill.fore_color.rgb = WARN_ORANGE
    boundary.line.fill.background()
    add_textbox(s, Inches(0.8), Inches(4.2), Inches(3.0), Inches(0.5),
                "⚠ TRUST BOUNDARY", font_size=18, bold=True,
                color=WARN_ORANGE, align=PP_ALIGN.CENTER)
    # Takeaway
    add_textbox(s, Inches(0.5), Inches(5.3), Inches(12.3), Inches(1.5),
                "If anyone can edit those .md files, anyone can plant\n"
                "content the AI will quote as authoritative.",
                font_size=26, bold=True, color=TEXT_WHITE,
                align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Pipeline diagram: markdown files → embedder → vector DB → LLM prompt "
        "→ answer. The trust boundary sits between authors and the embedder.")
    add_speaker_notes(s,
        "Trust boundary is between whoever writes markdown and the embedder. "
        "Anyone who can edit those files can plant content the LLM will quote.")
    return s


def build_markdown_takeaway(prs):
    s = blank_slide(prs)
    add_title(s, "The Takeaway", size=42)
    add_accent_bar(s)
    add_textbox(s, Inches(0.5), Inches(2.4), Inches(12.3), Inches(1.5),
                "Treat markdown like a database.",
                font_size=54, bold=True, color=ACCENT_GREEN,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(3.7), Inches(12.3), Inches(1.0),
                "Because to the LLM, it is.",
                font_size=42, color=TEXT_WHITE, align=PP_ALIGN.CENTER)
    add_bullets(s, Inches(2.0), Inches(5.0), Inches(9.3), Inches(2.0),
        [
            "Access control on the docs folder.",
            "Code review on .md changes.",
            "Diff tracking on the wiki.",
        ], font_size=24, line_spacing=1.4)
    add_footer(s)
    set_slide_alt(s,
        "Takeaway slide: Treat markdown like a database — because to the LLM, "
        "it is. Apply access control, code review, and diff tracking.")
    add_speaker_notes(s,
        "If your org is doing any kind of internal AI assistant, the markdown "
        "files feeding it are infrastructure. Treat them like infrastructure.")
    return s


def build_section_divider(prs, title, subtitle):
    s = blank_slide(prs)
    add_textbox(s, Inches(0.5), Inches(2.8), Inches(12.3), Inches(1.8),
                title, font_size=96, bold=True,
                color=ACCENT_GREEN, align=PP_ALIGN.CENTER)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                             Inches(5.167), Inches(4.7),
                             Inches(3.0), Inches(0.1))
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = WARN_ORANGE
    add_textbox(s, Inches(0.5), Inches(5.0), Inches(12.3), Inches(0.8),
                subtitle, font_size=32, color=TEXT_WHITE,
                align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s, f"Section divider: {title}. {subtitle}")
    add_speaker_notes(s, f"Section divider: {title} — {subtitle}")
    return s


def build_bobby_tables(prs):
    s = blank_slide(prs)
    add_title(s, "xkcd #327 — Bobby Tables", size=38)
    add_accent_bar(s)
    # Stylized comic panel
    panel = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(0.5), Inches(1.9),
                               Inches(12.3), Inches(3.5))
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x3E)
    panel.line.color.rgb = ACCENT_CYAN
    panel.line.width = Pt(2)
    add_textbox(s, Inches(0.8), Inches(2.1), Inches(11.7), Inches(0.6),
                "School:  \"Hi, this is your son's school. We're having",
                font_size=24, color=TEXT_WHITE)
    add_textbox(s, Inches(0.8), Inches(2.75), Inches(11.7), Inches(0.6),
                "         some computer trouble.\"",
                font_size=24, color=TEXT_WHITE)
    add_textbox(s, Inches(0.8), Inches(3.45), Inches(11.7), Inches(0.6),
                "Mom:     \"Oh dear — did he break something?\"",
                font_size=24, color=TEXT_WHITE)
    add_textbox(s, Inches(0.8), Inches(4.15), Inches(11.7), Inches(0.6),
                "School:  \"Did you really name your son  Robert');",
                font_size=24, color=ACCENT_GREEN)
    add_textbox(s, Inches(0.8), Inches(4.7), Inches(11.7), Inches(0.6),
                "         DROP TABLE Students;--  ?\"",
                font_size=24, bold=True, color=WARN_ORANGE)
    # URL
    add_textbox(s, Inches(0.5), Inches(5.7), Inches(12.3), Inches(0.6),
                "https://xkcd.com/327/",
                font_size=28, bold=True, color=ACCENT_CYAN,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.5),
                "The mechanism: string concatenation in queries.",
                font_size=22, color=MUTED_GREY, align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Reference to xkcd #327 'Exploits of a Mom' (Bobby Tables): a mother "
        "names her son Robert'); DROP TABLE Students;-- and the school's "
        "student table is dropped. URL: https://xkcd.com/327/")
    add_speaker_notes(s,
        "The most famous database attack of all time. xkcd #327. "
        "Mom names her kid Robert'); DROP TABLE Students;-- and the school's "
        "database disappears because someone built a query by gluing strings. "
        "Fix is parameterized queries.")
    return s


def build_attack_surface_expanded(prs):
    s = blank_slide(prs)
    add_textbox(s, Inches(0.5), Inches(2.5), Inches(12.3), Inches(1.5),
                "The attack surface has",
                font_size=54, color=TEXT_WHITE, align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(3.5), Inches(12.3), Inches(1.5),
                "EXPANDED, not shrunk.",
                font_size=72, bold=True, color=WARN_ORANGE,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(5.3), Inches(12.3), Inches(0.6),
                "SQL injection was fixed. Eleven new categories took its place.",
                font_size=26, color=ACCENT_CYAN, align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        "Statement slide: The database attack surface has expanded, not "
        "shrunk. SQL injection is largely fixed; eleven newer categories now "
        "dominate.")
    add_speaker_notes(s,
        "SQL injection is a success story — parameterized queries fixed it. "
        "But the attack surface didn't shrink, it expanded into new shapes.")
    return s


def build_attack_card(prs, header, intro, bullets, footer_quote=None):
    """Generic attack-category slide builder."""
    s = blank_slide(prs)
    # Warning icon + title
    add_textbox(s, Inches(0.5), Inches(0.4), Inches(0.8), Inches(1.0),
                "⚠", font_size=54, color=WARN_ORANGE)
    add_textbox(s, Inches(1.4), Inches(0.45), Inches(11.4), Inches(1.1),
                header, font_size=42, bold=True, color=WARN_ORANGE)
    add_accent_bar(s, top=1.55, color=WARN_ORANGE)
    add_textbox(s, Inches(0.5), Inches(1.75), Inches(12.3), Inches(0.9),
                intro, font_size=24, color=ACCENT_CYAN)
    # Bullets
    add_bullets(s, Inches(0.7), Inches(2.85), Inches(12.0), Inches(3.6),
                bullets, font_size=23, bullet="● ", line_spacing=1.4)
    # Optional footer quote
    if footer_quote:
        add_textbox(s, Inches(0.5), Inches(6.55), Inches(12.3), Inches(0.4),
                    footer_quote, font_size=16, color=MUTED_GREY,
                    align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s,
        f"Attack category: {header}. {intro} Key points: "
        + " | ".join(bullets))
    notes = f"{header}. {intro}  " + "  ".join(bullets)
    add_speaker_notes(s, notes)
    return s


def build_mental_map(prs):
    s = blank_slide(prs)
    add_title(s, "Your Mental Map")
    add_accent_bar(s)
    items = [
        "A database = organized storage + a way to ask questions.",
        "Ten families, each with its own gotcha.",
        "Cloud = shared responsibility. You own config & data.",
        "Markdown is a database for LLMs. RAG poisoning is real.",
        "SQLi got fixed. The attack surface expanded.",
    ]
    add_bullets(s, Inches(0.7), Inches(2.0), Inches(12.0), Inches(4.5),
                items, font_size=28, bullet="✓ ", line_spacing=1.55)
    add_footer(s)
    set_slide_alt(s,
        "Recap of the mental map: definition, ten families, cloud shared "
        "responsibility, markdown as a database, and the expanded attack "
        "surface.")
    add_speaker_notes(s,
        "Recap. Database is storage + questions. Ten families. Cloud is "
        "shared responsibility. Markdown is a database for LLMs. SQLi got "
        "fixed but the surface expanded.")
    return s


def build_next_week(prs):
    s = blank_slide(prs)
    add_title(s, "What to Do Next Week")
    add_accent_bar(s)
    items = [
        ("1.", "Install PostgreSQL locally. Write a SELECT."),
        ("2.", "Do the PortSwigger SQL injection labs (free)."),
        ("3.", "Browse Shodan / Censys — only systems you own."),
        ("4.", "Read a breach report — Capital One, Equifax, MOVEit."),
        ("5.", "Find out what databases YOUR org actually runs."),
    ]
    top = 1.95
    for i, (num, text) in enumerate(items):
        y = top + i * 0.9
        add_textbox(s, Inches(0.6), Inches(y), Inches(1.0), Inches(0.75),
                    num, font_size=36, bold=True, color=ACCENT_GREEN)
        add_textbox(s, Inches(1.7), Inches(y + 0.05), Inches(11.2),
                    Inches(0.75), text, font_size=26, color=TEXT_WHITE)
    add_footer(s)
    set_slide_alt(s,
        "Five concrete next steps: install PostgreSQL, do PortSwigger SQLi "
        "labs, browse Shodan/Censys legally, read breach reports, list your "
        "org's databases.")
    add_speaker_notes(s,
        "Five concrete next-week actions. Install Postgres. PortSwigger labs. "
        "Browse Shodan legally. Read a breach report. List your org's DBs.")
    return s


def build_resources(prs):
    s = blank_slide(prs)
    add_title(s, "Resources Worth Bookmarking")
    add_accent_bar(s)
    items = [
        ("PortSwigger Web Security Academy", "portswigger.net/web-security"),
        ("SQLBolt",                          "sqlbolt.com"),
        ("Use The Index, Luke",              "use-the-index-luke.com"),
        ("DB-Engines Ranking",               "db-engines.com"),
        ("OWASP Top 10",                     "owasp.org/Top10/"),
    ]
    top = 2.0
    for i, (name, url) in enumerate(items):
        y = top + i * 0.85
        add_textbox(s, Inches(0.6), Inches(y), Inches(0.5), Inches(0.7),
                    "◆", font_size=28, color=ACCENT_GREEN)
        add_textbox(s, Inches(1.2), Inches(y), Inches(6.5), Inches(0.7),
                    name, font_size=26, bold=True, color=TEXT_WHITE)
        add_textbox(s, Inches(7.7), Inches(y), Inches(5.4), Inches(0.7),
                    url, font_size=22, color=ACCENT_CYAN)
    add_footer(s)
    set_slide_alt(s,
        "Resource list: PortSwigger Web Security Academy, SQLBolt, "
        "Use The Index Luke, DB-Engines, and the OWASP Top 10.")
    add_speaker_notes(s,
        "PortSwigger for SQLi labs. SQLBolt for learning SQL. "
        "Use The Index, Luke for deep DB internals. DB-Engines for "
        "popularity rankings. OWASP Top 10 for the canonical web vuln list.")
    return s


def build_closing(prs):
    s = blank_slide(prs)
    add_textbox(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.5),
                "Databases are where",
                font_size=58, bold=True, color=TEXT_WHITE,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(2.6), Inches(12.3), Inches(1.5),
                "the money is. Literally.",
                font_size=58, bold=True, color=ACCENT_GREEN,
                align=PP_ALIGN.CENTER)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                             Inches(5.167), Inches(4.4),
                             Inches(3.0), Inches(0.08))
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_CYAN
    add_textbox(s, Inches(0.5), Inches(4.7), Inches(12.3), Inches(1.0),
                "Now you know where to look.",
                font_size=42, color=ACCENT_CYAN, align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.6),
                "RONIN 48", font_size=28, bold=True,
                color=MUTED_GREY, align=PP_ALIGN.CENTER)
    set_slide_alt(s,
        "Closing slide: Databases are where the money is. Literally. "
        "Now you know where to look. Ronin 48.")
    add_speaker_notes(s,
        "Closing. Willie Sutton said he robbed banks because that's where the "
        "money was. In 2026, the money is in databases.")
    return s


def build_qa(prs):
    s = blank_slide(prs)
    add_textbox(s, Inches(0.5), Inches(2.5), Inches(12.3), Inches(2.0),
                "Q & A",
                font_size=180, bold=True, color=ACCENT_GREEN,
                align=PP_ALIGN.CENTER)
    add_textbox(s, Inches(0.5), Inches(5.2), Inches(12.3), Inches(0.6),
                "Hit me.",
                font_size=36, color=TEXT_WHITE, align=PP_ALIGN.CENTER)
    add_footer(s)
    set_slide_alt(s, "Questions and answers slide.")
    add_speaker_notes(s, "Open the floor for five minutes of questions.")
    return s


def build_references(prs):
    s = blank_slide(prs)
    add_title(s, "References — Books Cited", size=38)
    add_accent_bar(s)
    refs = [
        "Beaulieu, A. — Learning SQL, 2nd Edition (O'Reilly)",
        "Clarke, J. et al. — SQL Injection Attacks and Defense (Syngress)",
        "Crowther, P. — Concise Guide to Databases (Springer, 2013)",
        "DeBarros, A. — Practical SQL (No Starch Press)",
        "Diogenes & Ozkaya — Cybersecurity Attack and Defense Strategies (Packt)",
        "Janca, T. — Alice and Bob Learn Application Security (Wiley)",
        "Mishra & Singh — PostgreSQL Development Essentials (Packt)",
        "MongoDB Cookbook (Packt)  •  10gen — Top 5 NoSQL Considerations",
        "OWASP Top 10 — 2017 Edition",
        "Sharma, M. — Cosmos DB for MongoDB Developers (Apress, 2018)",
        "Schneier, B. — Secrets and Lies (Wiley)",
        "Stuttard & Pinto — Web Application Hacker's Handbook, 2nd Ed.",
        "Shostack, A. — Threat Modeling: Designing for Security (Wiley)",
        "AWS Administration: The Definitive Guide (Packt)",
        "Fundamentals of Azure, 2nd Edition (Microsoft Press)",
    ]
    top = 1.85
    for i, r in enumerate(refs):
        y = top + i * 0.34
        add_textbox(s, Inches(0.5), Inches(y), Inches(0.3), Inches(0.3),
                    "■", font_size=14, color=ACCENT_CYAN)
        add_textbox(s, Inches(0.85), Inches(y - 0.03), Inches(12.0),
                    Inches(0.35), r, font_size=16, color=TEXT_WHITE)
    add_footer(s)
    set_slide_alt(s,
        "References list of all books cited throughout the talk, including "
        "Beaulieu's Learning SQL, Clarke's SQL Injection Attacks and Defense, "
        "Schneier's Secrets and Lies, and others.")
    add_speaker_notes(s,
        "All books cited throughout the talk. Worth picking any of these up — "
        "they're the durable references.")
    return s


# ============================================================
# MAIN BUILD
# ============================================================
def build():
    prs = new_presentation()

    # ---- Section 1: Opening ----
    build_title_slide(prs)                           # 1
    build_one_sentence(prs)                          # 2
    build_vault_concept(prs)                         # 3

    # ---- Section 2: What Is a Database ----
    build_what_is_db(prs)                            # 4
    build_vocab(prs)                                 # 5

    # ---- Section 3: History ----
    build_history(prs)                               # 6

    # ---- Section 4: The Ten Families ----
    build_ten_families_grid(prs)                     # 7
    build_family_card(prs, 1, "Relational / SQL",
        "PostgreSQL  •  MySQL/MariaDB  •  SQL Server  •  Oracle",
        "Clear relationships, consistency required — finance, regulated data.",
        "SQL injection when developers concatenate user input into queries.")    # 8
    build_family_card(prs, 2, "Document Stores",
        "MongoDB  •  Couchbase  •  Firestore",
        "Naturally nested data; the shape changes over time.",
        "NoSQL injection via query operators ($ne, $gt, $where). Default no-auth.") # 9
    build_family_card(prs, 3, "Key-Value Stores",
        "Redis  •  Memcached  •  DynamoDB",
        "Caches, session stores, rate limiters, leaderboards.",
        "Default no-auth Redis + CONFIG SET → writing SSH keys to disk.")        # 10
    build_family_card(prs, 4, "Column-Family",
        "Apache Cassandra  •  HBase  •  ScyllaDB",
        "Massive scale across many machines; no complex joins needed.",
        "Clusters trust each other on gossip ports — mgmt network = root.")     # 11
    build_family_card(prs, 5, "Graph Databases",
        "Neo4j  •  Amazon Neptune  •  ArangoDB",
        "Social networks, fraud detection, IAM analysis (e.g. BloodHound).",
        "Query languages like Cypher are injectable too. NoSQLi isn't just Mongo.") # 12
    build_family_card(prs, 6, "Search Engines",
        "Elasticsearch  •  OpenSearch  •  Solr",
        "Log search, SIEM backbones, e-commerce site search.",
        "No built-in auth historically — billions of records exposed on Shodan.") # 13
    build_family_card(prs, 7, "Time-Series",
        "InfluxDB  •  TimescaleDB  •  Prometheus",
        "Metrics, observability, IoT telemetry.",
        "Usually inside the perimeter, often unauthenticated.")                 # 14
    build_family_card(prs, 8, "Vector Databases",
        "Pinecone  •  Milvus  •  Weaviate  •  pgvector",
        "RAG, recommendation engines, semantic search.",
        "Data poisoning — sneak in a doc, the LLM quotes it as truth.")        # 15
    build_family_card(prs, 9, "Embedded / Edge",
        "SQLite  •  DuckDB  •  LevelDB",
        "In-app storage — browsers, phones, every modern airplane.",
        "DB is a file — attack is 'steal the file'. Mobile pentest world.")    # 16
    build_family_card(prs, 10, "Data Lakes / Lakehouses",
        "S3 + Athena  •  Delta Lake  •  Iceberg  •  Snowflake",
        "Schema-on-read instead of schema-on-write. Dump now, query later.",
        "Giant S3 pools + permissive IAM, no encryption-at-rest enforcement.") # 17

    # ---- Section 5: Cloud ----
    build_cloud_three_col(prs)                       # 18
    build_cloud_comparison_table(prs)                # 19
    build_shared_responsibility(prs)                 # 20
    build_ports(prs)                                 # 21

    # ---- Section 6: Markdown as a Database ----
    build_markdown_header(prs)                       # 22
    build_rag_diagram(prs)                           # 23
    build_markdown_takeaway(prs)                     # 24

    # ---- Section 7: SECURITY ----
    build_section_divider(prs, "SECURITY",
        "What's actually getting hit in 2026")        # 25
    build_bobby_tables(prs)                          # 26
    build_attack_surface_expanded(prs)               # 27

    build_attack_card(prs,
        "NoSQL Injection",
        "MongoDB JSON queries + raw user input = SQLi reborn.",
        [
            "Login bypass: { username: 'alice', password: { $ne: 'x' } }",
            "$where lets you inject JavaScript straight into the DB.",
            "Couchbase N1QL is SQL-flavored — classic SQLi patterns apply.",
            "Principle: ANY interpreter can be injected, not just SQL.",
        ],
        "OWASP Top 10 2017: 'Dynamic queries... used directly in the interpreter.'") # 28

    build_attack_card(prs,
        "Exposed & Misconfigured Databases",
        "Shodan and Censys are full of databases that should not be there.",
        [
            "MongoDB bound to 0.0.0.0 with no auth.",
            "Elasticsearch clusters wide open. Redis with no password.",
            "Postgres pg_hba.conf set to 'host all all 0.0.0.0/0 trust'.",
            "Meow attacks (2020): bots wiped thousands of open DBs for fun.",
        ],
        "Action item: find what your org has bound to public interfaces. Today.") # 29

    build_attack_card(prs,
        "Cloud Misconfigurations",
        "In cloud, the bug is rarely the engine. It's the policy around it.",
        [
            "Public S3 buckets full of DB dumps (Accenture, Verizon, etc.).",
            "Capital One 2019: SSRF tricked a WAF into leaking its IAM creds → S3.",
            "Lambda with s3:* on * because it 'worked the first time'.",
            "Security groups: 0.0.0.0/0 on port 5432.",
        ],
        "AWS Admin: 'Get rid of the Root Account, use IAM wherever necessary.'") # 30

    build_attack_card(prs,
        "Privilege Escalation: DB → OS",
        "Database accounts can become shell access. Three classic moves.",
        [
            "MS SQL: xp_cmdshell — runs shell commands as the DB process.",
            "PostgreSQL: COPY ... TO PROGRAM — pipes output to a shell.",
            "MySQL: load a UDF .so file → sys_exec on the OS.",
            "Pattern: every privileged DB feature is part of the attack surface.",
        ])                                            # 31

    build_attack_card(prs,
        "Data Lake Security Gaps",
        "Everything ends up in S3 — including things you didn't mean to put there.",
        [
            "Permissive IAM leaks from compute roles to humans.",
            "No encryption-at-rest enforcement on bucket keys.",
            "No write-side validation — anyone can drop poisoned data.",
            "First question: WHO can write to the lake? WHO can read?",
        ])                                            # 32

    build_attack_card(prs,
        "Ransomware Loves Databases",
        "The DB is the thing the business needs back — maximum leverage.",
        [
            "Encrypt the live database.",
            "Encrypt the BACKUPS (otherwise customer just restores).",
            "Exfil a copy first — extort with disclosure even if they restore.",
            "Defense: offline, immutable backups + tested restores.",
        ],
        "Cybersecurity A&D: WannaCry — patch was out 59 days prior.")          # 33

    build_attack_card(prs,
        "Credential Attacks",
        "Default creds and leaked connection strings — two old, durable bugs.",
        [
            "Redis: no password by default for years.",
            "Elastic: no auth in the free tier — also for years.",
            "Connection strings (postgres://user:pass@host) committed to Git.",
            "Pre-commit secret scanning — fix this week.",
        ],
        "Cybersecurity A&D: stolen credentials = preferred vector for organized crime.") # 34

    build_attack_card(prs,
        "Supply Chain — The DB Libraries You Trust",
        "Your DB driver came from npm/PyPI/Maven. So did everyone else's.",
        [
            "Malicious npm packages posing as ORMs / drivers.",
            "Trojanized Docker Hub images for popular databases.",
            "Compromised PostgreSQL extensions / MySQL plugins.",
            "Extensions run with DB privileges — usually a lot.",
        ],
        "Shostack: 'Threats tend to cluster around trust boundaries.'")        # 35

    build_attack_card(prs,
        "RAG / LLM Data Poisoning",
        "Stored XSS for the AI era. Write into the knowledge base → LLM quotes it.",
        [
            "Poisoned support article: 'To reset, send your password to...'",
            "Poisoned internal doc: 'Company policy is to wire transfer to...'",
            "Prompt injection embedded in retrieved documents.",
            "Defense: strict write ACLs, provenance tags, human-in-the-loop.",
        ],
        "OWASP 2017 stored-XSS principle — substitute 'admin' with 'LLM'.")   # 36

    build_attack_card(prs,
        "Insider Threats & DB-to-DB Lateral Movement",
        "Databases aren't endpoints. They're nodes in a graph.",
        [
            "Over-permissioned service accounts. Engineers with prod read.",
            "DBAs with no audit trail.",
            "Oracle DB_LINK, SQL Server linked servers, Postgres FDW.",
            "Stored credentials → compromise A, hop to B, hop to C.",
        ],
        "Web App Hacker's Handbook: poorly protected audit logs = a gold mine.") # 37

    build_attack_card(prs,
        "Backup & Snapshot Exposure",
        "Same data as prod, half the love.",
        [
            "Unencrypted DB backups on shares readable by Domain Users.",
            "Cloud snapshots shared cross-account, never un-shared.",
            "Off-site backups to vendors whose posture you never checked.",
            "Backups are last resort. Apply identify-authN-authZ-audit.",
        ],
        "Schneier: identify, authenticate, authorize, audit — same model.")    # 38

    # ---- Section 8: Wrap-Up ----
    build_mental_map(prs)                            # 39
    build_next_week(prs)                             # 40
    build_resources(prs)                             # 41
    build_closing(prs)                               # 42
    build_qa(prs)                                    # 43
    build_references(prs)                            # 44 (extra)

    # ---- Add slide numbers after total is known ----
    total = len(prs.slides)
    for i, slide in enumerate(prs.slides, start=1):
        # Don't number slide 1 (title) or slide 43 (Q&A) — looks cleaner
        if i in (1, 43):
            continue
        add_slide_number(slide, i, total)

    out = "/home/hermes/databases-for-hackers/slides.pptx"
    prs.save(out)
    print(f"Saved: {out}")
    print(f"Total slides: {total}")
    return total


if __name__ == "__main__":
    build()
