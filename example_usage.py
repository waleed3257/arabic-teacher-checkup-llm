#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مثال على استخدام النظام برمجياً
Example of programmatic usage of the system
"""

from services import validate_national_id, get_teacher_by_id, build_prompt, generate_report


def example_1_basic_usage():
    """مثال 1: الاستخدام الأساسي"""
    print("\n" + "="*70)
    print("مثال 1: الاستخدام الأساسي")
    print("="*70)
    
    national_id = "1065874370"
    
    if not validate_national_id(national_id):
        print("❌ رقم الهوية غير صالح")
        return
    
    teacher = get_teacher_by_id(national_id)
    
    if not teacher:
        print(f"❌ لم يتم العثور على المعلم: {national_id}")
        return
    
    print(f"✅ تم العثور على: {teacher.full_name}")
    print(f"   الرتبة: {teacher.rank}")
    print(f"   التخصص: {teacher.specialization}")
    print(f"   المدرسة: {teacher.school}")


def example_2_detailed_info():
    """مثال 2: عرض معلومات تفصيلية"""
    print("\n" + "="*70)
    print("مثال 2: عرض معلومات تفصيلية")
    print("="*70)
    
    national_id = "1040957142"
    teacher = get_teacher_by_id(national_id)
    
    if not teacher:
        print(f"❌ لم يتم العثور على المعلم")
        return
    
    print(f"\n👤 المعلم: {teacher.full_name}")
    print(f"🆔 الهوية: {teacher.national_id}")
    print(f"🎓 الرتبة: {teacher.rank}")
    print(f"📚 التخصص: {teacher.specialization}")
    print(f"🏫 المدرسة: {teacher.school}")
    print(f"📍 القطاع: {teacher.sector}")
    print(f"🏛️  الإدارة: {teacher.education_admin}")
    print(f"📅 سنة المباشرة: {teacher.start_year}")
    print(f"📝 نوع العقد: {teacher.contract_type}")
    
    print(f"\n📋 برامج فرص: {len(teacher.fursa_programs)}")
    for i, prog in enumerate(teacher.fursa_programs, 1):
        print(f"\n   {i}. {prog.program_name}")
        print(f"      - عدد الرغبات: {len(prog.wishes)}")
        if prog.total_points:
            print(f"      - إجمالي النقاط: {prog.total_points}")
        if prog.nomination_status:
            print(f"      - حالة الترشيح: {prog.nomination_status}")


def example_3_generate_prompt():
    """مثال 3: توليد النص التوجيهي"""
    print("\n" + "="*70)
    print("مثال 3: توليد النص التوجيهي")
    print("="*70)
    
    national_id = "1044846283"
    teacher = get_teacher_by_id(national_id)
    
    if not teacher:
        print(f"❌ لم يتم العثور على المعلم")
        return
    
    prompt = build_prompt(teacher)
    
    print(f"\n📝 النص التوجيهي للمعلم: {teacher.full_name}")
    print("─"*70)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print("─"*70)
    print(f"\nطول النص: {len(prompt)} حرف")


def example_4_batch_processing():
    """مثال 4: معالجة دفعة من المعلمين"""
    print("\n" + "="*70)
    print("مثال 4: معالجة دفعة من المعلمين")
    print("="*70)
    
    import pandas as pd
    
    apps_df = pd.read_excel('data/Application.xlsx', nrows=10)
    sample_ids = apps_df['السجل المدني'].head(5).astype(str).tolist()
    
    results = []
    
    for national_id in sample_ids:
        teacher = get_teacher_by_id(national_id)
        if teacher:
            results.append({
                'id': national_id,
                'name': teacher.full_name,
                'rank': teacher.rank,
                'specialization': teacher.specialization,
                'fursa_count': len(teacher.fursa_programs)
            })
    
    print(f"\n✅ تمت معالجة {len(results)} معلم/معلمة:\n")
    for r in results:
        print(f"   • {r['name']}")
        print(f"     الهوية: {r['id']}")
        print(f"     التخصص: {r['specialization']}")
        print(f"     برامج فرص: {r['fursa_count']}")
        print()


def example_5_generate_report_with_ollama():
    """مثال 5: توليد تقرير كامل باستخدام Ollama"""
    print("\n" + "="*70)
    print("مثال 5: توليد تقرير كامل باستخدام Ollama")
    print("="*70)
    print("⚠️  يتطلب هذا المثال تشغيل Ollama")
    print()
    
    national_id = "1065874370"
    teacher = get_teacher_by_id(national_id)
    
    if not teacher:
        print(f"❌ لم يتم العثور على المعلم")
        return
    
    print(f"📝 توليد تقرير للمعلم: {teacher.full_name}")
    print("⏳ جارٍ الاتصال بـ Ollama...")
    
    prompt = build_prompt(teacher)
    report = generate_report(prompt)
    
    print("\n" + "─"*70)
    print("📋 التقرير الوصفي:")
    print("─"*70)
    print(report)
    print("─"*70)


def main():
    """تشغيل جميع الأمثلة"""
    print("\n" + "📚 "*20)
    print("أمثلة على استخدام نظام توليد التقارير الوصفية للمعلمين")
    print("Examples of Arabic Teacher Checkup Narrative Generator")
    print("📚 "*20)
    
    try:
        example_1_basic_usage()
        example_2_detailed_info()
        example_3_generate_prompt()
        example_4_batch_processing()
        
        print("\n" + "="*70)
        user_input = input("هل تريد تجربة توليد تقرير باستخدام Ollama؟ (y/n): ")
        if user_input.lower() in ['y', 'yes', 'نعم', 'ن']:
            example_5_generate_report_with_ollama()
        else:
            print("\n⏭️  تم تخطي مثال Ollama")
        
        print("\n" + "="*70)
        print("✅ انتهت جميع الأمثلة!")
        print("="*70)
        print("\nللاستخدام الكامل، شغل: python main.py")
        print()
        
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
