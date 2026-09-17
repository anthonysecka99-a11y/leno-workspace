from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parents[1]
html_files = list(ROOT.glob("*.html"))
if not html_files:
    raise SystemExit("No HTML entry file found")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.has_viewport = False
        self.has_script = False
        self.ids = set()
        self.duplicate_ids = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag == "script":
            self.has_script = True
        if "id" in attrs:
            value = attrs["id"]
            if value in self.ids:
                self.duplicate_ids.append(value)
            self.ids.add(value)
    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
    @property
    def _in_title(self):
        # title text is checked separately with a simple regex below.
        return False

errors = []
for path in html_files:
    text = path.read_text(encoding="utf-8")
    if "<!doctype html>" not in text[:200].lower():
        errors.append(f"{path.name}: missing HTML5 doctype")
    if not re.search(r"<title>[^<]+</title>", text, re.I):
        errors.append(f"{path.name}: missing non-empty <title>")
    if not re.search(r'<meta[^>]+name=[\"\']viewport[\"\']', text, re.I):
        errors.append(f"{path.name}: missing viewport meta tag")
    parser = Parser()
    parser.feed(text)
    if parser.duplicate_ids:
        errors.append(f"{path.name}: duplicate ids: {', '.join(sorted(set(parser.duplicate_ids)))}")
    # Catch accidental hard-coded credential-looking assignments in frontend files.
    credential = re.search(r"(?:password|passwd|secret)\s*[:=]\s*['\"][^'\"]{6,}['\"]", text, re.I)
    if credential:
        errors.append(f"{path.name}: possible hard-coded credential detected")

if errors:
    print("LENO validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    raise SystemExit(1)

print(f"LENO validation passed: {len(html_files)} HTML file(s) checked.")
