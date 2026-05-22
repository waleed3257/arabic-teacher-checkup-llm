from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class FursaProgram:
    program_name: str
    wishes: List[Dict[str, str]] = field(default_factory=list)
    professional_points: Optional[float] = None
    license_points_educational: Optional[float] = None
    license_points_specialization: Optional[float] = None
    total_points: Optional[float] = None
    nomination_status: Optional[str] = None
    min_transfer_points: Optional[float] = None
    is_nominated: Optional[str] = None
    nominated_sector: Optional[str] = None


@dataclass
class Teacher:
    national_id: str
    full_name: str
    gender: Optional[str] = None
    rank: Optional[str] = None
    specialization: Optional[str] = None
    school: Optional[str] = None
    sector: Optional[str] = None
    education_admin: Optional[str] = None
    start_year: Optional[str] = None
    contract_type: Optional[str] = None
    current_work: Optional[str] = None
    stage: Optional[str] = None
    fursa_programs: List[FursaProgram] = field(default_factory=list)
