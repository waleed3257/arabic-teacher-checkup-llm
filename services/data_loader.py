import pandas as pd
from typing import Optional, List, Dict
from models.teacher import Teacher, FursaProgram
from config import EXCEL_FILES


def load_excel_files() -> Dict[str, pd.DataFrame]:
    """
    تحميل جميع ملفات Excel
    
    Returns:
        قاموس يحتوي على DataFrames لكل ملف
    """
    dataframes = {}
    
    try:
        dataframes["teachers"] = pd.read_excel(EXCEL_FILES["teachers"])
        dataframes["applications"] = pd.read_excel(EXCEL_FILES["applications"])
        dataframes["results"] = pd.read_excel(EXCEL_FILES["results"])
        dataframes["moved"] = pd.read_excel(EXCEL_FILES["moved"])
        
        for key in dataframes:
            dataframes[key].columns = dataframes[key].columns.str.strip()
            
    except FileNotFoundError as e:
        raise FileNotFoundError(f"لم يتم العثور على ملف Excel: {e}")
    except Exception as e:
        raise Exception(f"خطأ في تحميل ملفات Excel: {e}")
    
    return dataframes


def get_teacher_by_id(national_id: str) -> Optional[Teacher]:
    """
    جلب بيانات المعلم من خلال رقم الهوية الوطنية
    
    Args:
        national_id: رقم الهوية الوطنية
        
    Returns:
        كائن Teacher يحتوي على جميع البيانات، أو None إذا لم يتم العثور على المعلم
    """
    dfs = load_excel_files()
    
    teachers_df = dfs["teachers"]
    applications_df = dfs["applications"]
    results_df = dfs["results"]
    
    teacher_row = teachers_df[teachers_df["السجل المدني"].astype(str) == str(national_id)]
    
    if teacher_row.empty:
        return None
    
    teacher_data = teacher_row.iloc[0]
    
    teacher = Teacher(
        national_id=str(national_id),
        full_name=str(teacher_data.get("الاسم", "")).strip() if pd.notna(teacher_data.get("الاسم")) else None,
        gender=str(teacher_data.get("الجنس", "")).strip() if pd.notna(teacher_data.get("الجنس")) else None,
        rank=str(teacher_data.get("الرتبة", "")).strip() if pd.notna(teacher_data.get("الرتبة")) else None,
        specialization=str(teacher_data.get("التخصص", "")).strip() if pd.notna(teacher_data.get("التخصص")) else None,
        school=str(teacher_data.get("اسم المدرسة", "")).strip() if pd.notna(teacher_data.get("اسم المدرسة")) else None,
        sector=str(teacher_data.get("القطاع التعليمي", "")).strip() if pd.notna(teacher_data.get("القطاع التعليمي")) else None,
        education_admin=str(teacher_data.get("ادارة التعليم", "")).strip() if pd.notna(teacher_data.get("ادارة التعليم")) else None,
        start_year=str(teacher_data.get("سنة المباشرة", "")).strip() if pd.notna(teacher_data.get("سنة المباشرة")) else None,
        contract_type=str(teacher_data.get("نوع العقد", "")).strip() if pd.notna(teacher_data.get("نوع العقد")) else None,
        current_work=str(teacher_data.get("العمل الحالي", "")).strip() if pd.notna(teacher_data.get("العمل الحالي")) else None,
        stage=str(teacher_data.get("المرحلة الدراسية", "")).strip() if pd.notna(teacher_data.get("المرحلة الدراسية")) else None,
    )
    
    applications = applications_df[applications_df["السجل المدني"].astype(str) == str(national_id)]
    
    fursa_programs = []
    
    for _, app_row in applications.iterrows():
        program_name = str(app_row.get("الإعلان", "")).strip() if pd.notna(app_row.get("الإعلان")) else "غير محدد"
        
        wishes = []
        for i in range(10):
            wish_num_col = f"رقم الرغبة" if i == 0 else f"رقم الرغبة.{i}"
            sector_col = f"اسم القطاع" if i == 0 else f"اسم القطاع.{i}"
            admin_col = f"الإدارة العامة" if i == 0 else f"الإدارة العامة.{i}"
            
            if wish_num_col in app_row and pd.notna(app_row.get(wish_num_col)):
                wish = {
                    "number": str(app_row.get(wish_num_col, "")).strip(),
                    "sector": str(app_row.get(sector_col, "")).strip() if pd.notna(app_row.get(sector_col)) else "",
                    "admin": str(app_row.get(admin_col, "")).strip() if pd.notna(app_row.get(admin_col)) else "",
                }
                wishes.append(wish)
        
        result_row = results_df[
            (results_df["السجل المدني"].astype(str) == str(national_id)) &
            (results_df["الإعلان"].astype(str).str.strip() == program_name)
        ]
        
        nomination_status = None
        total_points = None
        min_transfer_points = None
        is_nominated = None
        nominated_sector = None
        
        if not result_row.empty:
            result_data = result_row.iloc[0]
            nomination_status = str(result_data.get("حالة الترشيح", "")).strip() if pd.notna(result_data.get("حالة الترشيح")) else None
            total_points = float(result_data.get("اجمالي نقاط المفاضلة")) if pd.notna(result_data.get("اجمالي نقاط المفاضلة")) else None
            min_transfer_points = float(result_data.get("نقاط_أقل_من_نقل")) if pd.notna(result_data.get("نقاط_أقل_من_نقل")) else None
            is_nominated = str(result_data.get("مرشح \\ غير مرشح", "")).strip() if pd.notna(result_data.get("مرشح \\ غير مرشح")) else None
            nominated_sector = str(result_data.get("القطاع المرشح عليه", "")).strip() if pd.notna(result_data.get("القطاع المرشح عليه")) else None
        
        fursa_program = FursaProgram(
            program_name=program_name,
            wishes=wishes,
            professional_points=float(app_row.get("نقاط التطوير المهني")) if pd.notna(app_row.get("نقاط التطوير المهني")) else None,
            license_points_educational=float(app_row.get("نقاط الرخصة المهنية تربوي")) if pd.notna(app_row.get("نقاط الرخصة المهنية تربوي")) else None,
            license_points_specialization=float(app_row.get("نقاط الرخصة المهنية تخصص")) if pd.notna(app_row.get("نقاط الرخصة المهنية تخصص")) else None,
            total_points=total_points,
            nomination_status=nomination_status,
            min_transfer_points=min_transfer_points,
            is_nominated=is_nominated,
            nominated_sector=nominated_sector,
        )
        
        fursa_programs.append(fursa_program)
    
    fursa_programs.sort(key=lambda x: x.program_name, reverse=True)
    
    teacher.fursa_programs = fursa_programs
    
    return teacher
