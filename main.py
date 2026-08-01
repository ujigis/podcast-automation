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
        print("配信対象のエピソードがありません。処理を終了します。")
        return

    rss_episodes = []
    for ep in episodes:
        audio_file_name = ep.get("audio_file_name")
        if not audio_file_name:
            print(f"警告: {ep.get('title')} に Audio_File_Name が設定されていません。スキップします。")
            continue

        audio_url = drive.get_audio_file_url(audio_file_name)
        if not audio_url:
            print(f"警告: Google Drive に {audio_file_name} が見つかりません。スキップします。")
            continue

        ep["audio_url"] = audio_url
        rss_episodes.append(ep)

        # ステータスを配信済みに更新
        notion.update_status(ep["page_id"], "配信済み")
        print(f"配信済みに更新: {ep.get('title')}")

    generator = RSSGenerator(
        channel_title="論文ポッドキャスト",
        channel_description="arXivなどの学術論文をNotebookLMで音声化して配信するポッドキャストです。",
        channel_link="https://github.com/ujigis/podcast-automation",
        channel_image_url="",
        channel_language="ja",
        channel_author="あおきGISオープンデータ研究所",
        channel_category="Education",
    )

    rss_xml = generator.generate(rss_episodes)

    os.makedirs("rss", exist_ok=True)
    with open("rss/feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print("RSS フィードを rss/feed.xml に出力しました。")


if __name__ == "__main__":
    main()
