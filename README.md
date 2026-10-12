# bench-py-cli

家計簿の CSV をカテゴリごとに集計する小さな CLI。Python 3 の標準ライブラリだけで動き、依存はない。

AI Worker の評価（Mission Bench）の題材として使う Repo。

## 使い方

```sh
python3 -m expenses summary sample.csv
python3 -m unittest            # 試験
```

## 入力

UTF-8 の CSV。1 行目は見出しで、列は `date,category,amount`。

- `date` — `YYYY-MM-DD`
- `category` — カテゴリ名
- `amount` — 金額（円、整数）

## 出力

カテゴリ名の順に `カテゴリ<TAB>金額` を 1 行ずつ、最後に `合計<TAB>金額` を出す。

```
food	3550
rent	72000
transport	690
合計	76240
```

ファイルが無いときは標準エラーに理由を出し、終了コード 1 で終わる。

## 構成

- `expenses/core.py` — CSV の読み込み・集計・出力の整形
- `expenses/cli.py` — コマンドの入口
- `tests/` — 試験（unittest）
