from pydantic import BaseModel, Field
from typing import List, Optional

class Observation(BaseModel):
    issue_description: str = Field(default="Not Available", description="Clear description of the issue found")
    severity: str = Field(default="Unknown", description="Severity measure: Low, Medium, High, or Critical")
    image_reference: str = Field(default="Image Not Available", description="Image page/ID reference")

class AreaInsight(BaseModel):
    area_name: str = Field(default="Unknown Area", description="The specific area or room name")
    observations: List[Observation] = Field(default_factory=list, description="List of issues")

class ReportSummary(BaseModel):
    overview: str = Field(default="Not Available", description="General overview of the property's condition")
    total_areas_inspected: int = Field(default=0)
    critical_issues_count: int = Field(default=0)
    
class Recommendation(BaseModel):
    action: str = Field(default="No specific action", description="Recommended action")
    priority: str = Field(default="Unknown", description="Priority")

class DDRResponse(BaseModel):
    property_summary: ReportSummary = Field(default_factory=ReportSummary)
    area_wise_observations: List[AreaInsight] = Field(default_factory=list)
    probable_root_cause: str = Field(default="Not Available", description="Combined assessment of root causes")
    recommended_actions: List[Recommendation] = Field(default_factory=list)
    additional_notes: str = Field(default="Not Available", description="Any other findings or notes")
    missing_unclear_information: str = Field(default="None", description="Points where data is conflicting")
