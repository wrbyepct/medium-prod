# 🎯 專案目標

這個專案主要是想模擬「真的在公司裡」開發與部署 API 的完整流程。
從 DRF 架構風格、雲端部署、到自動化 DevOps 都一併實作，打造可擴充、可維護的後端系統。

* 🧱 用 Django REST Framework 打造類似 Medium 的 REST API

* 🐳 用 Docker 來容器化整個專案

* 🌐 用 NGINX 當反向代理、負責服務 static / media

* 🧪 使用 pytest 走 TDD（測試驅動開發）流程

* 🔍 pre-commit、linter、formatter 全套上好上滿

* ⚙️ DevOps 實戰內容包含：

  * Terraform（IaC）
  * GitHub Actions（CI/CD）
  * AWS 雲端部署

    * VPC（2 個 AZ，含 Public/Private Subnet）
    * RDS（PostgreSQL）
    * ECS + ECR（容器化 + Fargate 無伺服器部署）
    * ALB（負載平衡 + SSL）
    * Route53 + 自訂網域 + HTTPS

* 📨 其他周邊服務

  * Amazon SES（寄信通知）
  * OpenSearch（文章全文搜尋）
  * ElastiCache / Redis（配合 Celery 當任務隊列）

# 🧩 功能總覽

## 📚 文章（Articles）

* 使用者可建立、查看、更新、刪除自己的文章
* 文章可被評分（1～5 ⭐）

## 💬 回覆（Responses）

* 支援巢狀留言（回覆文章、也可回覆其他回覆）
* 使用者可編輯 / 刪除自己的留言

## 🔖 書籤（Bookmarks）

* 使用者會有一個預設的「閱讀清單」
* 可自訂書籤分類
* 文章可加入任意分類

## ⭐ 評分（Ratings）

* 文章可被 1～5 分評分

## 🙍‍♂️ 個人檔案（Profiles）

* 註冊後自動建立 Profile
* 可編輯暱稱、簡介等基本資訊

## 👥 追蹤（Followers）

* 可以追蹤 / 取消追蹤其他使用者
* 可查看粉絲與追蹤清單

## 📨 通知（Celery + SES）

* 當有人追蹤你時會寄信通知

# ⚙️ 技術架構（Tech Stack）

* **Backend**：Django、DRF、PostgreSQL
* **Queue**：Celery + Redis（ElastiCache）
* **Infra**：Terraform、ECS Fargate、RDS、ALB、ECR、Route53
* **CI/CD**：GitHub Actions
* **Security**：HTTPS、VPC 隔離、IAM 權限
* **Extra**：OpenSearch（搜尋）、Amazon SES（Email）、Docker Compose（本地開發）

# 🛠️ 本地開發使用方式

## 📦 前置需求

* Docker
* Poetry

## 下載專案

```bash
git clone https://github.com/wrbyepct/medium-prod.git
cd medium-prod
```

## Install package

```bash
poetry install
```

## Create environment file

```bash
cp .example.envs .envs   # 把 .django 與 .postgres 裡的參數填好
```

## Start services

```bash
docker-compose up --build
```

## Database migration

```bash
docker-compose exec web python -m core.manage migrate
```
