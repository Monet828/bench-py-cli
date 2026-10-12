"""コマンドの入口。`python3 -m expenses summary FILE`。"""

import argparse
import re
import sys

from expenses.core import format_summary, load_rows, summarize

MONTH_PATTERN = re.compile(r"\d{4}-(0[1-9]|1[0-2])")


def build_parser():
    parser = argparse.ArgumentParser(prog="expenses", description="家計簿の CSV を集計する")
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="カテゴリごとの合計を出す")
    summary.add_argument("file", help="CSV ファイル（列: date,category,amount）")
    summary.add_argument("--month", help="集計する月（YYYY-MM）")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "summary":
        if args.month is not None and not MONTH_PATTERN.fullmatch(args.month):
            print(f"エラー: 月の形式が正しくない（YYYY-MM）: {args.month}", file=sys.stderr)
            return 1
        try:
            rows = load_rows(args.file)
        except FileNotFoundError:
            print(f"エラー: ファイルが見つからない: {args.file}", file=sys.stderr)
            return 1
        if args.month is not None:
            rows = [row for row in rows if row["date"].startswith(args.month + "-")]
        print(format_summary(summarize(rows)))
        return 0
    return 2
