#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
برنامج توليد التقارير الوصفية للمعلمين - النسخة المحسنة
Arabic Teacher Checkup Narrative Generator - Enhanced Version

يدعم:
- معالجة فردية (Individual): إدخال رقم هوية واحد
- معالجة دفعة (Bulk): قراءة من ملف Excel

الاستخدام:
    python main_enhanced.py
"""

import sys
from pathlib import Path
from services import (
    validate_national_id,
    get_teacher_by_id,
    build_prompt,
    generate_report,
    read_ids_from_excel,
    save_individual_result,
    save_bulk_results,
    ensure_directories,
)


def print_header():
    """طباعة ترويسة البرنامج"""
    print("\n" + "="*70)
    print("📋 برنامج توليد التقارير الوصفية للمعلمين - النسخة المحسنة")
    print("Arabic Teacher Checkup Narrative Generator - Enhanced")
    print("="*70 + "\n")


def print_separator():
    """طباعة خط فاصل"""
    print("\n" + "─"*70 + "\n")


def show_menu():
    """عرض القائمة الرئيسية"""
    print("\n" + "="*70)
    print("اختر طريقة المعالجة:")
    print("="*70)
    print("1️⃣  معالجة فردية (Individual) - إدخال رقم هوية واحد")
    print("2️⃣  معالجة دفعة (Bulk) - قراءة من ملف Excel")
    print("0️⃣  خروج")
    print("="*70)


def process_individual():
    """معالجة رقم هوية فردي"""
    print("\n" + "="*70)
    print("📝 المعالجة الفردية")
    print("="*70)
    
    national_id = input("\n🔍 أدخل رقم الهوية الوطنية (10 أرقام): ").strip()
    
    if not validate_national_id(national_id):
        print("\n❌ رقم الهوية غير صالح!")
        print("   يجب أن يكون الرقم مكوناً من 10 أرقام ويبدأ بـ 1 (مواطن) أو 2 (مقيم)")
        return
    
    print(f"\n⏳ جارٍ البحث عن بيانات الهوية: {national_id}")
    
    try:
        teacher = get_teacher_by_id(national_id)
    except Exception as e:
        print(f"\n❌ خطأ في تحميل البيانات: {e}")
        return
    
    if not teacher:
        print(f"\n❌ لم يتم العثور على بيانات للهوية: {national_id}")
        return
    
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
    
    report = generate_report(prompt)
    
    print_separator()
    print("📋 التقرير الوصفي النهائي:")
    print_separator()
    print(report)
    print_separator()
    
    try:
        output_file = save_individual_result(national_id, teacher.full_name, report)
        print(f"\n💾 تم حفظ التقرير في: {output_file}")
    except Exception as e:
        print(f"\n⚠️  تعذر حفظ الملف: {e}")
    
    print("\n✅ تم إنشاء التقرير بنجاح!\n")


def process_bulk():
    """معالجة دفعة من الأرقام من ملف Excel"""
    print("\n" + "="*70)
    print("📦 المعالجة الدفعية")
    print("="*70)
    
    input_file = "input/id.xlsx"
    
    if not Path(input_file).exists():
        print(f"\n❌ ملف الإدخال غير موجود: {input_file}")
        print("   يرجى إنشاء ملف Excel في مجلد input/ باسم id.xlsx")
        print("   يجب أن يحتوي الملف على عمود واحد على الأقل بأرقام الهوية")
        return
    
    print(f"\n📂 قراءة الأرقام من: {input_file}")
    
    try:
        ids = read_ids_from_excel(input_file)
        print(f"✅ تم العثور على {len(ids)} رقم هوية")
    except Exception as e:
        print(f"\n❌ خطأ في قراءة الملف: {e}")
        return
    
    if not ids:
        print("\n❌ لا توجد أرقام هوية في الملف")
        return
    
    print(f"\n⏳ جارٍ معالجة {len(ids)} معلم/معلمة...")
    print("   (قد يستغرق هذا عدة دقائق...)\n")
    
    results = []
    success_count = 0
    error_count = 0
    
    for i, national_id in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}] معالجة: {national_id}...", end=" ")
        
        if not validate_national_id(national_id):
            print("❌ رقم غير صالح")
            error_count += 1
            results.append({
                'id': national_id,
                'name': 'رقم هوية غير صالح',
                'report': 'خطأ: رقم الهوية غير صالح'
            })
            continue
        
        try:
            teacher = get_teacher_by_id(national_id)
            
            if not teacher:
                print("❌ غير موجود")
                error_count += 1
                results.append({
                    'id': national_id,
                    'name': 'غير موجود',
                    'report': 'خطأ: لم يتم العثور على المعلم في قاعدة البيانات'
                })
                continue
            
            prompt = build_prompt(teacher)
            report = generate_report(prompt)
            
            results.append({
                'id': national_id,
                'name': teacher.full_name,
                'report': report
            })
            
            print(f"✅ {teacher.full_name}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ خطأ: {str(e)[:50]}")
            error_count += 1
            results.append({
                'id': national_id,
                'name': 'خطأ',
                'report': f'خطأ في المعالجة: {str(e)}'
            })
    
    print_separator()
    print("📊 ملخص المعالجة:")
    print(f"   ✅ نجح: {success_count}")
    print(f"   ❌ فشل: {error_count}")
    print(f"   📝 إجمالي: {len(ids)}")
    print_separator()
    
    try:
        output_file = save_bulk_results(results)
        print(f"\n💾 تم حفظ النتائج في: {output_file}")
        print(f"   الملف يحتوي على 3 أعمدة: ID, Name, Full Text")
    except Exception as e:
        print(f"\n❌ خطأ في حفظ الملف: {e}")
        return
    
    print("\n✅ تمت المعالجة الدفعية بنجاح!\n")


def main():
    """الدالة الرئيسية للبرنامج"""
    print_header()
    
    ensure_directories()
    
    while True:
        show_menu()
        
        choice = input("\nاختر (1/2/0): ").strip()
        
        if choice == "1":
            process_individual()
        elif choice == "2":
            process_bulk()
        elif choice == "0":
            print("\n👋 شكراً لاستخدامك البرنامج. وداعاً!\n")
            sys.exit(0)
        else:
            print("\n❌ خيار غير صحيح. يرجى اختيار 1 أو 2 أو 0")
        
        input("\n⏎ اضغط Enter للمتابعة...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)
