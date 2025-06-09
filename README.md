# 🎯 Project Objectives
This project is designed to simulate a real-world API development and deployment environment. It emphasizes scalable architecture, DRF best practices, cloud deployment, and automation.

- 🧱 Build a Medium-like REST API using Django REST Framework

- 🐳 Containerize the project using Docker

- 🌐 Use NGINX as a reverse proxy for serving static/media files

- 🧪 Follow test-driven development (TDD) using pytest

- 🔍 Enforce code quality via pre-commit, linters, and formatters

- ⚙️ Practice DevOps with:

    - Terraform (Infrastructure as Code)

    - GitHub Actions (CI/CD)

    - AWS Cloud Deployment:

    - VPC with public/private subnets across 2 AZs

    - RDS (PostgreSQL) for relational data

    - ECS + ECR for containerized, serverless deployments

    - ALB for routing and SSL

    - Route53 + HTTPS via custom domain

- 📨 Add auxiliary services:

    - Amazon SES for email notifications

    - OpenSearch for advanced article search

    - ElastiCache (Redis) for asynchronous task queue with Celery

# 🧩 Features
## 📚 Articles
- Users can create, read, update, delete their own articles

- Articles can be rated (1–5 stars)

## 💬 Responses
- Nestable replies to articles or responses

- Users can edit/delete their own replies

##🔖 Bookmarks
- Users have a default Reading List

- Can create custom bookmark categories

- Bookmark articles into their categories

## ⭐ Ratings
- Rate any article on a 1–5 scale

## 🙍‍♂️ Profiles
- Auto-created at signup

- Editable name, bio, and other details

## 👥 Followers
- Follow/unfollow other users

- View followers and followees

## 📨 Notifications (via Celery + SES)
- Get notified when someone follows you

#⚙️ Tech Stack
- Backend:	Django, DRF, PostgreSQL
- Queue:	Celery + Redis (ElastiCache)
- Infra:	Terraform, ECS Fargate, RDS, ALB, ECR, Route53
- CI/CD:	GitHub Actions
- Security:	HTTPS, VPC isolation, IAM roles
- Extra:	OpenSearch (search), Amazon SES (email), Docker Compose (local dev)
- 
# 🛠️ How to user(Local Development)
git clone https://github.com/wrbyepct/medium-prod.git
cd medium-prod

# Install package
poetry install

# Create environment file
cp .example.envs .envs  # fill in values in .django .postgres

# Start services
docker-compose up --build

# Run migrations
docker-compose exec web python -m core.manage migrate

