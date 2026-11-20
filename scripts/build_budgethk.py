import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vQhfgdQ5ZWQep_9YgdI_ieu90KIMWHzGu31xN5xBGyY12-jv_nvzo6"
    "GX4JTXEl3KSqFuQWKHSg-bO5D/pub?gid=2112607594&single=true&output=csv"
)

request = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(request, timeout=60) as response:
    csv_text = response.read().decode("utf-8-sig")

rows = list(csv.DictReader(io.StringIO(csv_text)))

Path("docs").mkdir(exist_ok=True)

payload = {
    "source_url": SOURCE_URL,
    "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
    "row_count": len(rows),
    "rows": rows,
}

with open("docs/budgethk.json", "w", encoding="utf-8") as file:
    json.dump(payload, file, ensure_ascii=False, separators=(",", ":"))
