# archiver.py
import os
import shutil
from datetime import datetime
import zipfile

def archive_logs():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = f"archives/run_{ts}"
    os.makedirs(folder, exist_ok=True)

    # Copy report files
    for f in os.listdir("."):
        if f.startswith("final_diagnostic_report") and (f.endswith(".txt") or f.endswith(".html")):
            shutil.copy(f, os.path.join(folder, f))

    # Copy logs
    if os.path.exists("logs"):
        for f in os.listdir("logs"):
            shutil.copy(os.path.join("logs", f), os.path.join(folder, f))

    # Create ZIP
    zipname = f"{folder}.zip"
    with zipfile.ZipFile(zipname, 'w') as z:
        for root, _, files in os.walk(folder):
            for file in files:
                z.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder))

    print(f"[✅] Archived to {zipname}")

if __name__ == "__main__":
    archive_logs()
