def build_markdown_report(ddr_data: dict, summary_text: str = "") -> str:
    """
    Converts a Pydantic DDRResponse dict into a formatted Markdown document.
    """
    
    md = []
    md.append("# Detailed Diagnostic Report (DDR)\n")
    
    if summary_text:
        md.append("## Executive Summary")
        md.append(f"{summary_text}\n")
        
    md.append("## 1. Property Issue Summary")
    props = ddr_data.get('property_summary', {})
    md.append(f"**Overview:** {props.get('overview', 'N/A')}")
    md.append(f"**Total Areas Inspected:** {props.get('total_areas_inspected', 0)}")
    md.append(f"**Critical Issues Count:** {props.get('critical_issues_count', 0)}\n")
    
    md.append("## 2. Area-wise Observations")
    for area in ddr_data.get('area_wise_observations', []):
        md.append(f"### {area.get('area_name', 'Unknown Area')}")
        for obs in area.get('observations', []):
            md.append(f"- **Issue:** {obs.get('issue_description', '')}")
            md.append(f"  - **Severity:** {obs.get('severity', '')}")
            md.append(f"  - **Image Reference:** {obs.get('image_reference', 'Not Available')}")
        md.append("\n")
        
    md.append("## 3. Probable Root Cause")
    md.append(f"{ddr_data.get('probable_root_cause', 'N/A')}\n")
    
    md.append("## 4. Recommended Actions")
    for rec in ddr_data.get('recommended_actions', []):
        md.append(f"- [{rec.get('priority', 'Medium')}] {rec.get('action', '')}")
    md.append("\n")
        
    md.append("## 5. Additional Notes")
    md.append(f"{ddr_data.get('additional_notes', 'N/A')}\n")
    
    md.append("## 6. Missing / Unclear Information")
    md.append(f"{ddr_data.get('missing_unclear_information', 'N/A')}\n")
    
    return "\n".join(md)
