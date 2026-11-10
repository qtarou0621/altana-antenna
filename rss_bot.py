import json
import os
import time
import feedparser
import requests

# 監視したいRSSフィードのリスト
FEEDS = {
    "FF11公式トピックス": "http://www.playonline.com/ff11/polnews/news.xml",
    # "きゅーちゃんYouTube": "https://www.youtube.com/feeds/videos.xml?channel_id=ここにチャンネルID",
}

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"
MAX_HISTORY = 50  # 記憶しておく既読URLの最大数

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def post_to_discord(feed_name, title, link):
    message = (
        f"📡 **アルタナちゃんアンテナが新着情報をキャッチしましたっ！**\n"
        f"【{feed_name}】\n"
        f"**{title}**\n"
        f"{link}"
    )
    requests.post(WEBHOOK_URL, json={"content": message})
    # Discordのレートリミット（連投制限）対策で1秒待つ
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

        # 過去に通知したURLのリストを取得（旧バージョンの文字列データにも対応）
        seen_links = state.get(feed_name, [])
        if isinstance(seen_links, str):
            seen_links = [seen_links]

        # 初回実行時（まだ履歴が空っぽの時）は、過去記事の大量連投を防ぐため最新1件だけ通知
        if not seen_links:
            latest = feed.entries[0]
            post_to_discord(feed_name, latest.title, latest.link)
            # 今ある記事すべてを「既読」として記録
            state[feed_name] = [entry.link for entry in feed.entries][:MAX_HISTORY]
            updated = True
            continue

        # 未読の記事をすべて抽出する
        new_entries = [entry for entry in feed.entries if entry.link not in seen_links]

        if new_entries:
            # 古い順（時系列順）に並び替えてから順番に通知する
            for entry in reversed(new_entries):
                post_to_discord(feed_name, entry.title, entry.link)
                seen_links.insert(0, entry.link)

            # 履歴が肥大化しないように直近50件に絞って保存
            state[feed_name] = seen_links[:MAX_HISTORY]
            updated = True

    if updated:
        save_state(state)

if __name__ == "__main__":
    main()
