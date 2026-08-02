"""
論文ポッドキャスト自動配信システム - メイン処理
環境変数から認証情報を取得し、
1. Notion から「音声完成」ステータスのエピソードを取得
2. Google Drive から音声ファイルの公開URLを取得
3. RSS XML を生成して rss/feed.xml に出力
4. Notion のステータスを「配信済み」に更新
"""
import os
import sys
from src.notion_client import NotionPodcastClient
from src.google_drive_client import GoogleDriveClient
from src.rss_generator import RSSGenerator


def main():
    notion_api_key = os.environ.get("NOTION_API_KEY")
    notion_database_id = os.environ.get("NOTION_DATABASE_ID")
    google_service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    google_drive_folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")

    if not all([notion_api_key, notion_database_id,
                google_service_account_json, google_drive_folder_id]):
        print("必要な環境変数が設定されていません。")
        sys.exit(1)

    notion = NotionPodcastClient(notion_api_key, notion_database_id)
    drive = GoogleDriveClient(google_service_account_json, google_drive_folder_id)
    episodes = notion.get_completed_episodes()
    print(f"「音声完成」ステータスのエピソード: {len(episodes)} 件")

    if not episodes:
