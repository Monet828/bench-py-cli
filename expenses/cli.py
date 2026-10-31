"""コマンドの入口。`python3 -m expenses summary FILE`。"""

import argparse
import sys

from expenses.core import filter_by_month, format_summary, load_rows, summarize, validate_month


def build_parser():
    parser = argparse.ArgumentParser(prog="expenses", description="家計簿の CSV を集計する")
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="カテゴリごとの合計を出す")
    summary.add_argument("file", help="CSV ファイル（列: date,category,amount）")
    summary.add_argument("--month", help="対象の月（YYYY-MM）。指定すると、その月の行だけ集計する")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "summary":
        if args.month is not None:
            try:
                validate_month(args.month)
            except ValueError as e:
                print(f"エラー: {e}", file=sys.stderr)
                return 2
        try:
            rows = load_rows(args.file)
        except FileNotFoundError:
            print(f"エラー: ファイルが見つからない: {args.file}", file=sys.stderr)
            return 1
        if args.month is not None:
            rows = filter_by_month(rows, args.month)
        print(format_summary(summarize(rows)))
        return 0
    return 2
