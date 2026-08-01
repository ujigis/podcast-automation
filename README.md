# 論文ポッドキャスト自動配信システム

NotebookLM の Audio Overview 機能で生成した論文解説音声を、
Notion + Google Drive + GitHub Actions + RSS フィードを使って
Spotify に自動配信するシステムです。

## 仕組み

1. NotebookLM で論文の Audio Overview（音声）を生成
2. 音声ファイルを Google Drive にアップロード
3. Notion Database にエピソード情報を登録（ステータス：音声完成）
4. GitHub Actions が毎日自動実行され、RSS フィードを生成
5. Spotify for Podcasters が RSS フィードを自動検出し、エピソードを配信

## セットアップ

詳細なセットアップ手順は、配布された各種セットアップガイドを参照してください。

必要な GitHub Secrets:

- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `GOOGLE_DRIVE_FOLDER_ID`

## ファイル構成

```
podcast-automation/
├── .github/workflows/podcast-deploy.yml  # 自動実行ワークフロー
├── src/
│   ├── notion_client.py       # Notion API クライアント
│   ├── google_drive_client.py # Google Drive API クライアント
│   └── rss_generator.py       # RSS 生成モジュール
├── rss/feed.xml                # 生成される RSS フィード
├── main.py                     # メイン処理
└── requirements.txt             # Python 依存パッケージ
```

## RSS フィード URL

```
https://raw.githubusercontent.com/ujigis/podcast-automation/main/rss/feed.xml
```

このURLを Spotify for Podcasters に登録してください。
