# 🚀 Deployment Guide

<div dir="rtl">

دليل شامل لنشر AI Video Studio على بيئات مختلفة.

---

## 📋 جدول المحتويات

1. [النشر المحلي (Local)](#النشر-المحلي)
2. [النشر على VPS](#النشر-على-vps)
3. [النشر على AWS](#النشر-على-aws)
4. [النشر على Google Cloud](#النشر-على-google-cloud)
5. [استكشاف المشاكل](#استكشاف-المشاكل)

---

## النشر المحلي

### المتطلبات
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM على الأقل
- 10GB مساحة قرص

### الخطوات

```bash
# 1. استنساخ المشروع
git clone https://github.com/omarabdhkem/ai-video-studio.git
cd ai-video-studio

# 2. إعداد ملف البيئة
./setup.sh

# 3. تشغيل التطبيق
docker-compose up -d

# 4. التحقق من الحالة
docker-compose ps
```

---

## النشر على VPS

### المتطلبات
- Ubuntu 20.04+ أو Debian 11+
- 4GB RAM minimum (8GB مفضل)
- 20GB disk space
- Domain name (اختياري)

### 1. إعداد الخادم

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# تثبيت Docker Compose
sudo apt install docker-compose -y

# إضافة المستخدم لمجموعة Docker
sudo usermod -aG docker $USER
newgrp docker
```

### 2. نقل المشروع

```bash
# على جهازك المحلي
scp -r ai-video-studio user@your-server-ip:/home/user/

# أو باستخدام Git
ssh user@your-server-ip
git clone https://github.com/omarabdhkem/ai-video-studio.git
cd ai-video-studio
```

### 3. إعداد البيئة

```bash
# إنشاء ملف .env
cp .env.example .env
nano .env  # أضف GROQ_API_KEY

# إنشاء ملف backend/.env
cp backend/.env.example backend/.env
nano backend/.env  # أضف GROQ_API_KEY
```

### 4. تشغيل التطبيق

```bash
docker-compose up -d
```

### 5. إعداد Nginx (اختياري للإنتاج)

```bash
# تثبيت Nginx
sudo apt install nginx -y

# إنشاء ملف التكوين
sudo nano /etc/nginx/sites-available/aivideo
```

أضف التكوين التالي:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }

    # Static videos
    location /api/v1/videos/ {
        proxy_pass http://localhost:8000;
        proxy_buffering off;
    }
}
```

```bash
# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/aivideo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. إعداد SSL (اختياري - موصى به)

```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com
```

---

## النشر على AWS

### باستخدام EC2

#### 1. إنشاء EC2 Instance

```bash
# اختر AMI: Ubuntu 20.04 LTS
# Instance Type: t2.medium أو أفضل
# Storage: 20GB GP2
# Security Group: افتح المنافذ 22, 80, 443, 3000, 8000
```

#### 2. الاتصال بالخادم

```bash
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com
```

#### 3. اتبع خطوات VPS أعلاه

### باستخدام ECS (Docker)

```yaml
# task-definition.json
{
  "family": "ai-video-studio",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-ecr-repo/backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "GROQ_API_KEY",
          "value": "your-key-here"
        }
      ]
    },
    {
      "name": "frontend",
      "image": "your-ecr-repo/frontend:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

---

## النشر على Google Cloud

### باستخدام Compute Engine

مشابه لـ AWS EC2 - اتبع خطوات VPS.

### باستخدام Cloud Run

```bash
# بناء الصور
docker build -t gcr.io/PROJECT_ID/backend ./backend
docker build -t gcr.io/PROJECT_ID/frontend ./frontend

# رفع الصور
docker push gcr.io/PROJECT_ID/backend
docker push gcr.io/PROJECT_ID/frontend

# نشر على Cloud Run
gcloud run deploy backend \
  --image gcr.io/PROJECT_ID/backend \
  --platform managed \
  --set-env-vars GROQ_API_KEY=xxx

gcloud run deploy frontend \
  --image gcr.io/PROJECT_ID/frontend \
  --platform managed
```

---

## استكشاف المشاكل

### المشكلة: الحاويات لا تبدأ

```bash
# عرض السجلات
docker-compose logs

# إعادة بناء الصور
docker-compose build --no-cache
docker-compose up -d
```

### المشكلة: خطأ في الاتصال بـ Database

```bash
# التحقق من حالة PostgreSQL
docker-compose ps db

# عرض سجلات Database
docker-compose logs db

# إعادة تشغيل Database
docker-compose restart db
```

### المشكلة: نفاد المساحة

```bash
# تنظيف صور Docker غير المستخدمة
docker system prune -a

# تنظيف volumes
docker volume prune
```

### المشكلة: بطء في التوليد

```bash
# زيادة موارد Docker
# في Docker Desktop: Settings → Resources

# أو زيادة موارد VPS
# Upgrade instance type
```

---

## أفضل الممارسات للإنتاج

### 1. الأمان
- ✅ استخدم HTTPS (SSL/TLS)
- ✅ احفظ API keys في متغيرات البيئة
- ✅ استخدم firewall
- ✅ حدّث النظام بانتظام
- ✅ استخدم strong passwords

### 2. النسخ الاحتياطي
```bash
# نسخ احتياطي للـ Database
docker exec aivideo-db pg_dump -U postgres aivideostudio > backup.sql

# نسخ احتياطي للفيديوهات
tar -czf videos-backup.tar.gz backend/output/
```

### 3. المراقبة
```bash
# مراقبة استهلاك الموارد
docker stats

# مراقبة السجلات
docker-compose logs -f --tail=100
```

### 4. التحديثات
```bash
# سحب آخر التحديثات
git pull origin main

# إعادة بناء ونشر
docker-compose down
docker-compose build
docker-compose up -d
```

---

## الخلاصة

اختر طريقة النشر المناسبة لاحتياجاتك:

| الطريقة | الأفضل لـ | التكلفة | الصعوبة |
|---------|----------|---------|---------|
| Local | التطوير والاختبار | مجاني | سهل |
| VPS | الإنتاج الصغير | $5-20/شهر | متوسط |
| AWS EC2 | الإنتاج المتوسط | $20-100/شهر | متوسط |
| Cloud Run | الإنتاج المرن | حسب الاستخدام | متقدم |

---

للمساعدة، افتح [Issue](https://github.com/omarabdhkem/ai-video-studio/issues) على GitHub.

</div>
