import json
import os
import re
import time
from urllib.parse import urlparse
import feedparser
import requests

# 監視したいRSSフィードのリスト
FEEDS = {
    "FF11公式 トピックス": "http://www.playonline.com/ff11/polnews/topics.xml",
    "FF11公式 インフォメーション": "http://www.playonline.com/ff11/polnews/news.xml",
    "FF11公式 開発・運営だより": "http://www.playonline.com/ff11/polnews/letter.xml",
    "FF11公式 関連情報": "http://www.playonline.com/ff11/polnews/event.xml",
}

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"
MAX_HISTORY = 50  # 記憶しておく既読URLの最大数

# 枠の左側の色（16進数カラーコード）
# 0x9B59B6 = アルタナちゃんパープル / 0xE67E22 = RSSオレンジ
EMBED_COLOR = 0x9B59B6


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def clean_html(raw_html):
    """RSSの概要欄に含まれるHTMLタグを綺麗に除去する"""
    if not raw_html:
        return ""
    # <br>や</p>を改行に変換してから残りのタグを消す
    text = re.sub(r"<br\s*/?>|</p>", "\n", raw_html, flags=re.IGNORECASE)
    text = re.sub(r"<.*?>", "", text)
    # 連続する改行や空白を整える
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    # 長すぎる場合は300文字で省略
    if len(text) > 300:
        text = text[:300] + "..."
    return text


def post_to_discord(feed_name, entry):
    title = entry.get("title", "無題")
    link = entry.get("link", "")
    summary = clean_html(entry.get("summary", entry.get("description", "")))
    domain = urlparse(link).netloc

    # Discordのカード型（Embed）データを作成
    embed = {
        "title": title,
        "url": link,
        "description": summary,
        "color": EMBED_COLOR,
        "footer": {
            "text": f"{feed_name} ({domain})"
        }
    }

    payload = {
        # カードの上に一言添えたい場合は下のコメントアウトを外してね
        # "content": f"📡 **アルタナちゃんアンテナが新着情報をキャッチしましたっ！**",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload)
    time.sleep(1)


def main():
    if not WEBHOOK_URL:
        print("Webhook URLが設定されていないわ！")
        return

    state = load_state()
    updated = False

    for feed_name, feed_url in FEEDS.items():
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            continue

        seen_links = state.get(feed_name, [])
        if isinstance(seen_links, str):
            seen_links = [seen_links]

        # 初回実行時は最新1件だけ通知
        if not seen_links:
            latest = feed.entries[0]
            post_to_discord(feed_name, latest)
            state[feed_name] = [entry.link for entry in feed.entries][:MAX_HISTORY]
            updated = True
            continue

        # 未読の記事を抽出
        new_entries = [entry for entry in feed.entries if entry.link not in seen_links]

        if new_entries:
            for entry in reversed(new_entries):
                post_to_discord(feed_name, entry)
                seen_links.insert(0, entry.link)

            state[feed_name] = seen_links[:MAX_HISTORY]
            updated = True

    if updated:
        save_state(state)


if __name__ == "__main__":
    main()
