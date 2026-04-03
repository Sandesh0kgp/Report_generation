import glob

for file in glob.glob("**/*.py", recursive=True):
    if "venv" in file or "test_data" in file: continue
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace('\"', '"')
    if content != new_content:
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed quotes in {file}")

