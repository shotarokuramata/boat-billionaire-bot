# 競艇レース分析・自動通知システム

競艇のレース情報を自動取得・分析し、設定された条件に基づいて対象レースを抽出・通知する自動化システムです。

## 主要機能

### 1. レース情報の自動取得・分析
- **対象サイト**: 競艇日和 (kyoteibiyori.com)
- **取得データ**: 選手の統計情報、レース環境情報
- **分析機能**: 設定された条件に基づく自動フィルタリング

### 2. 条件マッチング機能
以下の項目に基づいて対象レースを判定：
- 逃げ率（年間/半年間）
- 許容逃げ率（年間/半年間）
- 突き刺し率（年間）
- 捲り率（年間）
- 直近10レースでの1着回数

### 3. 自動メール通知機能
- **分析結果の通知**: 対象レースの詳細情報
- **結果レポート**: レース結果と予想精度の検証
- **添付ファイル**: CSV形式のデータファイル

### 4. データ出力機能
- **CSV出力**: 対象レースの詳細データ
- **結果追跡**: レース結果の自動取得・記録

## 送信データの詳細

### 1. 初回分析結果メール（main.py実行時）

#### 件名
```
bot実行結果 会場NO:{会場番号} 日付:{実行日}
```

#### 送信データ内容
各レースについて以下の情報を含む：

**基本情報**
- レースURL
- 判定結果メッセージ

**統計データ（対象レースのみ）**
- `escape_last_year`: 年間逃げ率
- `escape_last_half_year`: 半年間逃げ率
- `allow_escape_last_year`: 年間許容逃げ率
- `allow_escape_last_half_year`: 半年間許容逃げ率
- `pierce_last_year`: 年間突き刺し率
- `overtake_last_year`: 年間捲り率
- `first_place_in_last_ten_race`: 直近10レースでの1着回数

#### メール本文例
```
Race URL: https://www.boatrace.jp/owpc/pc/race/racelist?rno=01&jcd=01&hd=20241129
Message: 対象データです
Data: RaceDataDTO(escape_last_year=6.5, escape_last_half_year=6.8, ...)
----------------------------------------
Race URL: https://www.boatrace.jp/owpc/pc/race/racelist?rno=02&jcd=01&hd=20241129
Message: データを抽出しましたが、条件に合致しませんでした。
----------------------------------------
```

### 2. 結果レポートメール（main_result.py実行時）

#### 件名
```
レース結果
```

#### 送信データ内容
**添付ファイル**: `{実行日}_result.csv`

**CSVファイル構成**
1. **レース基本情報**
   - `race_url`: レースURL
   - 統計データ（上記と同じ7項目）

2. **レース結果データ**
   - `rank_1` ~ `rank_6`: 1着〜6着の艇番
   
3. **レース環境データ**
   - `race_distance`: レース距離
   - `wind_speed`: 風速
   - `wind_direction`: 風向
   - `wave`: 波高
   - `won_by`: 決まり手

#### 本文
```
本日の分析対象レースの結果を添付します。
```

## 技術仕様

### 使用技術
- **Python**: メイン言語
- **Playwright**: ブラウザ自動化（ヘッドレスChrome）
- **BeautifulSoup**: HTMLパースィング
- **pandas**: データ処理
- **Gmail SMTP**: メール送信

### 設定ファイル
- `config.json`: メール送信設定
- `config_race_data.json`: 抽出条件設定

### 実行コマンド
```bash
# レース分析実行
python main.py {レース会場番号}

# 結果取得・通知
python main_result.py
```

## セットアップ

1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

2. 設定ファイルの作成
```bash
cp config.example.json config.json
# config.jsonを編集してGmail設定を入力
```

※gmailのパスワードについて、アプリパスワードを発行する必要があります。

参考:https://support.google.com/accounts/answer/185833?hl=ja

3. 条件設定の調整
```bash
# config_race_data.jsonを編集して抽出条件を設定
# 0を設定した場合、その項目については判定されない
```

## 出力ファイル

### 生成されるファイル
- `csv/{実行日}.csv`: 対象レースの基本データ
- `csv/{実行日}_result.csv`: 結果を含む完全データ
- `output.txt`: 実行ログ（必要に応じて）

### データ保存場所
- `csv/`: CSVファイル保存ディレクトリ
- プロジェクトルート: 設定ファイル

## 注意事項

- 1レース場に限定して実行（回線負荷軽減）
- Gmail アプリパスワードの設定が必要
- ブラウザセッションの適切な管理
- 条件値を0に設定すると該当項目を無効化

