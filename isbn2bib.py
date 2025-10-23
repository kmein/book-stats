#!/usr/bin/env python3
import sys
import requests
import re
from datetime import datetime, timezone

def bibtex_escape(text):
    """Escape special characters for BibTeX."""
    if not text:
        return ""
    return (text.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("#", "\\#")
                .replace("_", "\\_")
                .replace("{", "\\{")
                .replace("}", "\\}")).strip()

def fetch_openlibrary(isbn):
    """Fetch book metadata from OpenLibrary."""
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return data.get(f"ISBN:{isbn}", {})

def to_bibtex(data, isbn):
    """Convert OpenLibrary JSON data to a BibTeX entry."""
    title = bibtex_escape(data.get("title", ""))
    publishers = data.get("publishers", [])
    publisher = bibtex_escape(publishers[0]["name"]) if publishers else ""

    # Extract a year from publish_date
    year = ""
    if "publish_date" in data:
        m = re.search(r"\d{4}", data["publish_date"])
        if m:
            year = m.group(0)

    authors = data.get("authors", [])
    author_str = " and ".join(
        [bibtex_escape(a["name"]) for a in authors if "name" in a]
    )

    # Build a simple citation key
    first_author = author_str.split(" and ")[0].split()[-1] if author_str else "anon"
    bibkey = re.sub(r"\W+", "", first_author) + year

    pages = data.get("number_of_pages", "")
    if isinstance(pages, int):
        pages = str(pages)

    added_date = datetime.today()

    fields = {
        "author": author_str,
        "title": title,
        "publisher": publisher,
        "year": year,
        "isbn": isbn,
        "added": added_date.strftime("%Y-%m-%d"),
        "pagetotal": pages,
    }

    field_lines = [f"  {k} = {{{v}}}" for k, v in fields.items() if v]
    entry = f"@book{{{bibkey},\n" + ",\n".join(field_lines) + "\n}\n"
    return entry

def main():
    if len(sys.argv) != 2:
        print("Usage: isbn2bib.py <ISBN>", file=sys.stderr)
        sys.exit(1)

    isbn = sys.argv[1].replace("-", "").strip()
    data = fetch_openlibrary(isbn)

    if not data:
        print(f"# No record found for ISBN {isbn}", file=sys.stderr)
        sys.exit(2)

    print(to_bibtex(data, isbn))

if __name__ == "__main__":
    main()
