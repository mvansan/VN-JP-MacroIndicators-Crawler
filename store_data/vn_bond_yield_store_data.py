import boto3
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
import tempfile

load_dotenv()

def get_s3_key(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    cutoff_date = datetime(2025, 5, 14)
    
    if date <= cutoff_date:
        return "uploads/vn_bond_yield/history.csv"
    else:
        return f"uploads/vn_bond_yield/{date.strftime('%d-%m-%Y')}.csv"

def upload_bond_yield_data(df, date_str, s3_client, bucket_name):
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
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'ap-southeast-1')
        )
        s3 = session.client("s3")
        bucket_name = "yen-vnd-rate-forcast-1205"

        data_path = "data/cleaned/vn_bond_yield_cleaned.csv"
        df = pd.read_csv(data_path)
        
        df['date'] = pd.to_datetime(df['date'])
        
        cutoff_date = datetime(2025, 5, 14)
        historical_data = df[df['date'].dt.date <= cutoff_date.date()]
        current_data = df[df['date'].dt.date > cutoff_date.date()]
        
        if not historical_data.empty:
            upload_bond_yield_data(historical_data, "2025-05-14", s3, bucket_name)
        
        for date, group_df in current_data.groupby(current_data['date'].dt.date):
            date_str = date.strftime("%Y-%m-%d")
            upload_bond_yield_data(group_df, date_str, s3, bucket_name)
            
        print("All VN bond yield data has been processed and uploaded successfully!")
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    process_and_upload_data() 