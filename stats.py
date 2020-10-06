#!/usr/bin/env python3

import argparse
import csv
import sys

import pandas
import matplotlib.pyplot


def report_text(path):
    try:
        df = pandas.read_csv(path)

        title_count = df["title"].count()
        author_count = df["author"].drop_duplicates().count()
        top_5_authors = (
            df.groupby("author")
            .count()
            .sort_values(by="title", ascending=False)["title"]
            .head(5)
        )

        by_genre = df.groupby("genre").count()
        genre_percent = (
            (by_genre["title"] / by_genre["title"].sum()) * 100
        ).sort_values(ascending=False)

        print(f"- Total books: {title_count}")
        print(f"- Total authors: {author_count}")
        print()

        print("# Top 5 authors")
        for author, titles in top_5_authors.iteritems():
            print(f"- {author} ({titles} titles)")
            # print(f"{index+1}. {row['author']}")
        print()

        print("# Genres")
        for genre, percent in genre_percent.iteritems():
            print(f"- {genre} ({percent:.2f}%)")

    except Exception as e:
        print(e, file=sys.stderr)
        print(f"File {path} does not exist", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report about read books")
    parser.add_argument("file", metavar="PATH", type=str, help="data file")
    args = parser.parse_args()
    report_text(args.file)
