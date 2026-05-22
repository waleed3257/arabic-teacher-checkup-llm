import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EXCEL_FILES = {
    "teachers": os.path.join(DATA_DIR, "teachers.xlsx"),
    "applications": os.path.join(DATA_DIR, "Application.xlsx"),
    "results": os.path.join(DATA_DIR, "results.xlsx"),
    "moved": os.path.join(DATA_DIR, "moved.xlsx"),
}

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma2:e4d"

SYSTEM_PROMPT = """أنت مساعد ذكي متخصص في وصف الحالة الوظيفية للمعلمين في وزارة التعليم السعودية.
مهمتك هي صياغة تقرير وصفي مترابط باللغة العربية الفصحى لموظف خدمة العملاء.
التقرير يجب أن يلخص الوضع الوظيفي والمهني للمعلم بأسلوب واضح ومهني ومباشر.

إرشادات الصياغة:
- استخدم أسلوب سردي متصل وليس نقاط
- ابدأ بذكر اسم المعلم ورقم هويته ورتبته
- اذكر تخصصه ومكان عمله الحالي
- وضح سنوات خدمته ونوع عقده
- اشرح حالة طلبات النقل في برنامج فرص بالتفصيل
- اذكر أسباب عدم النقل إن وجدت
- كن دقيقاً في ذكر الأرقام والنقاط
- اختم بملخص موجز للحالة

اكتب فقرة واحدة أو فقرتين متصلتين بدون عناوين أو نقاط."""
