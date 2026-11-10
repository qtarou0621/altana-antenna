# 📡 Altana Antenna (アルタナちゃんアンテナ)

![RSS Check Status](https://github.com/qtarou0621/altana-antenna/actions/workflows/rss_check.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-Private%20Use-purple.svg)

**Altana Antenna** は、特定のRSSフィード（『ファイナルファンタジーXI』公式情報など）を定期巡回し、新着記事を検知して Discord サーバーへリッチな Embed（カード形式）で自動通知するサーバーレス Bot です。

---

## ✨ 特徴 (Features)

* **完全サーバーレス & ランニングコスト 0円**
  * GitHub Actions の定期実行（cron）を利用して自動巡回します。
* **取りこぼし防止 & スパム防止設計**
  * 最大50件分の既読URLを `state.json` で管理し、複数記事の同時更新も時系列順に漏らさず通知します。初回登録時は最新1件のみを通知し、過去ログの大量連投を防ぎます。
* **Discord Embed 対応**
  * HTMLタグを自動整形し、アルタナちゃんのイメージカラー（パープル）をあしらったカード形式で配信します。

---

## 🛠️ 構成ファイル (Files)

| ファイル名 | 役割 |
| :--- | :--- |
| `rss_bot.py` | RSSの取得・解析・HTML整形・Discord Webhook 送信を行うメインスクリプト |
| `state.json` | 通知済み記事の URL 履歴を保持するステートファイル（Actions により自動更新） |
| `.github/workflows/rss_check.yml` | 定期実行（15分周期）および状態コミットを制御するワークフロー |

---

## 📡 監視対象フィード (Target Feeds)

* **FF11公式 トピックス** (`topics.xml`)
* **FF11公式 インフォメーション** (`news.xml`)
* **FF11公式 開発・運営だより** (`letter.xml`)
* **FF11公式 関連情報** (`event.xml`)

---

## 📦 インストール・セットアップ手順 (Installation)

もしゼロから同じ仕組みを構築・複製する場合の手順です。

### 1. リポジトリの作成
* GitHub上で新しいリポジトリ（例：`altana-antenna`）を **Public** で作成し、`Add a README file` にチェックを入れます。

### 2. シークレット（秘密情報）の設定
1. リポジトリの **Settings** ＞ **Secrets and variables** ＞ **Actions** を開きます。
2. **New repository secret** をクリックし、以下を登録します。
   * **Name**: `DISCORD_WEBHOOK_URL`
   * **Secret**: Discordで発行した Webhook URL

### 3. ファイルの配置
以下の3つのファイルをリポジトリのルート（および `.github/workflows/` フォルダ内）に作成・配置します。
1. `rss_bot.py` （メインコード）
2. `state.json` （中身は `{}` のみ）
3. `.github/workflows/rss_check.yml` （ワークフロー定義）

### 4. 動作確認
* Actions タブを開き、**Altana Antenna RSS Check** ＞ **Run workflow** から手動テスト実行を行い、Discordに通知が飛ぶことを確認します。
