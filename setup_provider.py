#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
معالج إعداد مزود LLM
LLM Provider Setup Wizard
"""

import os
import sys
from pathlib import Path
from dotenv import dotenv_values, set_key

ENV_PATH = Path(__file__).parent / ".env"

PROVIDERS = {
    "1": {
        "id": "ollama",
        "name": "Ollama (Local / Self-hosted)",
        "key_var": None,
        "default_model": "gemma4:latest",
        "model_examples": ["gemma4:latest", "llama3.1:8b", "deepseek-r1:8b", "mistral:latest"],
        "extra": {"OLLAMA_BASE_URL": "http://localhost:11434"},
    },
    "2": {
        "id": "openai",
        "name": "OpenAI",
        "key_var": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
        "model_examples": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        "extra": {"OPENAI_BASE_URL": "https://api.openai.com/v1"},
    },
    "3": {
        "id": "openrouter",
        "name": "OpenRouter",
        "key_var": "OPENROUTER_API_KEY",
        "default_model": "google/gemini-2.0-flash",
        "model_examples": [
            "google/gemini-2.0-flash",
            "openai/gpt-4o",
            "anthropic/claude-3.5-haiku",
            "meta-llama/llama-3.1-8b-instruct",
        ],
        "extra": {},
    },
    "4": {
        "id": "google",
        "name": "Google AI (Gemini)",
        "key_var": "GOOGLE_API_KEY",
        "default_model": "gemini-2.0-flash",
        "model_examples": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        "extra": {},
    },
    "5": {
        "id": "anthropic",
        "name": "Anthropic (Claude)",
        "key_var": "ANTHROPIC_API_KEY",
        "default_model": "claude-3-5-haiku-20241022",
        "model_examples": [
            "claude-3-5-haiku-20241022",
            "claude-3-5-sonnet-20241022",
            "claude-opus-4-5",
        ],
        "extra": {},
    },
}


def print_header():
    print("\n" + "=" * 60)
    print("⚙️  معالج إعداد مزود LLM  |  LLM Provider Setup Wizard")
    print("=" * 60 + "\n")


def print_current_config():
    config = dotenv_values(ENV_PATH)
    provider = config.get("LLM_PROVIDER", "غير محدد")
    model = config.get("LLM_MODEL", "غير محدد")

    print("📋 الإعداد الحالي / Current Configuration:")
    print(f"   Provider : {provider}")
    print(f"   Model    : {model}")

    key_vars = ["OPENAI_API_KEY", "OPENROUTER_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"]
    for var in key_vars:
        val = config.get(var, "")
        if val:
            masked = val[:8] + "..." + val[-4:] if len(val) > 12 else "****"
            print(f"   {var}: {masked}")
    print()


def choose_provider() -> dict:
    print("🔌 اختر المزود / Choose Provider:\n")
    for num, p in PROVIDERS.items():
        print(f"   {num}) {p['name']}")
    print()

    while True:
        choice = input("اختر رقم المزود (1-5): ").strip()
        if choice in PROVIDERS:
            return PROVIDERS[choice]
        print("   ❌ خيار غير صحيح. أدخل رقماً من 1 إلى 5.\n")


def choose_model(provider: dict) -> str:
    examples = provider["model_examples"]
    default = provider["default_model"]

    print(f"\n🤖 اختر النموذج / Choose Model:")
    print(f"   أمثلة / Examples:")
    for i, m in enumerate(examples, 1):
        print(f"      {i}) {m}")
    print()

    user_input = input(f"اسم النموذج (Enter للافتراضي: {default}): ").strip()
    return user_input if user_input else default


def get_api_key(provider: dict) -> str | None:
    key_var = provider.get("key_var")
    if not key_var:
        return None

    config = dotenv_values(ENV_PATH)
    existing = config.get(key_var, "")
    masked = (existing[:8] + "..." + existing[-4:]) if len(existing) > 12 else ""

    print(f"\n🔑 مفتاح API / API Key  ({key_var}):")
    if existing:
        print(f"   القيمة الحالية / Current: {masked}")
        keep = input("   هل تريد الإبقاء عليه؟ Keep it? (Y/n): ").strip().lower()
        if keep != "n":
            return existing

    while True:
        key = input(f"   أدخل {key_var}: ").strip()
        if key:
            return key
        print("   ❌ المفتاح مطلوب لهذا المزود.\n")


def get_ollama_url() -> str:
    config = dotenv_values(ENV_PATH)
    current = config.get("OLLAMA_BASE_URL", "http://localhost:11434")
    print(f"\n🌐 Ollama Base URL (الحالي: {current}):")
    url = input("   أدخل URL أو Enter للإبقاء على الحالي: ").strip()
    return url if url else current


def save_config(provider: dict, model: str, api_key: str | None, extra_overrides: dict):
    if not ENV_PATH.exists():
        ENV_PATH.touch()

    set_key(str(ENV_PATH), "LLM_PROVIDER", provider["id"])
    set_key(str(ENV_PATH), "LLM_MODEL", model)

    for k, v in extra_overrides.items():
        set_key(str(ENV_PATH), k, v)

    if api_key and provider["key_var"]:
        set_key(str(ENV_PATH), provider["key_var"], api_key)

    print("\n✅ تم حفظ الإعدادات في .env بنجاح!")
    print(f"   LLM_PROVIDER = {provider['id']}")
    print(f"   LLM_MODEL    = {model}")
    if provider["key_var"]:
        print(f"   {provider['key_var']} = ****")
    print()


def main():
    print_header()
    print_current_config()

    provider = choose_provider()
    model = choose_model(provider)

    extra_overrides = dict(provider["extra"])

    if provider["id"] == "ollama":
        extra_overrides["OLLAMA_BASE_URL"] = get_ollama_url()
        api_key = None
    else:
        api_key = get_api_key(provider)

    print("\n" + "-" * 60)
    print("📝 ملخص الإعداد / Configuration Summary:")
    print(f"   Provider : {provider['name']}")
    print(f"   Model    : {model}")
    if api_key:
        masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "****"
        print(f"   API Key  : {masked}")
    print("-" * 60)

    confirm = input("\nحفظ الإعدادات؟ Save? (Y/n): ").strip().lower()
    if confirm == "n":
        print("\n⚠️  تم الإلغاء. لم يتم حفظ أي تغييرات.\n")
        sys.exit(0)

    save_config(provider, model, api_key, extra_overrides)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم الإلغاء.\n")
        sys.exit(0)
