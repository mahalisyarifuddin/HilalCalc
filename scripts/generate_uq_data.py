import json
from hijridate import Hijri

def main():
    start_year = 1343
    end_year = 1500
    data = []

    print(f"Generating Umm al-Qura data for {start_year}-{end_year} AH...")

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            try:
                # Get Gregorian date for the 1st of the Hijri month
                h = Hijri(year, month, 1)
                g = h.to_gregorian()
                # Format as YYYY-MM-DD
                g_str = g.isoformat()

                data.append({
                    "y": year,
                    "m": month,
                    "gt": g_str
                })
            except Exception as e:
                print(f"Error for {year}-{month}: {e}")

    with open("data/uq_dates.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated {len(data)} records.")

if __name__ == "__main__":
    main()
