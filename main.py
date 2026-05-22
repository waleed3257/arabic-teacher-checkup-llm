#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
برنامج توليد التقارير الوصفية للمعلمين باستخدام الذكاء الاصطناعي
Arabic Teacher Checkup Narrative Generator with Ollama LLM

الاستخدام:
    python main.py
"""

import sys
from services import validate_national_id, get_teacher_by_id, build_prompt, generate_report


def print_header():
    """طباعة ترويسة البرنامج"""
    print("\n" + "="*70)
    print("📋 برنامج توليد التقارير الوصفية للمعلمين")
    print("Arabic Teacher Checkup Narrative Generator")
    print("="*70 + "\n")


def print_separator():
    """طباعة خط فاصل"""
    print("\n" + "─"*70 + "\n")


def main():
    """الدالة الرئيسية للبرنامج"""
    print_header()
    
    national_id = input("🔍 أدخل رقم الهوية الوطنية (10 أرقام): ").strip()
    
    if not validate_national_id(national_id):
        print("\n❌ رقم الهوية غير صالح!")
        print("   يجب أن يكون الرقم مكوناً من 10 أرقام ويبدأ بـ 1 (مواطن) أو 2 (مقيم)")
        sys.exit(1)
    
    print(f"\n⏳ جارٍ البحث عن بيانات الهوية: {national_id}")
    
    try:
        teacher = get_teacher_by_id(national_id)
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("   تأكد من وجود ملفات Excel في المسار: /Users/waleedalhojaili/Dev/Leqa/data/")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ في تحميل البيانات: {e}")
        sys.exit(1)
    
    if not teacher:
        print(f"\n❌ لم يتم العثور على بيانات للهوية: {national_id}")
        print("   تأكد من صحة رقم الهوية ووجوده في ملف teachers.xlsx")
        sys.exit(1)
    
    print(f"✅ تم العثور على المعلم: {teacher.full_name}")
    
    print("\n📝 جارٍ بناء البيانات التفصيلية...")
    prompt = build_prompt(teacher)
    
    print_separator()
    print("📊 البيانات المجمعة:")
    print_separator()
    print(prompt)
    print_separator()
    
    print("\n🤖 جارٍ توليد التقرير الوصفي باستخدام الذكاء الاصطناعي...")
    print("   (قد يستغرق هذا بضع ثوانٍ...)\n")
    
    try:
        report = generate_report(prompt)
    except Exception as e:
        print(f"\n{e}")
        sys.exit(1)
    
    print_separator()
    print("📋 التقرير الوصفي النهائي:")
    print_separator()
    print(report)
    print_separator()
    
    print("\n✅ تم إنشاء التقرير بنجاح!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)
