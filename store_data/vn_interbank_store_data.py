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
        return "uploads/vn_interbank_interest/history.csv"
    else:
        return f"uploads/vn_interbank_interest/{date.strftime('%d-%m-%Y')}.csv"

def get_latest_s3_data(s3_client, bucket_name):
    try:
        # Get the latest file from S3
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix="uploads/vn_interbank_interest/"
        )
        
        if 'Contents' not in response:
            return None
            
        # Sort by last modified date
        latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
        
        # Download the file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            s3_client.download_file(bucket_name, latest_file['Key'], tmp.name)
            df = pd.read_csv(tmp.name)
            os.unlink(tmp.name)
            return df
            
    except Exception as e:
        print(f"Error getting latest S3 data: {str(e)}")
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
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'ap-southeast-1')
        )
        s3 = session.client("s3")
        bucket_name = "yen-vnd-rate-forcast-1205"

        # Get latest data from S3
        latest_s3_data = get_latest_s3_data(s3, bucket_name)
        
        # Read current data
        data_path = "data/cleaned/vn_interbank_interest_clean.csv"
        current_df = pd.read_csv(data_path)
        current_df['date'] = pd.to_datetime(current_df['date'])
        
        if latest_s3_data is not None:
            latest_s3_data['date'] = pd.to_datetime(latest_s3_data['date'])
            latest_date = latest_s3_data['date'].max()
            
            # Only process new data
            new_data = current_df[current_df['date'] > latest_date]
            
            if new_data.empty:
                print("No new data to upload")
                return
                
            print(f"Found new data from {new_data['date'].min()} to {new_data['date'].max()}")
            
            # Process and upload new data
            cutoff_date = datetime(2025, 5, 14)
            historical_data = new_data[new_data['date'].dt.date <= cutoff_date.date()]
            current_data = new_data[new_data['date'].dt.date > cutoff_date.date()]
            
            if not historical_data.empty:
                upload_vn_interbank_data(historical_data, "2025-05-14", s3, bucket_name)
            
            for date, group_df in current_data.groupby(current_data['date'].dt.date):
                date_str = date.strftime("%Y-%m-%d")
                upload_vn_interbank_data(group_df, date_str, s3, bucket_name)
        else:
            # If no data in S3, upload all current data
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
