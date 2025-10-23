#!/usr/bin/env python3
import csv, sys, re

def bibtex_escape(text):
    """Escape characters that can break BibTeX."""
    if text is None:
        return ""
    text = (text.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("#", "\\#")
                .replace("_", "\\_")
                .replace("{", "\\{")
                .replace("}", "\\}"))
    return text.strip()

def csv_to_bib(stdin, stdout):
    reader = csv.DictReader(stdin)
    entries = []

    for i, row in enumerate(reader, start=1):
        item_type = (row.get("item_type") or "misc").lower()
        type_map = {
            "book": "book",
            "movie": "misc",
            "music": "misc",
            "game": "misc",
        }
        entry_type = type_map.get(item_type, "misc")

        # Build key
        last = re.sub(r'\W+', '', row.get("last_name", "")) or "item"
        year_match = re.findall(r'\d{4}', row.get("publish_date", "") or "")
        year = year_match[0] if year_match else "n.d."
        key = f"{last}{year}{i}"

        # Map basic fields
        fields = {
            "title": bibtex_escape(row.get("title")),
            "author": bibtex_escape(f"{row.get('last_name','')}, {row.get('first_name','')}"),
            "publisher": bibtex_escape(row.get("publisher")),
            "year": year,
            "isbn": bibtex_escape(row.get("ean_isbn13") or row.get("upc_isbn10")),
            "abstract": bibtex_escape(row.get("description")),
            "price": bibtex_escape(row.get("price")),
        }

        # Include all other columns as custom fields
        for k, v in row.items():
            if not v or not v.strip():
                continue
            if k in fields:
                continue
            fields[k] = bibtex_escape(v)

        field_lines = [f"  {k} = {{{v}}}" for k, v in fields.items() if v]
        entry = f"@{entry_type}{{{key},\n" + ",\n".join(field_lines) + "\n}\n"
        entries.append(entry)

    stdout.write("\n".join(entries))
    stdout.flush()

if __name__ == "__main__":
    csv_to_bib(sys.stdin, sys.stdout)
