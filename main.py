# Add to main.py after extract_phones()
print("\n5. Cleaning old leads (removing ads older than 2 weeks)...")
from scripts.export_for_web import export_to_json
export_to_json(max_age_weeks=2)
