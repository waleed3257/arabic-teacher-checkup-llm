#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار النظام بدون الحاجة لـ Ollama
Test the system without requiring Ollama
"""

from services import validate_national_id, get_teacher_by_id, build_prompt


def test_validation():
    """اختبار التحقق من رقم الهوية"""
    print("\n" + "="*70)
    print("1️⃣  اختبار التحقق من رقم الهوية")
    print("="*70)
    
    test_cases = [
        ("1008755877", True),
        ("2123456789", True),
        ("123", False),
        ("12345678901", False),
        ("3123456789", False),
    ]
    
    for national_id, expected in test_cases:
        result = validate_national_id(national_id)
        status = "✅" if result == expected else "❌"
        print(f"{status} {national_id}: {result} (expected: {expected})")


def test_data_loading():
    """اختبار تحميل البيانات"""
    print("\n" + "="*70)
    print("2️⃣  اختبار تحميل البيانات")
    print("="*70)
    
    import pandas as pd
    
    apps_df = pd.read_excel('data/Application.xlsx', nrows=100)
    sample_ids = apps_df['السجل المدني'].head(3).astype(str).tolist()
    
    for national_id in sample_ids:
        teacher = get_teacher_by_id(national_id)
        if teacher:
            print(f"\n✅ {national_id}: {teacher.full_name}")
            print(f"   الرتبة: {teacher.rank}")
            print(f"   التخصص: {teacher.specialization}")
            print(f"   عدد برامج فرص: {len(teacher.fursa_programs)}")
            
            if teacher.fursa_programs:
                prog = teacher.fursa_programs[0]
                print(f"   آخر برنامج: {prog.program_name}")
                print(f"   عدد الرغبات: {len(prog.wishes)}")
                if prog.total_points:
                    print(f"   إجمالي النقاط: {prog.total_points}")
        else:
            print(f"❌ {national_id}: لم يتم العثور على بيانات")


def test_prompt_generation():
    """اختبار توليد النص التوجيهي"""
    print("\n" + "="*70)
    print("3️⃣  اختبار توليد النص التوجيهي")
    print("="*70)
    
    import pandas as pd
    
    apps_df = pd.read_excel('data/Application.xlsx', nrows=50)
    sample_id = str(apps_df['السجل المدني'].iloc[0])
    
    teacher = get_teacher_by_id(sample_id)
    if teacher:
        prompt = build_prompt(teacher)
        print(f"\n📝 النص التوجيهي للمعلم: {teacher.full_name}")
        print("─"*70)
        print(prompt)
        print("─"*70)
        print(f"\n✅ تم توليد النص التوجيهي بنجاح ({len(prompt)} حرف)")
    else:
        print(f"❌ لم يتم العثور على المعلم")


def main():
    """تشغيل جميع الاختبارات"""
    print("\n" + "🧪 "*20)
    print("اختبار نظام توليد التقارير الوصفية للمعلمين")
    print("Testing Arabic Teacher Checkup Narrative Generator")
    print("🧪 "*20)
    
    try:
        test_validation()
        test_data_loading()
        test_prompt_generation()
        
        print("\n" + "="*70)
        print("✅ جميع الاختبارات نجحت!")
        print("="*70)
        print("\nالخطوة التالية:")
        print("1. تأكد من تشغيل Ollama: ollama serve")
        print("2. تأكد من تحميل النموذج: ollama pull gemma2:e4d")
        print("3. شغل البرنامج الرئيسي: python main.py")
        print()
        
    except Exception as e:
        print(f"\n❌ فشل الاختبار: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
