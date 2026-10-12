"""コマンドの入口。`python3 -m expenses summary FILE`。"""

import argparse
import sys
from datetime import datetime

from expenses.core import format_summary, load_rows, summarize


def build_parser():
    parser = argparse.ArgumentParser(prog="expenses", description="家計簿の CSV を集計する")
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="カテゴリごとの合計を出す")
    summary.add_argument("file", help="CSV ファイル（列: date,category,amount）")
    summary.add_argument("--month", help="集計する月（YYYY-MM）")
    return parser


def valid_month(value):
    try:
        datetime.strptime(value, "%Y-%m")
    except ValueError:
        return False
    return len(value) == 7


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "summary":
        if args.month and not valid_month(args.month):
            print(f"エラー: invalid month: {args.month}（YYYY-MM で指定）", file=sys.stderr)
            return 2
        try:
            rows = load_rows(args.file)
        except FileNotFoundError:
            print(f"エラー: ファイルが見つからない: {args.file}", file=sys.stderr)
            return 1
        if args.month:
            rows = [row for row in rows if row["date"].startswith(args.month + "-")]
        print(format_summary(summarize(rows)))
        return 0
    return 2
