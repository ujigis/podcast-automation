"""
RSS 2.0 (iTunes/Spotify 対応) フィード生成モジュール
"""

from datetime import datetime
from email.utils import format_datetime
from xml.sax.saxutils import escape


class RSSGenerator:
    def __init__(
        self,
        channel_title: str,
        channel_description: str,
        channel_link: str,
        channel_image_url: str = "",
        channel_language: str = "ja",
        channel_author: str = "",
        channel_category: str = "Education",
    ):
        self.channel_title = channel_title
        self.channel_description = channel_description
        self.channel_link = channel_link
        self.channel_image_url = channel_image_url
        self.channel_language = channel_language
        self.channel_author = channel_author
        self.channel_category = channel_category

    def generate(self, episodes: list) -> str:
        items_xml = "\n".join(
            [self._episode_to_item(ep) for ep in episodes]
        )

        image_tag = ""
        if self.channel_image_url:
            image_tag = f'<itunes:image href="{escape(self.channel_image_url)}"/>'

        rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{escape(self.channel_title)}</title>
    <description>{escape(self.channel_description)}</description>
    <link>{escape(self.channel_link)}</link>
    <language>{self.channel_language}</language>
    <itunes:author>{escape(self.channel_author)}</itunes:author>
    <itunes:category text="{escape(self.channel_category)}"/>
    <itunes:explicit>false</itunes:explicit>
    {image_tag}
    <lastBuildDate>{format_datetime(datetime.utcnow())}</lastBuildDate>
{items_xml}
  </channel>
</rss>
"""
        return rss

    @staticmethod
    def _episode_to_item(ep: dict) -> str:
        title = escape(ep.get("title", ""))
        description = escape(ep.get("description") or ep.get("abstract", ""))
        audio_url = ep.get("audio_url", "")
        pub_date_str = ep.get("publish_date_spotify")

        if pub_date_str:
            try:
                pub_date = datetime.fromisoformat(pub_date_str)
            except ValueError:
                pub_date = datetime.utcnow()
        else:
            pub_date = datetime.utcnow()

        guid = escape(audio_url or title)

        return f"""    <item>
      <title>{title}</title>
      <description>{description}</description>
      <enclosure url="{escape(audio_url)}" type="audio/mpeg"/>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{format_datetime(pub_date)}</pubDate>
      <itunes:explicit>false</itunes:explicit>
    </item>"""
