import requests
import json
from config import OLLAMA_URL, OLLAMA_MODEL, SYSTEM_PROMPT


def generate_report(prompt: str, timeout: int = 120) -> str:
    """
    توليد التقرير الوصفي باستخدام Ollama LLM
    
    Args:
        prompt: النص التوجيهي الذي يحتوي على بيانات المعلم
        timeout: مهلة الانتظار بالثواني (افتراضي: 120)
        
    Returns:
        التقرير الوصفي المولد باللغة العربية
    """
    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
        }
    }
    
    try:
        print(f"🤖 جارٍ الاتصال بـ Ollama (النموذج: {OLLAMA_MODEL})...")
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        if not generated_text:
            return "❌ لم يتم توليد نص من النموذج اللغوي. حاول مرة أخرى."
        
        return generated_text
        
    except requests.exceptions.ConnectionError:
        return """❌ تعذّر الاتصال بخادم Ollama
        
تأكد من:
1. تشغيل Ollama: ollama serve
2. تحميل النموذج: ollama pull gemma2:e4d
3. أن الخادم يعمل على: http://localhost:11434"""
        
    except requests.exceptions.Timeout:
        return f"""❌ انتهت مهلة الانتظار ({timeout} ثانية)
        
حاول:
1. زيادة مهلة الانتظار
2. استخدام نموذج أصغر وأسرع
3. التحقق من موارد النظام"""
        
    except requests.exceptions.HTTPError as e:
        return f"""❌ خطأ HTTP من خادم Ollama: {e}
        
تحقق من:
1. أن النموذج {OLLAMA_MODEL} محمل: ollama list
2. صحة اسم النموذج في config.py"""
        
    except json.JSONDecodeError:
        return "❌ خطأ في تحليل استجابة JSON من Ollama"
        
    except Exception as e:
        return f"❌ خطأ غير متوقع: {type(e).__name__}: {str(e)}"
