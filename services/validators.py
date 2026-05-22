import re


def validate_national_id(national_id: str) -> bool:
    """
    التحقق من صحة رقم الهوية الوطنية السعودية
    
    الهوية السعودية: 10 أرقام تبدأ بـ:
    - 1 للمواطنين
    - 2 للمقيمين
    
    Args:
        national_id: رقم الهوية الوطنية
        
    Returns:
        True إذا كان الرقم صحيحاً، False خلاف ذلك
    """
    if not national_id:
        return False
    
    national_id = str(national_id).strip()
    
    return bool(re.fullmatch(r"[12]\d{9}", national_id))
