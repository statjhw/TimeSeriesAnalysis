import requests
import pandas as pd
import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

def collect_subway_data(start_year, end_year, line_name, station_name):
    base_url = "http://openapi.seoul.go.kr:8088/{key}/json/CardSubwayStatsNew/1/5/{date}/{line}/{station}"
    
    all_data = []
    
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        
        url = base_url.format(
            key=API_KEY,
            date=date_str,
            line=line_name,
            station=station_name
        )
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if "CardSubwayStatsNew" in data and "row" in data["CardSubwayStatsNew"]:
                rows = data["CardSubwayStatsNew"]["row"]
                for row in rows:
                    all_data.append(row)
            else:
                print(f"No data for {date_str}: {data.get('RESULT', {}).get('MESSAGE', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error fetching {date_str}: {e}")
            
        current_date += datetime.timedelta(days=1)
        # time.sleep(0.05) # Slight delay to be polite, though not strictly necessary for this volume
        
    df = pd.DataFrame(all_data)
    return df

if __name__ == "__main__":
    print("Starting data collection (test run)...")
    # Test with 1 month first
    df = collect_subway_data(2017, 2017, "과천선", "범계")
    # Limit to Jan 2017 for quick test
    df = df[df['USE_YMD'].astype(str).str.startswith('201701')]
    
    if not df.empty:
        output_file = "subway_data_test.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"Data collection complete. Saved {len(df)} rows to {output_file}")
    else:
        print("No data collected.")
