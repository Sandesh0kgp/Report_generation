import os
import glob

def fix_files():
    for ext in ['*.py', '*.ipynb', '*.md']:
        for file in glob.glob(f"**/{ext}", recursive=True):
            if 'venv' in file or 'test_data' in file:
                continue
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix backslash escaped quotes that were injected
            new_content = content.replace(r'"""', '"""')
            
            if file.endswith('.py'):
                # Avoid accidentally replacing valid 
 if any, but since the only 
 injected was for string newlines:
                new_content = new_content.replace(r'
', '
')
                
            if new_content != content:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {file}")

if __name__ == "__main__":
    fix_files()
