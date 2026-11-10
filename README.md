# 📡 Altana Antenna (アルタナちゃんアンテナ)

![RSS Check Status](https://github.com/qtarou0621/altana-antenna/actions/workflows/rss_check.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-Private%20Use-purple.svg)

**Altana Antenna** は、特定のRSSフィード（主に『ファイナルファンタジーXI』公式情報など）を定期巡回し、新着記事を検知して Discord サーバーへリッチな Embed（カード形式）で自動通知するサーバーレス Bot です。

---

## ✨ 特徴 (Features)

* **完全サーバーレス & ランニングコスト 0円**
  * GitHub Actions の定期実行（cron）を利用して 15分周期で自動巡回します。
* **取りこぼし防止 & スパム防止設計**
  * 過去最大50件分の既読URLを `state.json` で状態管理し、複数記事の同時更新も時系列順に漏らさず通知します。初回登録時は最新1件のみを通知し、過去ログの大量連投を防ぎます。
* **Discord Embed 対応**
  * HTMLタグを自動整形し、アルタナちゃんのイメージカラー（パープル）をあしらった見やすいカード形式で概要を配信します。

---

## 🛠️ アーキテクチャ & 構成ファイル

| ファイル名 | 役割 |
| :--- | :--- |
| `rss_bot.py` | RSSフィードの取得・解析・HTML整形・Discord Webhook 送信を行うメインスクリプト |
| `state.json` | 通知済み記事の URL 履歴を保持するステートファイル（Actions により自動更新） |
| `.github/workflows/rss_check.yml` | 定期実行（15分周期）および状態コミットを制御する GitHub Actions ワークフロー |

---

## 📡 監視対象フィード (Target Feeds)

* **FF11公式 トピックス** (`topics.xml`)
* **FF11公式 インフォメーション** (`news.xml`)
* **FF11公式 開発・運営だより** (`letter.xml`)
* **FF11公式 関連情報** (`event.xml`)

---

## ⚙️ セットアップ (For Fork / Reference)

1. リポジトリの **Settings > Secrets and variables > Actions** に以下の Repository secret を登録します。
   * `DISCORD_WEBHOOK_URL`: 通知先 Discord チャンネルの Webhook URL
2. `rss_bot.py` 内の `FEEDS` 辞書に監視したい RSS フィードの名称と URL を定義します。
