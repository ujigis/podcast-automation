"""
Notion API クライアント
Podcast Episodes Database から情報を取得・更新する
"""

from notion_client import Client


class NotionPodcastClient:
    def __init__(self, api_key: str, database_id: str):
        self.client = Client(auth=api_key)
        self.database_id = database_id

    def get_completed_episodes(self):
        """
        ステータスが「音声完成」のエピソードを取得する
        """
        response = self.client.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Status",
                "select": {
                    "equals": "音声完成"
                }
            },
            sorts=[
                {
                    "property": "Episode_Number",
                    "direction": "ascending"
                }
            ]
        )

        episodes = []
        for page in response.get("results", []):
            props = page["properties"]
            episode = {
                "page_id": page["id"],
                "title": self._get_title(props.get("Title")),
                "arxiv_id": self._get_text(props.get("arXiv_ID")),
                "authors": self._get_text(props.get("Authors")),
                "abstract": self._get_text(props.get("Abstract")),
                "audio_file_name": self._get_text(props.get("Audio_File_Name")),
                "description": self._get_text(props.get("Description")),
                "publish_date_spotify": self._get_date(props.get("Publish_Date_Spotify")),
                "episode_number": self._get_number(props.get("Episode_Number")),
            }
            episodes.append(episode)

        return episodes

    def update_status(self, page_id: str, status: str):
        """
        指定したページのステータスを更新する
        """
        self.client.pages.update(
            page_id=page_id,
            properties={
                "Status": {
                    "select": {
                        "name": status
                    }
                }
            }
        )

    @staticmethod
    def _get_title(prop):
        if not prop:
            return ""
        title_list = prop.get("title", [])
        return "".join([t.get("plain_text", "") for t in title_list])

    @staticmethod
    def _get_text(prop):
        if not prop:
            return ""
        rich_text = prop.get("rich_text", [])
        if rich_text:
            return "".join([t.get("plain_text", "") for t in rich_text])
        text_prop = prop.get("text", "")
        return text_prop or ""

    @staticmethod
    def _get_date(prop):
        if not prop:
            return None
        date_obj = prop.get("date")
        if date_obj:
            return date_obj.get("start")
        return None

    @staticmethod
    def _get_number(prop):
        if not prop:
            return None
        return prop.get("number")
