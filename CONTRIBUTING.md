# 🤝 Contributing to AI Video Studio

<div dir="rtl">

شكراً لاهتمامك بالمساهمة في AI Video Studio! نحن نرحب بجميع أنواع المساهمات.

## 🌟 كيفية المساهمة

### 1. الإبلاغ عن الأخطاء (Bug Reports)

إذا وجدت خطأ:
- تحقق من أن الخطأ غير مُبلغ عنه في [Issues](https://github.com/omarabdhkem/ai-video-studio/issues)
- افتح Issue جديد مع:
  - عنوان واضح وصفي
  - خطوات إعادة إنتاج المشكلة
  - السلوك المتوقع والفعلي
  - لقطات شاشة إن أمكن
  - معلومات البيئة (نظام التشغيل، إصدار Docker، إلخ)

### 2. اقتراح ميزات جديدة

لديك فكرة رائعة؟
- افتح Issue بعنوان يبدأ بـ `[Feature Request]`
- اشرح الميزة المقترحة بالتفصيل
- وضح حالات الاستخدام
- أضف أمثلة أو mockups إن أمكن

### 3. تقديم تحسينات على الكود

#### خطوات المساهمة بالكود:

1. **Fork المشروع**
   ```bash
   # انقر على زر Fork في GitHub
   ```

2. **استنسخ Fork الخاص بك**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-video-studio.git
   cd ai-video-studio
   ```

3. **أنشئ فرع جديد**
   ```bash
   git checkout -b feature/amazing-feature
   # أو
   git checkout -b fix/bug-description
   ```

4. **قم بالتغييرات**
   - اتبع نمط الكود الموجود
   - أضف تعليقات واضحة
   - تأكد من أن الكود يعمل

5. **اختبر التغييرات**
   ```bash
   # للـ Backend
   cd backend
   python -m pytest  # إذا كانت هناك اختبارات
   
   # للـ Frontend
   cd frontend
   npm run lint
   npm run build
   ```

6. **Commit التغييرات**
   ```bash
   git add .
   git commit -m "Add: وصف واضح للتغيير"
   ```
   
   استخدم prefixes واضحة:
   - `Add:` لإضافة ميزات جديدة
   - `Fix:` لإصلاح الأخطاء
   - `Update:` لتحديث موجود
   - `Remove:` لحذف شيء
   - `Docs:` لتغييرات في التوثيق

7. **Push إلى Fork الخاص بك**
   ```bash
   git push origin feature/amazing-feature
   ```

8. **افتح Pull Request**
   - اذهب إلى صفحة المشروع الأصلي
   - انقر على "New Pull Request"
   - اختر فرعك
   - اكتب وصفاً تفصيلياً للتغييرات

## 📝 معايير الكود

### Python (Backend)
- استخدم PEP 8 style guide
- أضف type hints
- اكتب docstrings للدوال
- استخدم async/await للعمليات غير المتزامنة

```python
async def example_function(param: str) -> dict:
    """
    وصف واضح للدالة
    
    Args:
        param: وصف المعامل
        
    Returns:
        وصف القيمة المُرجعة
    """
    return {"result": param}
```

### TypeScript/React (Frontend)
- استخدم TypeScript بشكل صارم
- استخدم functional components
- أضف types لجميع Props
- استخدم Tailwind CSS للتصميم

```typescript
interface ComponentProps {
  title: string;
  onAction: () => void;
}

export default function Component({ title, onAction }: ComponentProps) {
  return (
    <div className="p-4">
      <h1>{title}</h1>
    </div>
  );
}
```

## 🧪 الاختبارات

- أضف اختبارات لأي كود جديد
- تأكد من أن جميع الاختبارات تمر
- اختبر في بيئات مختلفة إن أمكن

## 📚 التوثيق

- حدّث README.md إذا لزم الأمر
- أضف تعليقات في الكود للأجزاء المعقدة
- وثّق أي API endpoints جديدة

## 🔍 مراجعة الكود

- كن مهذباً ومحترماً في التعليقات
- اشرح سبب التغييرات المقترحة
- كن منفتحاً للنقاش والتعديلات

## 🎯 أولويات المساهمة

نرحب بشكل خاص بالمساهمات في:

1. **تحسين الأداء**
   - تحسين سرعة توليد الفيديو
   - تقليل استهلاك الذاكرة
   - تحسين جودة الفيديو

2. **إضافة ميزات**
   - دعم لغات إضافية
   - قوالب فيديو جاهزة
   - تأثيرات بصرية متقدمة
   - integration مع منصات أخرى

3. **تحسين الواجهة**
   - تصميم أفضل للموبايل
   - إضافة dark/light mode
   - تحسين تجربة المستخدم

4. **التوثيق**
   - شروحات فيديو
   - أمثلة إضافية
   - ترجمة للغات أخرى

## 💬 تواصل معنا

- افتح Issue للنقاش قبل البدء بميزة كبيرة
- انضم إلى Discussions للأسئلة العامة
- تابع التحديثات على Twitter/X

## 📜 Code of Conduct

- كن محترماً ومهذباً
- لا تمييز أو تحرش
- ساعد الآخرين
- شارك المعرفة

## 🎉 شكراً لك!

كل مساهمة، مهما كانت صغيرة، تساعد في تحسين المشروع. نحن نقدر وقتك وجهدك! 

</div>
