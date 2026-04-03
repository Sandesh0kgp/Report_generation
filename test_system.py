import requests
import sys

URL = "http://localhost:8005/process"

def test_api():
    print("Sending POST request to FastAPI...")
    files = {
        'inspection_file': ('sample_inspection.pdf', open('test_data/sample_inspection.pdf', 'rb'), 'application/pdf'),
        'thermal_file': ('sample_thermal.pdf', open('test_data/sample_thermal.pdf', 'rb'), 'application/pdf')
    }
    
    try:
        response = requests.post(URL, files=files)
        response.raise_for_status()
        
        data = response.json()
        print("\n✅ Request Successful!")
        print(f"Status: {data.get('status')}")
        print("======== EXTRACTED SUMMARY (via Groq) ========")
        print(data.get('summary_text'))
        print("\n======== FINAL MARKDOWN DDR (via Gemini) ========")
        print(data.get('markdown_report'))
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(response.text)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_api()
