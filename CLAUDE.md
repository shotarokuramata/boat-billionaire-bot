# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

このプロジェクトは競艇のレース情報を取得し、設定された条件に基づいて対象レースを抽出するPythonアプリケーションです。対象レースの結果を自動的にメール送信する機能も含まれています。

## 主要コマンド

### 依存関係のインストール
```bash
pip install -r requirements.txt
```

### メインアプリケーションの実行
```bash
python main.py {レース会場番号}
```

### レース結果の取得
```bash
python main_result.py
```

### テストの実行
```bash
python test.py
```

## アーキテクチャ

### コアモジュール
- `main.py`: メインエントリーポイント。レース会場番号を引数に取り、対象レースの抽出を実行
- `main_result.py`: 抽出されたレースの結果を取得し、メール送信を実行
- `get_boat_data.py`: 競艇公式サイトからレース情報をスクレイピング
- `get_kyotei_biyori.py`: 競艇日和サイトからフレーム情報を取得
- `mail.py`: Gmail APIを使用してメール送信機能を提供

### データモデル (dto/)
- `data.py`: レースデータのDTO（RaceDataDTO）。レース統計情報を保持し、設定された条件との照合機能を提供
- `report.py`: レポートデータのDTO（ReportDTO）。レース結果の報告データを構造化

### 設定ファイル
- `config.json`: メール送信用の認証情報（Gmail設定）
- `config_race_data.json`: レース抽出条件の閾値設定
- `config.example.json`: 設定ファイルのテンプレート

### データフロー
1. 指定されたレース会場の全ラウンド（1-12）を順次処理
2. 各ラウンドについて競艇日和サイトから統計データを取得
3. RaceDataDTOの`is_target()`メソッドで設定条件との照合
4. 条件に合致するレースを抽出し、結果をメール送信

### 技術スタック
- **Webスクレイピング**: Playwright（ヘッドレスChrome）、BeautifulSoup、requests
- **データ処理**: pandas、dataclasses
- **メール送信**: Gmail SMTP（アプリパスワード認証）
- **出力形式**: CSV、テキスト

## 重要な注意事項

### 設定要件
- `config.json`の作成が必須（Gmail認証情報）
- Gmailアプリパスワードの発行が必要
- `config_race_data.json`で抽出条件の閾値を設定（0設定で該当項目を無効化）

### 実行制限
- 1レース場に限定して実行（回線負荷軽減のため）
- Playwrightブラウザセッションの適切な管理

### データ出力
- CSV形式でレース結果を保存（`csv/`ディレクトリ）
- メール送信によるレポート配信機能