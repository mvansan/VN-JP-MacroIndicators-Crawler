import boto3
import os
from datetime import datetime
import pandas as pd
import tempfile
import re

def get_s3_key(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    cutoff_date = datetime(2025, 5, 14)
    
    if date <= cutoff_date:
        return "uploads/vn_interbank_interest/history.csv"
    else:
        return f"uploads/vn_interbank_interest/{date.strftime('%d-%m-%Y')}.csv"

def extract_date_from_key(key):
    m = re.search(r'vn_interbank_interest/(\d{2}-\d{2}-\d{4})\\.csv', key)
    if not m:
        m = re.search(r'vn_interbank_interest/(\d{2}-\d{2}-\d{4})\.csv', key)
    if m:
        return datetime.strptime(m.group(1), "%d-%m-%Y")
    return None

def get_latest_cloud_date(s3_client, bucket_name):
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix="uploads/vn_interbank_interest/"
        )
        if 'Contents' not in response:
            return None
        max_date = None
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('history.csv'):
                continue
            date = extract_date_from_key(key)
            if date and (max_date is None or date > max_date):
                max_date = date
        return max_date
    except Exception as e:
        print(f"Error getting latest cloud date: {str(e)}")
        return None

def upload_vn_interbank_data(df, date_str, s3_client, bucket_name):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            df.to_csv(tmp.name, index=False)
            
            s3_key = get_s3_key(date_str)
            
            s3_client.upload_file(tmp.name, bucket_name, s3_key)
            print(f"Successfully uploaded data for {date_str} to s3://{bucket_name}/{s3_key}")
            
        os.unlink(tmp.name)
            
    except Exception as e:
        print(f"Error uploading file for date {date_str}: {str(e)}")
        raise

def process_and_upload_data():
    try:
        session = boto3.Session()
        s3 = session.client("s3")
        bucket_name = "yen-vnd-rate-forcast-1205"
        latest_cloud_date = get_latest_cloud_date(s3, bucket_name)
        data_path = "data/cleaned/vn_interbank_interest_clean.csv"
        current_df = pd.read_csv(data_path)
        current_df['date'] = pd.to_datetime(current_df['date'])
        
        if latest_cloud_date is not None:
            new_data = current_df[current_df['date'] > latest_cloud_date]
            if new_data.empty:
                print("No new data to upload")
                return
            print(f"Found new data from {new_data['date'].min()} to {new_data['date'].max()}")
            cutoff_date = datetime(2025, 5, 14)
            historical_data = new_data[new_data['date'].dt.date <= cutoff_date.date()]
            current_data = new_data[new_data['date'].dt.date > cutoff_date.date()]
            
            if not historical_data.empty:
                upload_vn_interbank_data(historical_data, "2025-05-14", s3, bucket_name)
            
            for date, group_df in current_data.groupby(current_data['date'].dt.date):
                date_str = date.strftime("%Y-%m-%d")
                upload_vn_interbank_data(group_df, date_str, s3, bucket_name)
        else:
            cutoff_date = datetime(2025, 5, 14)
            historical_data = current_df[current_df['date'].dt.date <= cutoff_date.date()]
            current_data = current_df[current_df['date'].dt.date > cutoff_date.date()]
            
            if not historical_data.empty:
                upload_vn_interbank_data(historical_data, "2025-05-14", s3, bucket_name)
            
            for date, group_df in current_data.groupby(current_data['date'].dt.date):
                date_str = date.strftime("%Y-%m-%d")
                upload_vn_interbank_data(group_df, date_str, s3, bucket_name)
            
        print("All data has been processed and uploaded successfully!")
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    process_and_upload_data()
