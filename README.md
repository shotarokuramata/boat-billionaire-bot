# bort-billionaire-bot

<h2>導入手順</h2>

1. requirement.txtの内容をpipでインストールする

```
pip install -r requirements.txt
```

2. config.jsonを作成

config.example.jsonの内容を参考に、必要情報を設定する。

※gmailのパスワードについて、アプリパスワードを発行する必要がある。

参考:https://support.google.com/accounts/answer/185833?hl=ja

3. config_race_data.jsonの編集

対象レースのデータについて、閾値を設定する

※0を設定した場合、その項目については判定されない

4. 実行

対象レースの抽出を実行

```
python main.py {レース会場番号}
```

抽出した対象レースの結果を取得

```
python main_result.py
```
