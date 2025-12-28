# 🎬 AI Video Studio - استوديو الفيديو الذكي

<div dir="rtl">

## 📖 نظرة عامة

**AI Video Studio** هي منصة مجانية متكاملة بنسبة 100% لأتمتة إنتاج فيديوهات اليوتيوب باستخدام الذكاء الاصطناعي. تجمع المنصة بين أفضل التقنيات المجانية لتوفير حل شامل لإنشاء محتوى فيديو احترافي.

### ✨ المميزات الرئيسية

- 🆓 **100% مجاني** - بدون تكاليف خفية
- 🤖 **بدون OpenAI** - يستخدم Groq API المجاني
- 🗣️ **أصوات طبيعية** - Edge-TTS بجودة عالية
- 🎥 **تجميع تلقائي** - MoviePy + FFmpeg
- 🌍 **دعم متعدد اللغات** - عربي وإنجليزي
- 🐳 **Docker Ready** - تشغيل سريع بأمر واحد
- 🎨 **واجهة جميلة** - Next.js + Tailwind CSS

---

## 🏗️ البنية التقنية

### Backend (Python FastAPI)

```
backend/
├── main.py                 # تطبيق FastAPI الرئيسي
├── requirements.txt        # المكتبات المطلوبة
├── Dockerfile             # ملف Docker
├── .env.example           # مثال على ملف البيئة
├── agents/                # الوكلاء الذكيون
│   ├── script_agent.py   # توليد السكريبت (Groq)
│   ├── voice_agent.py    # توليد الصوت (Edge-TTS)
│   └── video_agent.py    # تجميع الفيديو (MoviePy)
├── api/                   # API Routes
│   ├── routes.py         # المسارات
│   └── models.py         # نماذج البيانات
├── config/               # الإعدادات
│   └── settings.py       # إعدادات التطبيق
└── services/             # الخدمات
    ├── groq_service.py   # خدمة Groq API
    └── tts_service.py    # خدمة Text-to-Speech
```

### Frontend (Next.js + TypeScript)

```
frontend/
├── app/
│   ├── layout.tsx        # التخطيط الرئيسي
│   ├── page.tsx          # الصفحة الرئيسية
│   └── globals.css       # الأنماط العامة
├── components/           # المكونات القابلة لإعادة الاستخدام
├── package.json         # اعتماديات Node.js
├── next.config.js       # إعدادات Next.js
├── tailwind.config.js   # إعدادات Tailwind
└── tsconfig.json        # إعدادات TypeScript
```

---

## 🚀 البدء السريع

### المتطلبات الأساسية

- Docker و Docker Compose
- حساب Groq API (مجاني من [groq.com](https://groq.com))

### خطوات التثبيت

#### 1. استنساخ المشروع

```bash
git clone https://github.com/omarabdhkem/ai-video-studio.git
cd ai-video-studio
```

#### 2. إعداد ملف البيئة

```bash
# في مجلد backend
cd backend
cp .env.example .env
# قم بتحرير .env وأضف GROQ_API_KEY الخاص بك
```

#### 3. تشغيل المشروع باستخدام Docker

```bash
# العودة إلى المجلد الرئيسي
cd ..

# تشغيل جميع الخدمات
docker-compose up -d
```

#### 4. الوصول إلى التطبيق

- **الواجهة الأمامية**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000

---

## 📚 دليل الاستخدام

### إنشاء فيديو جديد

1. افتح الواجهة على http://localhost:3000
2. املأ النموذج:
   - **عنوان الفيديو**: اختر عنواناً جذاباً
   - **موضوع الفيديو**: اكتب وصفاً تفصيلياً للموضوع
   - **اللغة**: اختر العربية أو الإنجليزية
   - **جنس الصوت**: ذكر أو أنثى
   - **المدة**: من 1 إلى 10 دقائق
   - **الأسلوب**: معلوماتي، تعليمي، ترفيهي، أو تحفيزي
3. اضغط على "إنشاء الفيديو"
4. انتظر حتى يكتمل التوليد
5. حمّل الفيديو الجاهز

### مراحل الإنتاج

1. **توليد السكريبت** (10-30 ثانية)
   - يستخدم Groq API لتوليد نص منظم بمشاهد
   
2. **توليد الصوت** (30-60 ثانية)
   - يحول النص إلى صوت طبيعي باستخدام Edge-TTS
   
3. **تجميع الفيديو** (60-120 ثانية)
   - يدمج الصوت مع الخلفيات والنصوص

---

## 🔧 API Endpoints

### Health Check
```http
GET /api/v1/health
```

### إنشاء مشروع
```http
POST /api/v1/projects/create
Content-Type: application/json

{
  "title": "عنوان الفيديو",
  "topic": "وصف الموضوع",
  "language": "ar",
  "voice_gender": "male",
  "duration_minutes": 3,
  "style": "informative"
}
```

### توليد سكريبت
```http
POST /api/v1/generate/script
Content-Type: application/json

{
  "topic": "الذكاء الاصطناعي",
  "language": "ar",
  "duration_minutes": 3
}
```

### توليد صوت
```http
POST /api/v1/generate/voice
Content-Type: application/json

{
  "text": "النص المراد تحويله لصوت",
  "language": "ar",
  "gender": "male"
}
```

### قائمة المشاريع
```http
GET /api/v1/projects?page=1&page_size=10
```

### تفاصيل مشروع
```http
GET /api/v1/projects/{project_id}
```

---

## 🛠️ المكتبات والتقنيات

### Backend
- **FastAPI** - إطار عمل API سريع وحديث
- **Groq API** - توليد النصوص بالذكاء الاصطناعي (مجاني)
- **Edge-TTS** - تحويل النص إلى صوت (مجاني 100%)
- **MoviePy** - معالجة وتجميع الفيديو
- **FFmpeg** - ترميز وتصدير الفيديو
- **PostgreSQL** - قاعدة البيانات
- **Redis** - التخزين المؤقت

### Frontend
- **Next.js 14** - إطار عمل React
- **TypeScript** - JavaScript مع أنواع ثابتة
- **Tailwind CSS** - تصميم سريع وجميل
- **Axios** - استدعاءات API
- **Lucide Icons** - أيقونات جميلة

---

## 🎯 الأصوات المتاحة

### اللغة العربية
- **ذكر**: `ar-SA-HamedNeural` (سعودي)
- **أنثى**: `ar-EG-SalmaNeural` (مصري)

### اللغة الإنجليزية
- **ذكر**: `en-US-GuyNeural`
- **أنثى**: `en-US-JennyNeural`

---

## 📝 التطوير المحلي

### تشغيل Backend فقط

```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تثبيت المكتبات
pip install -r requirements.txt

# تشغيل الخادم
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### تشغيل Frontend فقط

```bash
cd frontend

# تثبيت المكتبات
npm install

# تشغيل خادم التطوير
npm run dev
```

---

## 🐛 حل المشاكل الشائعة

### المشكلة: "GROQ_API_KEY is required"
**الحل**: تأكد من إضافة مفتاح Groq API في ملف `.env`

### المشكلة: خطأ في MoviePy
**الحل**: تأكد من تثبيت FFmpeg بشكل صحيح

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# MacOS
brew install ffmpeg

# Windows
# قم بتحميل FFmpeg من الموقع الرسمي
```

### المشكلة: فشل تشغيل Docker
**الحل**: تأكد من تشغيل Docker daemon

```bash
# التحقق من حالة Docker
docker info

# إعادة تشغيل Docker
sudo systemctl restart docker
```

---

## 🤝 المساهمة

نرحب بجميع المساهمات! إذا كنت ترغب في المساهمة:

1. Fork المشروع
2. أنشئ فرع للميزة (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى الفرع (`git push origin feature/amazing-feature`)
5. افتح Pull Request

---

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 🙏 شكر وتقدير

- **Groq** - للتوفير API مجاني وسريع
- **Microsoft Edge-TTS** - لخدمة TTS المجانية
- **MoviePy** - لمكتبة معالجة الفيديو الرائعة
- **FastAPI** - لإطار العمل الممتاز
- **Next.js** - لأفضل تجربة React

---

## 📧 التواصل

إذا كان لديك أي أسئلة أو اقتراحات، لا تتردد في فتح Issue أو التواصل معنا!

---

<div align="center">

**صُنع بـ ❤️ للمجتمع العربي**

⭐ إذا أعجبك المشروع، لا تنسَ إضافة نجمة!

</div>

</div>