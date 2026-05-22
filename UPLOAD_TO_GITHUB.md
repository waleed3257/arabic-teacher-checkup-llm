# 📤 رفع المشروع إلى GitHub | Upload to GitHub

## الخطوات المطلوبة

### 1️⃣ إنشاء Repository على GitHub

1. اذهب إلى: https://github.com/new
2. املأ المعلومات التالية:

```
Repository name: arabic-teacher-checkup-llm
Description: Arabic Teacher Checkup Narrative Generator using Ollama LLM - نظام توليد التقارير الوصفية للمعلمين
Public/Private: اختر حسب رغبتك
✅ لا تفعل "Initialize this repository with a README"
```

3. اضغط "Create repository"

---

### 2️⃣ ربط المشروع المحلي بـ GitHub

بعد إنشاء الـ repository، نفذ الأوامر التالية:

```bash
cd /Users/waleedalhojaili/Dev/Leqa

# ربط الـ repository
git remote add origin https://github.com/waleed3257/arabic-teacher-checkup-llm.git

# تغيير اسم الفرع إلى main (اختياري)
git branch -M main

# رفع الكود
git push -u origin main
```

---

### 3️⃣ إذا طلب منك تسجيل الدخول

قد يطلب منك GitHub تسجيل الدخول. استخدم أحد الطرق:

#### الطريقة 1: Personal Access Token (موصى بها)
1. اذهب إلى: https://github.com/settings/tokens
2. اضغط "Generate new token" → "Generate new token (classic)"
3. اختر الصلاحيات: `repo` (كامل)
4. انسخ الـ token
5. عند الرفع، استخدم الـ token بدلاً من كلمة المرور

#### الطريقة 2: GitHub CLI
```bash
# تثبيت GitHub CLI (إذا لم يكن مثبتاً)
brew install gh

# تسجيل الدخول
gh auth login

# رفع الكود
git push -u origin main
```

---

### 4️⃣ التحقق من الرفع

بعد الرفع بنجاح، اذهب إلى:
```
https://github.com/waleed3257/arabic-teacher-checkup-llm
```

يجب أن ترى جميع الملفات والوثائق.

---

## ✅ الملفات التي سيتم رفعها

```
✅ main.py
✅ config.py
✅ requirements.txt
✅ test_system.py
✅ example_usage.py
✅ models/
✅ services/
✅ README.md
✅ QUICKSTART.md
✅ GETTING_STARTED.md
✅ ARCHITECTURE.md
✅ PROJECT_SUMMARY.md
✅ CHECKLIST.md
✅ .gitignore
✅ data/ (ملفات Excel - حجمها كبير)
```

---

## ⚠️ ملاحظة مهمة عن ملفات Excel

ملفات Excel في مجلد `data/` كبيرة الحجم (~60 MB). إذا واجهت مشكلة:

### الخيار 1: رفعها كما هي
```bash
git push -u origin main
```

### الخيار 2: استبعادها من Git
إذا كانت كبيرة جداً، أضف إلى `.gitignore`:
```bash
echo "data/*.xlsx" >> .gitignore
git rm --cached data/*.xlsx
git commit -m "Remove large Excel files from git"
git push -u origin main
```

ثم ارفع ملفات Excel بطريقة أخرى (Google Drive, OneDrive, etc.)

---

## 🔄 تحديثات مستقبلية

بعد أي تعديلات على الكود:

```bash
git add .
git commit -m "وصف التعديلات"
git push
```

---

## 📞 المساعدة

إذا واجهت مشاكل:
- تأكد من تسجيل الدخول إلى GitHub
- تحقق من اسم المستخدم: `waleed3257`
- استخدم Personal Access Token للمصادقة

---

**الكود جاهز للرفع! 🚀**
