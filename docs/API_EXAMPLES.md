# 📖 API Examples

<div dir="rtl">

هذا الملف يحتوي على أمثلة عملية لاستخدام API الخاص بـ AI Video Studio.

## 🚀 البدء

تأكد من تشغيل الخادم أولاً:

```bash
docker-compose up -d
```

جميع الأمثلة تستخدم `http://localhost:8000` كعنوان API.

---

## 📋 الأمثلة

### 1. فحص صحة النظام (Health Check)

**الطلب:**
```bash
curl http://localhost:8000/api/v1/health
```

**الاستجابة:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "groq": "available",
    "edge_tts": "available",
    "moviepy": "available"
  }
}
```

---

### 2. إنشاء مشروع فيديو جديد

**الطلب:**
```bash
curl -X POST http://localhost:8000/api/v1/projects/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "مقدمة في الذكاء الاصطناعي",
    "topic": "شرح مبسط لمفهوم الذكاء الاصطناعي وتطبيقاته في الحياة اليومية",
    "language": "ar",
    "voice_gender": "male",
    "duration_minutes": 3,
    "style": "educational"
  }'
```

---

## 🐍 استخدام Python

```python
import requests
import time

API_URL = "http://localhost:8000/api/v1"

# إنشاء مشروع جديد
def create_project():
    response = requests.post(
        f"{API_URL}/projects/create",
        json={
            "title": "درس برمجة Python",
            "topic": "تعلم أساسيات البرمجة بلغة Python للمبتدئين",
            "language": "ar",
            "voice_gender": "male",
            "duration_minutes": 5,
            "style": "educational"
        }
    )
    return response.json()

# متابعة حالة المشروع
def check_project_status(project_id):
    response = requests.get(f"{API_URL}/projects/{project_id}")
    return response.json()

# تنفيذ
project = create_project()
print(f"Project created: {project['id']}")

# انتظار الإكمال
while True:
    status = check_project_status(project['id'])
    print(f"Progress: {status['progress']}% - Status: {status['status']}")
    
    if status['status'] == 'completed':
        print(f"Video ready: {status['video_url']}")
        break
    elif status['status'] == 'failed':
        print(f"Error: {status['error_message']}")
        break
    
    time.sleep(5)
```

---

## 🌐 استخدام JavaScript/Node.js

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:8000/api/v1';

// إنشاء مشروع جديد
async function createProject() {
  const response = await axios.post(`${API_URL}/projects/create`, {
    title: 'مراجعة كتاب',
    topic: 'مراجعة شاملة لكتاب الأب الغني والأب الفقير',
    language: 'ar',
    voice_gender: 'female',
    duration_minutes: 4,
    style: 'informative'
  });
  
  return response.data;
}

// تنفيذ
(async () => {
  try {
    const project = await createProject();
    console.log(`Project created: ${project.id}`);
  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

---

## 🔍 استكشاف الأخطاء

### خطأ 500: Internal Server Error

**السبب المحتمل:** لم يتم تكوين `GROQ_API_KEY`

**الحل:**
```bash
# تحقق من ملف .env
cat backend/.env | grep GROQ_API_KEY

# إذا كان فارغاً، أضف المفتاح:
echo "GROQ_API_KEY=your_actual_key_here" >> backend/.env

# أعد تشغيل الخدمات
docker-compose restart backend
```

---

للمزيد من الأمثلة، راجع [Swagger UI](http://localhost:8000/docs)

</div>
