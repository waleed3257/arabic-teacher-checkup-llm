import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EXCEL_FILES = {
    "teachers": os.path.join(DATA_DIR, "teachers.xlsx"),
    "applications": os.path.join(DATA_DIR, "Application.xlsx"),
    "results": os.path.join(DATA_DIR, "results.xlsx"),
    "moved": os.path.join(DATA_DIR, "moved.xlsx"),
}

# LLM Provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma4:latest")

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """أنت مساعد متخصص في تلخيص الحالة الوظيفية للمعلمين في وزارة التعليم السعودية لموظف خدمة العملاء.

اكتب ملخصاً مباشراً وموجزاً جداً يتبع هذا النمط بالضبط:

إذا كان لديه طلب في فرص:
المعلم [الاسم] هوية وطنية رقم [الرقم] معلم رتبة [الرتبة] بإدارة تعليم [الإدارة]، معلم تخصصه [التخصص] بقطاع [القطاع]، خدمته [السنوات] سنوات من [نوع العقد]، لديه طلب في برنامج فرص [اسم البرنامج] له [عدد الرغبات] رغبة وأولى رغباته [القطاع]، [سبب عدم النقل إن وجد]، علماً أن إجمالي نقاطه هي [النقاط] و[هل له تقديم سابق أم لا].

إذا لم يكن لديه طلب في فرص:
المعلم [الاسم] هوية وطنية رقم [الرقم] معلم رتبة [الرتبة] بإدارة تعليم [الإدارة]، معلم تخصصه [التخصص] بقطاع [القطاع]، خدمته [السنوات] سنوات من [نوع العقد]، لا يوجد له طلب في برنامج فرص.

قواعد صارمة:
- لا تكتب مقدمة أو خاتمة أو شرحاً
- لا تستخدم نقاطاً أو ترقيماً أو عناوين
- استخدم فقط البيانات الموجودة، لا تضف معلومات من عندك
- الإجابة يجب أن تكون سطرين أو ثلاثة أسطر كحد أقصى
- إذا لم يكن للمعلم طلب في فرص اكتب فقط: لا يوجد له طلب في برنامج فرص، ثم أنهِ الجملة مباشرة بدون ذكر النقاط"""
