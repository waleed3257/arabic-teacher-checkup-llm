# دليل الإعداد | Setup Guide

## ⚙️ معالج إعداد مزود LLM

يوفر البرنامج معالج إعداد تفاعلي لاختيار وتكوين مزود LLM.

---

## 🚀 تشغيل المعالج

```bash
python3 setup_provider.py
```

---

## 📋 المزودات المدعومة

### 1️⃣ Ollama (Local / Self-hosted) ⭐ موصى به
- **مجاني** ويعمل محلياً
- **خصوصية كاملة** - البيانات لا تغادر جهازك
- **يدعم نماذج متعددة**: gemma, llama, deepseek, mistral, وغيرها
- **اكتشاف تلقائي**: يعرض النماذج المتاحة لديك

### 2️⃣ OpenAI
- يتطلب API Key
- نماذج: gpt-4o, gpt-4o-mini, gpt-3.5-turbo

### 3️⃣ OpenRouter
- يتطلب API Key
- يوفر الوصول لنماذج متعددة من مزودات مختلفة

### 4️⃣ Google AI (Gemini)
- يتطلب API Key
- نماذج: gemini-2.0-flash, gemini-1.5-pro

### 5️⃣ Anthropic (Claude)
- يتطلب API Key
- نماذج: claude-3-5-haiku, claude-3-5-sonnet

---

## 🎯 الميزة الجديدة: اكتشاف النماذج المتاحة

### لـ Ollama فقط:
عند اختيار Ollama، المعالج سيقوم بـ:

1. **الاتصال بـ Ollama API** تلقائياً
2. **جلب قائمة النماذج المتاحة** على جهازك
3. **عرضها مرقمة** للاختيار السهل
4. **تمييز النموذج الافتراضي** بـ ⭐

### مثال:

```
🤖 اختر النموذج / Choose Model:
   🔍 جارٍ البحث عن النماذج المتاحة في Ollama...

   ✅ النماذج المتاحة / Available Models (3):
      1) gemma4:e4b ⭐
      2) minimax-m2:cloud
      3) gpt-oss:20b-cloud

اختر رقم النموذج أو اكتب اسمه (Enter للافتراضي: gemma4:latest): 
```

### خيارات الاختيار:

#### الخيار 1: اختيار بالرقم
```
اختر رقم النموذج: 2
✅ سيتم اختيار: minimax-m2:cloud
```

#### الخيار 2: كتابة الاسم
```
اختر رقم النموذج: llama3.1:8b
✅ سيتم اختيار: llama3.1:8b
```

#### الخيار 3: الافتراضي
```
اختر رقم النموذج: [Enter]
✅ سيتم اختيار: gemma4:latest
```

---

## 📝 مثال كامل على الاستخدام

```bash
$ python3 setup_provider.py

============================================================
⚙️  معالج إعداد مزود LLM  |  LLM Provider Setup Wizard
============================================================

📋 الإعداد الحالي / Current Configuration:
   Provider : ollama
   Model    : gemma4:e4b

🔌 اختر المزود / Choose Provider:

   1) Ollama (Local / Self-hosted)
   2) OpenAI
   3) OpenRouter
   4) Google AI (Gemini)
   5) Anthropic (Claude)

اختر رقم المزود (1-5): 1

🤖 اختر النموذج / Choose Model:
   🔍 جارٍ البحث عن النماذج المتاحة في Ollama...

   ✅ النماذج المتاحة / Available Models (3):
      1) gemma4:e4b ⭐
      2) minimax-m2:cloud
      3) gpt-oss:20b-cloud

اختر رقم النموذج أو اكتب اسمه (Enter للافتراضي: gemma4:latest): 1

🌐 Ollama Base URL (الحالي: http://localhost:11434):
   أدخل URL أو Enter للإبقاء على الحالي: [Enter]

------------------------------------------------------------
📝 ملخص الإعداد / Configuration Summary:
   Provider : Ollama (Local / Self-hosted)
   Model    : gemma4:e4b
------------------------------------------------------------

حفظ الإعدادات؟ Save? (Y/n): y

✅ تم حفظ الإعدادات في .env بنجاح!
   LLM_PROVIDER = ollama
   LLM_MODEL    = gemma4:e4b
```

---

## 🔧 إعدادات متقدمة

### تغيير Ollama URL
إذا كان Ollama يعمل على منفذ مختلف أو جهاز آخر:

```
🌐 Ollama Base URL (الحالي: http://localhost:11434):
   أدخل URL: http://192.168.1.100:11434
```

### استخدام نموذج غير موجود في القائمة
يمكنك كتابة اسم أي نموذج حتى لو لم يكن في القائمة:

```
اختر رقم النموذج: deepseek-r1:14b
```

---

## ⚠️ استكشاف الأخطاء

### لم يتم العثور على نماذج متاحة

```
   ⚠️  لم يتم العثور على نماذج متاحة. تأكد من تشغيل Ollama.
   💡 يمكنك تحميل نموذج بـ: ollama pull <model-name>
```

**الحل:**
```bash
# تأكد من تشغيل Ollama
ollama serve

# في نافذة أخرى، حمل نموذج
ollama pull gemma4:latest
ollama pull llama3.1:8b
ollama pull deepseek-r1:8b

# ثم أعد تشغيل المعالج
python3 setup_provider.py
```

### Ollama لا يستجيب

**الحل:**
1. تأكد من تشغيل Ollama: `ollama serve`
2. تحقق من المنفذ: `http://localhost:11434`
3. جرب الوصول يدوياً: `curl http://localhost:11434/api/tags`

---

## 📁 ملف .env

بعد الإعداد، سيتم إنشاء/تحديث ملف `.env` في جذر المشروع:

```env
LLM_PROVIDER=ollama
LLM_MODEL=gemma4:e4b
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 🔄 إعادة التكوين

لتغيير الإعدادات في أي وقت:

```bash
python3 setup_provider.py
```

المعالج سيعرض الإعدادات الحالية ويسمح لك بتغييرها.

---

## 💡 نصائح

### للأداء الأفضل مع Ollama:
1. استخدم نماذج صغيرة للسرعة (8b أو أقل)
2. استخدم نماذج كبيرة للجودة (70b+)
3. جرب نماذج مختلفة لإيجاد الأنسب

### نماذج موصى بها للعربية:
- `gemma4:latest` - ممتاز للعربية
- `llama3.1:8b` - سريع ودقيق
- `deepseek-r1:8b` - جيد للتفكير المنطقي

---

## 🆘 الدعم

إذا واجهت مشاكل:
1. تأكد من تشغيل Ollama: `ollama serve`
2. تحقق من النماذج المتاحة: `ollama list`
3. راجع ملف `.env` للتأكد من الإعدادات
4. جرب نموذج آخر

---

**استمتع بالإعداد السهل! ⚙️**
