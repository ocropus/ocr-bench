import re
import unicodedata
import editdistance

replacements = [
    ("\u2018", "'"),  # Left single quotation mark
    ("\u2019", "'"),  # Right single quotation mark
    ("\u201C", '"'),  # Left double quotation mark
    ("\u201D", '"'),  # Right double quotation mark
    ("\u2013", "-"),  # En dash
    ("\u2014", "-"),  # Em dash
    ("\u2015", "-"),  # Horizontal bar
    ("\u2026", "..."), # Ellipsis
    ("\u201A", ","),  # Single low-9 quotation mark
    ("\u201E", '"'),  # Double low-9 quotation mark
    ("\u2032", "'"),  # Prime, used as an apostrophe in some texts
    ("\u2033", '"'),   # Double prime, used as a quote in some texts
    ("\"", "''"),     # normalize double quotes to two single quotes
]

def normalize_text(text):
    text = text.strip()
    text = re.sub("\0c", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = text.strip()
    for old, new in replacements:
        text = re.sub(old, new, text)
    return text

def normalized_errors(text, gt):
    errs = editdistance.eval(
        normalize_text(text),
        normalize_text(gt)
    )
    return errs, len(normalize_text(gt))

def text_only(text):
    text = text.strip()
    text = re.sub("\0c", "", text)
    text = unicodedata.normalize("NFKD", text)
    return re.sub(r"[^a-zA-Z0-9]+", " ", text)

def text_errs(text, gt):
    errs = editdistance.eval(
        text_only(text).upper(),
        text_only(gt).upper()
    )
    return errs, len(text_only(gt))

class Something:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def add(self, other):
        self.value += other.value

class OCRErrors:
    def __init__(self):
        self.total, self.errors = 0, 0
        self.ttotal, self.terrors = 0, 0

    def add(self, text, gt):
        self.text, self.gt = text, gt
        errs, total = normalized_errors(text, gt)
        self.errors += errs
        self.total += total

        terrs, ttotal = text_errs(text, gt)
        self.terrors += terrs
        self.ttotal += ttotal

        if False and terrs > errs:
            raise ValueError(f"Text only errors ({terrs}) > normalized errors ({errs})")


        return errs, total, terrs, ttotal

    def __str__(self):
        return f"Normalized: {self.errors}/{self.total} ({self.errors/self.total:.4f})\n" + \
               f"Text only: {self.terrors}/{self.ttotal} ({self.terrors/self.ttotal:.4f})"
