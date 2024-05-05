import pandas as pd
import user_agents
import ipinfo  
from dotenv import load_dotenv
import os
import requests
import socket



INPUT_FILE = "data/clicks.json"
OUTPUT_FILE = "data/clicks_transformed.csv"  

#Load .env (Pushed to repo for display reasons, but it is not supposed to be pushed to repo)
load_dotenv()


# IPINFO_ACCESS_TOKEN = os.getenv('IPINFO_TOKEN')
IPINFO_ACCESS_TOKEN = 'ec5991895d7c1f'
handler = ipinfo.getHandler(IPINFO_ACCESS_TOKEN)

def transform_data():
    df = pd.read_json(INPUT_FILE)
    df = df.join(pd.json_normalize(df.pop('data')))  

    df['click_timestamp'] = df['click_timestamp'].astype(int) 
    df['click_datetime'] = pd.to_datetime(df['click_timestamp'], unit='s') 
    df['click_date'] = df['click_datetime'].dt.date
    df['click_time'] = df['click_datetime'].dt.time

    def parse_user_agent(ua_string):
        ua = user_agents.parse(ua_string)
        return pd.Series([ua.os.family, ua.os.version_string, ua.browser.family, ua.browser.version_string, ua.device.family], 
                     index=['os_name_from_ua', 'os_version_from_ua', 'browser_from_ua', 'browser_version_from_ua', 'device_type_from_ua']) 

    temp_df = df['click_user_agent'].apply(parse_user_agent)
    temp_df.columns = ['os_name', 'os_version', 'browser', 'browser_version', 'device_type']

    # print(df.columns)  
    # print(temp_df.columns)
    df = df.drop(['os_name', 'os_version', 'device_type'], axis=1)
    df = df.join(temp_df) 

    # # Get geodata using IP Adress. 
    # def extract_ipv4(ip_string):
    #     if ip_string.startswith('::ffff:'):
    #         return ip_string[7:]  # Extract the IPv4 part
    #     else:
    #         return ip_string 

    # # Assumption for this data is that it can be used to track user activity based on their map location and improvements can be made in marketing, for example
    # def get_geo_data(ip_address):
    #     try:
    #         response = requests.get(f"https://ipinfo.io/{ip_address}?token={IPINFO_ACCESS_TOKEN}")
    #         response.raise_for_status()  
    #         data = response.json()
    #         return data.get('latitude'), data.get('longitude'), data.get('region') 
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error processing IP: {ip_address}. Error: {e}")
    #         return None, None, None 

    # df['ipv4'] = df['click_ipv6'].apply(extract_ipv4)
    # df[['latitude', 'longitude', 'region']] = df['ipv4'].apply(get_geo_data) 
    # df.fillna(method='ffill', inplace=True) 


    def categorize_publisher(publisher_name):
        if 'Korzinka' in publisher_name:
            return 'Korzinka'
        elif 'Lebazar_old_app' in publisher_name:
            return 'Online Old App'
        elif 'Рефералки' in publisher_name:
            return 'Referrals'
        elif 'SMM Korzinka Go' in publisher_name:
            return 'Social Media KGO'
        elif 'Охватка' in publisher_name:
            return 'Social Media clicks'
        elif 'Lebazar_media' in publisher_name:
            return 'App Media'
        else:
            return 'Other'



    df['publisher_category'] = df['publisher_name'].apply(categorize_publisher)

    # Normalization
    df['device_model'] = df['device_model'].str.lower().str.replace('galaxy ', '') 
    df['city'] = df['city'].str.replace('Tashkent city', 'Tashkent')


    df.to_csv(OUTPUT_FILE, index=False) 


if __name__ == "__main__":
    transform_data()

