import requests
import json
import time
from config import (
    LLM_PROVIDER, LLM_MODEL, SYSTEM_PROMPT,
    OLLAMA_BASE_URL,
    OPENAI_API_KEY, OPENAI_BASE_URL,
    OPENROUTER_API_KEY,
    GOOGLE_API_KEY,
    ANTHROPIC_API_KEY,
)

PROVIDER_LABELS = {
    "ollama": "Ollama",
    "openai": "OpenAI",
    "openrouter": "OpenRouter",
    "google": "Google AI",
    "anthropic": "Anthropic",
}


def _call_ollama(prompt: str, timeout: int) -> str:
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"
    payload = {
        "model": LLM_MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
        "stream": False,
        "options": {"temperature": 0.7, "top_p": 0.9},
    }
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json().get("response", "").strip()


def _call_openai_compatible(prompt: str, timeout: int, api_key: str, base_url: str) -> str:
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }
    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(f"خطأ من المزود: {data['error']}")
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"استجابة غير متوقعة من المزود: {data}") from e


def _call_google(prompt: str, timeout: int) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent"
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7},
    }
    response = requests.post(url, json=payload, params={"key": GOOGLE_API_KEY}, timeout=timeout)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def _call_anthropic(prompt: str, timeout: int) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()["content"][0]["text"].strip()


def generate_report(prompt: str, timeout: int = 120, max_retries: int = 3) -> str:
    """
    توليد التقرير الوصفي باستخدام مزود LLM المحدد في .env
    """
    provider = LLM_PROVIDER.lower()
    label = PROVIDER_LABELS.get(provider, provider)
    print(f"🤖 جارٍ الاتصال بـ {label} (النموذج: {LLM_MODEL})...")

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            if provider == "ollama":
                text = _call_ollama(prompt, timeout)

            elif provider == "openai":
                if not OPENAI_API_KEY:
                    raise ValueError("❌ OPENAI_API_KEY غير محدد في ملف .env")
                text = _call_openai_compatible(prompt, timeout, OPENAI_API_KEY, OPENAI_BASE_URL)

            elif provider == "openrouter":
                if not OPENROUTER_API_KEY:
                    raise ValueError("❌ OPENROUTER_API_KEY غير محدد في ملف .env")
                text = _call_openai_compatible(
                    prompt, timeout, OPENROUTER_API_KEY, "https://openrouter.ai/api/v1"
                )

            elif provider == "google":
                if not GOOGLE_API_KEY:
                    raise ValueError("❌ GOOGLE_API_KEY غير محدد في ملف .env")
                text = _call_google(prompt, timeout)

            elif provider == "anthropic":
                if not ANTHROPIC_API_KEY:
                    raise ValueError("❌ ANTHROPIC_API_KEY غير محدد في ملف .env")
                text = _call_anthropic(prompt, timeout)

            else:
                raise ValueError(
                    f"❌ مزود LLM غير معروف: '{provider}'\n"
                    f"الخيارات المتاحة: ollama | openai | openrouter | google | anthropic"
                )

            if not text:
                raise ValueError("❌ لم يتم توليد نص من النموذج اللغوي. حاول مرة أخرى.")

            return text

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                wait = 2 ** attempt
                print(f"   ⏳ تجاوز حد الطلبات (429). إعادة المحاولة بعد {wait} ثانية... ({attempt}/{max_retries})")
                time.sleep(wait)
                last_error = e
                continue
            raise RuntimeError(
                f"❌ خطأ HTTP من {label}: {e}\n\n"
                f"تحقق من:\n"
                f"1. صحة مفتاح API في ملف .env\n"
                f"2. أن النموذج '{LLM_MODEL}' متاح لدى {label}\n"
                f"3. رصيد حسابك في الخدمة"
            ) from e

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"❌ تعذّر الاتصال بـ {label}\n\n"
                f"تأكد من:\n"
                f"1. صحة OLLAMA_BASE_URL في .env (للاستخدام المحلي)\n"
                f"2. تشغيل خادم Ollama: ollama serve\n"
                f"3. توفر الاتصال بالإنترنت (للمزودين السحابيين)"
            )

        except requests.exceptions.Timeout as e:
            raise TimeoutError(
                f"❌ انتهت مهلة الاستجابة من {label}\n\n"
                f"جرب:\n"
                f"1. زيادة مهلة الانتظار\n"
                f"2. استخدام نموذج أصغر\n"
                f"3. التحقق من موارد النظام"
            ) from e

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ خطأ في تحليل استجابة JSON من {label}") from e

    raise RuntimeError(
        f"❌ تجاوز حد الطلبات من {label} بعد {max_retries} محاولات.\n"
        f"انتظر دقيقة ثم حاول مجدداً، أو قلل عدد الطلبات."
    ) from last_error
