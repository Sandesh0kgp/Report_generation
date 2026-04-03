from reportlab.pdfgen import canvas
import os

def create_inspection_pdf(filepath):
    c = canvas.Canvas(filepath)
    c.drawString(100, 750, "Sample Inspection Report")
    c.drawString(100, 730, "Property: 123 Main St")
    c.drawString(100, 710, "Issues Found:")
    c.drawString(100, 690, "- Kitchen sink tap is leaking water underneath the cabinet.")
    c.drawString(100, 670, "- Faint water scale marks found on the bedroom wall near the window.")
    c.save()

def create_thermal_pdf(filepath):
    c = canvas.Canvas(filepath)
    c.drawString(100, 750, "Sample Thermal Report")
    c.drawString(100, 730, "Thermal Anomalies Detected:")
    c.drawString(100, 710, "1. Distinct cold spot beneath kitchen sink area (-4 C from ambient).")
    c.drawString(100, 690, "2. No anomalies detected around the bedroom wall window edge.")
    c.save()

if __name__ == "__main__":
    os.makedirs("test_data", exist_ok=True)
    create_inspection_pdf("test_data/sample_inspection.pdf")
    create_thermal_pdf("test_data/sample_thermal.pdf")
    print("Mock PDFs generated inside test_data/")
