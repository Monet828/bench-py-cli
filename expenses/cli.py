"""コマンドの入口。`python3 -m expenses summary FILE`。"""

import argparse
import re
import sys

from expenses.core import format_summary, load_rows, summarize


def build_parser():
    parser = argparse.ArgumentParser(prog="expenses", description="家計簿の CSV を集計する")
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="カテゴリごとの合計を出す")
    summary.add_argument("file", help="CSV ファイル（列: date,category,amount）")
    summary.add_argument("--month", help="対象の月（YYYY-MM）。指定した月の行だけ集計する")
    return parser


def is_valid_month(value):
    """4桁の年・ハイフン・2桁の月（01〜12）なら True。"""
    return re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", value) is not None


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "summary":
        if args.month is not None and not is_valid_month(args.month):
            print(
                f"エラー: --month は YYYY-MM 形式（月は01〜12）で指定する: {args.month}",
                file=sys.stderr,
            )
            return 1
        try:
            rows = load_rows(args.file)
        except FileNotFoundError:
            print(f"エラー: ファイルが見つからない: {args.file}", file=sys.stderr)
            return 1
        print(format_summary(summarize(rows, args.month)))
        return 0
    return 2
