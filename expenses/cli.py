"""コマンドの入口。`python3 -m expenses summary FILE`。"""

import argparse
import sys

from expenses.core import format_summary, load_rows, summarize


def build_parser():
    parser = argparse.ArgumentParser(prog="expenses", description="家計簿の CSV を集計する")
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="カテゴリごとの合計を出す")
    summary.add_argument("file", help="CSV ファイル（列: date,category,amount）")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "summary":
        try:
            rows = load_rows(args.file)
        except FileNotFoundError:
            print(f"エラー: ファイルが見つからない: {args.file}", file=sys.stderr)
            return 1
        print(format_summary(summarize(rows)))
        return 0
    return 2
