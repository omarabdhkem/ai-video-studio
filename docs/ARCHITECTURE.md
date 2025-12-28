# 🏗️ Architecture Overview

<div dir="rtl">

## معمارية النظام

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
│                    ┌──────────────────────┐                      │
│                    │   React Components   │                      │
│                    │  - Dashboard Page    │                      │
│                    │  - Project List      │                      │
│                    │  - Create Form       │                      │
│                    └──────────┬───────────┘                      │
│                               │                                  │
│                               │ HTTP/REST API                    │
│                               │                                  │
└───────────────────────────────┼──────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    API Routes                          │    │
│  │  - POST /projects/create                               │    │
│  │  - GET  /projects                                      │    │
│  │  - POST /generate/script                               │    │
│  │  - POST /generate/voice                                │    │
│  └─────────────────┬──────────────────────────────────────┘    │
│                    │                                            │
│                    ▼                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Agents (Business Logic)                   │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │    │
│  │  │Script Agent  │  │ Voice Agent  │  │ Video Agent  │ │    │
│  │  │  (Groq API)  │  │  (Edge-TTS)  │  │  (MoviePy)   │ │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │    │
│  │         │                 │                 │          │    │
│  └─────────┼─────────────────┼─────────────────┼──────────┘    │
│            │                 │                 │                │
│            ▼                 ▼                 ▼                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    Services                            │    │
│  │  - Groq Service (AI Text Generation)                   │    │
│  │  - TTS Service (Text-to-Speech)                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────┬───────────────────────────────────┬──────────────┘
               │                                   │
               ▼                                   ▼
    ┌──────────────────┐                 ┌──────────────────┐
    │   PostgreSQL DB  │                 │      Redis       │
    │   (Projects)     │                 │   (Cache/Queue)  │
    └──────────────────┘                 └──────────────────┘
```

---

## تدفق البيانات (Data Flow)

### 1. إنشاء مشروع فيديو جديد

```
User → Frontend → Backend API → Background Task
                                      ↓
                              ┌───────────────┐
                              │ Script Agent  │
                              │   (Groq API)  │
                              └───────┬───────┘
                                      ↓
                              ┌───────────────┐
                              │ Voice Agent   │
                              │  (Edge-TTS)   │
                              └───────┬───────┘
                                      ↓
                              ┌───────────────┐
                              │ Video Agent   │
                              │   (MoviePy)   │
                              └───────┬───────┘
                                      ↓
                              ┌───────────────┐
                              │  Video File   │
                              │    (.mp4)     │
                              └───────────────┘
```

### 2. معالجة السكريبت

```
Topic Input → Groq API → AI Model
                            ↓
                    ┌───────────────┐
                    │ Script JSON   │
                    │  - Title      │
                    │  - Scenes[]   │
                    │  - Text       │
                    └───────────────┘
```

### 3. توليد الصوت

```
Text → Edge-TTS Service → Neural Voice
                              ↓
                    ┌──────────────────┐
                    │  Audio File      │
                    │  (.mp3)          │
                    │  + Duration      │
                    └──────────────────┘
```

### 4. تجميع الفيديو

```
Audio Files[] + Text[] → MoviePy
                            ↓
              ┌─────────────────────────┐
              │ Video Processing        │
              │ - Background            │
              │ - Subtitles             │
              │ - Audio Sync            │
              └──────────┬──────────────┘
                         ↓
              ┌─────────────────────────┐
              │ Final Video (.mp4)      │
              │ 1920x1080, 24fps        │
              └─────────────────────────┘
```

---

## المكونات الرئيسية

### Backend Components

#### 1. **API Layer** (`api/`)
- **routes.py**: يحدد جميع endpoints
- **models.py**: نماذج البيانات (Pydantic)

#### 2. **Agents** (`agents/`)
- **script_agent.py**: 
  - يستخدم Groq API لتوليد النصوص
  - يحول الموضوع إلى سكريبت منظم
  
- **voice_agent.py**:
  - يستخدم Edge-TTS لتوليد الصوت
  - يدعم أصوات متعددة (ذكر/أنثى، عربي/إنجليزي)
  
- **video_agent.py**:
  - يستخدم MoviePy لتجميع الفيديو
  - يضيف النصوص والخلفيات
  - يصدر MP4 جاهز للنشر

#### 3. **Services** (`services/`)
- **groq_service.py**: واجهة Groq API
- **tts_service.py**: واجهة Edge-TTS

#### 4. **Config** (`config/`)
- **settings.py**: إعدادات التطبيق

### Frontend Components

#### 1. **App Router** (`app/`)
- **layout.tsx**: التخطيط الأساسي
- **page.tsx**: الصفحة الرئيسية
- **globals.css**: الأنماط العامة

#### 2. **Features**
- نموذج إنشاء مشروع
- قائمة المشاريع
- شريط التقدم
- تحميل الفيديو

---

## التقنيات المستخدمة

### Backend Stack
```
FastAPI (Python 3.11)
├── Groq SDK (AI Text Generation)
├── Edge-TTS (Text-to-Speech)
├── MoviePy (Video Processing)
├── FFmpeg (Media Encoding)
├── Pydantic (Data Validation)
└── Uvicorn (ASGI Server)
```

### Frontend Stack
```
Next.js 14 (React 18)
├── TypeScript
├── Tailwind CSS
├── Axios (HTTP Client)
└── Lucide Icons
```

### Infrastructure
```
Docker Compose
├── Backend Container
├── Frontend Container
├── PostgreSQL Database
└── Redis Cache
```

---

## الأمان والأداء

### Security
- ✅ Environment variables للبيانات الحساسة
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ No secrets في الكود

### Performance
- ✅ Background tasks للمعالجة الطويلة
- ✅ Redis للتخزين المؤقت
- ✅ Async/await للعمليات I/O
- ✅ Docker للعزل والتوسع

### Scalability
- ✅ Stateless API design
- ✅ Database للبيانات الدائمة
- ✅ File storage منفصل
- ✅ يمكن توسيعه أفقياً

---

## خطوات التطوير المستقبلية

### المرحلة 1 (الحالية) ✅
- [x] MVP كامل
- [x] الوظائف الأساسية
- [x] Docker setup

### المرحلة 2 (قادمة)
- [ ] حفظ المشاريع في Database
- [ ] Authentication & Users
- [ ] قوالب فيديو جاهزة
- [ ] Background music

### المرحلة 3 (مستقبلية)
- [ ] Webhook notifications
- [ ] Upload للفيديو مباشرة لليوتيوب
- [ ] Analytics dashboard
- [ ] Multiple video formats

---

## ملاحظات معمارية

### لماذا FastAPI؟
- سرعة عالية
- دعم async/await
- توثيق تلقائي (Swagger)
- Type hints

### لماذا Next.js؟
- SSR & SSG support
- أداء ممتاز
- Developer experience رائعة
- TypeScript support

### لماذا Edge-TTS؟
- مجاني 100%
- أصوات طبيعية
- لا يحتاج API key
- دعم ممتاز للعربية

### لماذا Groq؟
- مجاني للاستخدام
- سرعة استجابة عالية
- نماذج AI قوية
- بديل ممتاز لـ OpenAI

---

</div>
