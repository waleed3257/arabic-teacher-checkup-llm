from datetime import datetime
from models.teacher import Teacher


def calculate_service_years(start_year_hijri: str) -> int:
    """
    حساب سنوات الخدمة من سنة المباشرة الهجرية
    
    Args:
        start_year_hijri: سنة المباشرة بالتقويم الهجري
        
    Returns:
        عدد سنوات الخدمة التقريبي
    """
    current_hijri = 1446
    
    try:
        start = int(float(str(start_year_hijri).strip()))
        years = current_hijri - start
        return max(0, years)
    except (ValueError, TypeError, AttributeError):
        return 0


def build_prompt(teacher: Teacher) -> str:
    """
    بناء النص التوجيهي (Prompt) للنموذج اللغوي من بيانات المعلم
    
    Args:
        teacher: كائن Teacher يحتوي على بيانات المعلم
        
    Returns:
        نص توجيهي منسق للنموذج اللغوي
    """
    service_years = calculate_service_years(teacher.start_year) if teacher.start_year else 0
    
    lines = [
        "بيانات المعلم الأساسية:",
        f"- الاسم الكامل: {teacher.full_name}",
        f"- رقم الهوية الوطنية: {teacher.national_id}",
    ]
    
    if teacher.rank:
        rank_display = teacher.rank
        for prefix in ("رتبة معلم ", "رتبة ", "معلم "):
            if rank_display.startswith(prefix):
                rank_display = rank_display[len(prefix):]
                break
        lines.append(f"- الرتبة: {rank_display}")
    
    if teacher.specialization:
        lines.append(f"- التخصص: {teacher.specialization}")
    
    if teacher.school:
        lines.append(f"- المدرسة: {teacher.school}")
    
    if teacher.sector:
        lines.append(f"- القطاع التعليمي: {teacher.sector}")
    
    if teacher.education_admin:
        lines.append(f"- إدارة التعليم: {teacher.education_admin}")
    
    if teacher.stage:
        lines.append(f"- المرحلة الدراسية: {teacher.stage}")
    
    if teacher.start_year:
        lines.append(f"- سنة المباشرة: {teacher.start_year} هـ (حوالي {service_years} سنوات خدمة)")
    
    if teacher.contract_type:
        lines.append(f"- نوع العقد: {teacher.contract_type}")
    
    if teacher.current_work:
        lines.append(f"- العمل الحالي: {teacher.current_work}")
    
    lines.append("")
    lines.append("برامج فرص للنقل الداخلي:")
    
    if not teacher.fursa_programs:
        lines.append("- لا توجد طلبات في برنامج فرص")
    else:
        latest_program = teacher.fursa_programs[0]
        
        lines.append(f"\n[البرنامج الأحدث: {latest_program.program_name}]")
        
        if latest_program.wishes:
            lines.append(f"  عدد الرغبات: {len(latest_program.wishes)}")
            for i, wish in enumerate(latest_program.wishes[:3], 1):
                if wish.get("sector"):
                    lines.append(f"  - الرغبة {wish.get('number', i)}: {wish.get('sector')} ({wish.get('admin', 'غير محدد')})")
        else:
            lines.append("  - لا توجد رغبات مسجلة")
        
        if latest_program.professional_points is not None:
            lines.append(f"  نقاط التطوير المهني: {latest_program.professional_points}")
        
        if latest_program.license_points_educational is not None:
            lines.append(f"  نقاط الرخصة المهنية (تربوي): {latest_program.license_points_educational}")
        
        if latest_program.license_points_specialization is not None:
            lines.append(f"  نقاط الرخصة المهنية (تخصص): {latest_program.license_points_specialization}")
        
        if latest_program.total_points is not None:
            lines.append(f"  إجمالي نقاط المفاضلة: {latest_program.total_points}")
        
        if latest_program.is_nominated:
            lines.append(f"  حالة الترشيح: {latest_program.is_nominated}")
        
        if latest_program.nomination_status:
            lines.append(f"  تفاصيل الترشيح: {latest_program.nomination_status}")
        
        if latest_program.nominated_sector:
            lines.append(f"  القطاع المرشح عليه: {latest_program.nominated_sector}")
        
        if latest_program.min_transfer_points is not None:
            lines.append(f"  أقل نقاط للنقل في القطاع المطلوب: {latest_program.min_transfer_points}")
        
        if len(teacher.fursa_programs) > 1:
            lines.append(f"\nالبرامج السابقة:")
            for prog in teacher.fursa_programs[1:]:
                if prog.wishes:
                    lines.append(f"  - {prog.program_name}: تقدم بـ {len(prog.wishes)} رغبة/رغبات")
                else:
                    lines.append(f"  - {prog.program_name}: لم يتقدم أو لا توجد بيانات")
    
    lines.append("\n" + "="*60)
    lines.append("المطلوب:")
    lines.append("اكتب ملخصاً مباشراً وموجزاً في سطرين أو ثلاثة أسطر فقط، بدون مقدمة أو شرح.")
    lines.append("اتبع النمط: المعلم [الاسم] هوية وطنية رقم [الرقم] معلم رتبة [الرتبة] بإدارة تعليم [الإدارة]، تخصصه [التخصص] بقطاع [القطاع]، خدمته [السنوات] سنوات من [نوع العقد]، [حالة فرص بإيجاز]، علماً أن إجمالي نقاطه هي [النقاط] و[هل له تقديم سابق أم لا].")
    
    return "\n".join(lines)
