"""
Google Drive API クライアント
指定したフォルダ内の音声ファイルを検索し、公開URLを取得する
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleDriveClient:
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self, service_account_json: str, folder_id: str):
        credentials_info = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=self.SCOPES
        )
        self.service = build("drive", "v3", credentials=credentials)
        self.folder_id = folder_id

    def get_audio_file_url(self, file_name: str):
        """
        フォルダ内から指定したファイル名を検索し、
        公開設定にした上で直リンクURLを返す
        """
        query = (
            f"name = '{file_name}' and "
            f"'{self.folder_id}' in parents and "
            f"trashed = false"
        )
        results = self.service.files().list(
            q=query,
            fields="files(id, name)",
            pageSize=1
        ).execute()

        files = results.get("files", [])
        if not files:
            return None

        file_id = files[0]["id"]

        # 誰でも閲覧可能に設定
        self.service.permissions().create(
            fileId=file_id,
            body={
                "type": "anyone",
                "role": "reader"
            }
        ).execute()

        # 直接ダウンロード用URL
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return direct_url
