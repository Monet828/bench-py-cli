"""CSV の読み込みと集計。"""

import csv


def load_rows(path):
    """CSV（列: date,category,amount）を読み、行の dict のリストを返す。amount は int（円）。"""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for record in csv.DictReader(f):
            rows.append(
                {
                    "date": record["date"].strip(),
                    "category": record["category"].strip(),
                    "amount": int(record["amount"]),
                }
            )
    return rows


def summarize(rows):
    """カテゴリごとの合計を dict で返す。"""
    totals = {}
    for row in rows:
        totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]
    return totals


def format_summary(totals):
    """集計を出力の行にする。カテゴリ名の順に「カテゴリ<TAB>金額」、最後に「合計<TAB>金額」。"""
    lines = [f"{category}\t{totals[category]}" for category in sorted(totals)]
    lines.append(f"合計\t{sum(totals.values())}")
    return "\n".join(lines)
