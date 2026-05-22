import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import os


def read_ids_from_excel(file_path: str) -> List[str]:
    """
    قراءة أرقام الهوية من ملف Excel
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        قائمة بأرقام الهوية
    """
    try:
        df = pd.read_excel(file_path)
        
        id_column = None
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if 'id' in col_lower or 'هوية' in col_lower or 'سجل' in col_lower:
                id_column = col
                break
        
        if id_column is None:
            id_column = df.columns[0]
        
        ids = df[id_column].astype(str).str.strip().tolist()
        ids = [id_val for id_val in ids if id_val and id_val != 'nan']
        
        return ids
        
    except Exception as e:
        raise Exception(f"خطأ في قراءة ملف Excel: {e}")


def save_individual_result(national_id: str, name: str, report: str, output_dir: str = "output") -> str:
    """
    حفظ نتيجة فردية في ملف Excel
    
    Args:
        national_id: رقم الهوية
        name: اسم المعلم
        report: التقرير النصي
        output_dir: مجلد الحفظ
        
    Returns:
        مسار الملف المحفوظ
    """
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame([{
        'ID': national_id,
        'Name': name,
        'Full Text': report
    }])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{national_id}_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return filepath


def save_bulk_results(results: List[Dict], output_dir: str = "output") -> str:
    """
    حفظ نتائج دفعة في ملف Excel واحد
    
    Args:
        results: قائمة بالنتائج، كل عنصر يحتوي على {id, name, report}
        output_dir: مجلد الحفظ
        
    Returns:
        مسار الملف المحفوظ
    """
    os.makedirs(output_dir, exist_ok=True)
    
    data = []
    for result in results:
        data.append({
            'ID': result.get('id', ''),
            'Name': result.get('name', ''),
            'Full Text': result.get('report', '')
        })
    
    df = pd.DataFrame(data)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bulk_report_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return filepath


def ensure_directories():
    """التأكد من وجود المجلدات المطلوبة"""
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
