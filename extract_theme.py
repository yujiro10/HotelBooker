from pathlib import Path
from zipfile import ZipFile

zip_path = Path(r"C:\Users\yujiro_\Desktop\hotelier-1.0.0.zip")
dest = Path(r"C:\Users\yujiro_\.cursor\projects\empty-window\imported_theme")
dest.mkdir(parents=True, exist_ok=True)

with ZipFile(zip_path, "r") as zf:
    zf.extractall(dest)
    (dest.parent / "theme_manifest.txt").write_text("\n".join(zf.namelist()), encoding="utf-8")
