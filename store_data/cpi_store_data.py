import boto3
import os
from datetime import datetime
import pandas as pd
import tempfile
import re

def get_s3_key(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    cutoff_date = datetime(2025, 6, 1)
    
    if date <= cutoff_date:
        return "uploads/cpi_data/history.csv"
    else:
        return f"uploads/cpi_data/{date.strftime('%d-%m-%Y')}.csv"

def extract_month_from_key(key):
    m = re.search(r'cpi_data/(\d{2}-\d{2}-\d{4})\\.csv', key)
    if not m:
        m = re.search(r'cpi_data/(\d{2}-\d{2}-\d{4})\.csv', key)
    if m:
        dt = datetime.strptime(m.group(1), "%d-%m-%Y")
        return dt.replace(day=1)
    return None

def get_latest_cloud_month(s3_client, bucket_name):
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix="uploads/cpi_data/"
        )
        if 'Contents' not in response:
            return None
        max_month = None
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('history.csv'):
                continue
            month = extract_month_from_key(key)
            if month and (max_month is None or month > max_month):
                max_month = month
        return max_month
    except Exception as e:
        print(f"Error getting latest cloud month: {str(e)}")
        return None

def upload_cpi_data(df, date_str, s3_client, bucket_name):
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
        latest_cloud_month = get_latest_cloud_month(s3, bucket_name)
        data_path = "data/cleaned/cpi_data.csv"
        current_df = pd.read_csv(data_path)
        current_df['date'] = pd.to_datetime(current_df['date'])
        current_df['month'] = current_df['date'].dt.to_period('M')
        if latest_cloud_month is not None:
            new_data = current_df[current_df['date'] > latest_cloud_month]
            if new_data.empty:
                print("No new data to upload")
                return
            print(f"Found new data from {new_data['date'].min()} to {new_data['date'].max()}")
            cutoff_date = datetime(2025, 6, 1)
            historical_data = new_data[new_data['date'].dt.date <= cutoff_date.date()]
            current_data = new_data[new_data['date'].dt.date > cutoff_date.date()]
            if not historical_data.empty:
                upload_cpi_data(historical_data, "2025-06-01", s3, bucket_name)
            for date, group_df in current_data.groupby(current_data['date'].dt.date):
                date_str = date.strftime("%Y-%m-%d")
                upload_cpi_data(group_df, date_str, s3, bucket_name)
        else:
            cutoff_date = datetime(2025, 6, 1)
            historical_data = current_df[current_df['date'].dt.date <= cutoff_date.date()]
            current_data = current_df[current_df['date'].dt.date > cutoff_date.date()]
            if not historical_data.empty:
                upload_cpi_data(historical_data, "2025-06-01", s3, bucket_name)
            for date, group_df in current_data.groupby(current_data['date'].dt.date):
                date_str = date.strftime("%Y-%m-%d")
                upload_cpi_data(group_df, date_str, s3, bucket_name)
        print("All CPI data has been processed and uploaded successfully!")
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    process_and_upload_data() 