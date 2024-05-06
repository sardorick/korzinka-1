import pandas as pd
import user_agents


INPUT_FILE = "/Users/szokirov/Documents/GitHub/korzinka-1/data/clicks.json"
OUTPUT_FILE = "/Users/szokirov/Documents/GitHub/korzinka-1/data/clicks_transformed.csv"  






def transform_data():
    df = pd.read_json(INPUT_FILE)
    df = df.join(pd.json_normalize(df.pop('data')))  

    # Convert the time stamp to correct type
    df['click_timestamp'] = df['click_timestamp'].astype(int) 
    df['click_datetime'] = pd.to_datetime(df['click_timestamp'], unit='s') 
    # Extract date and time to individual columns
    df['click_date'] = df['click_datetime'].dt.date
    df['click_time'] = df['click_datetime'].dt.time

    # Parse the user agent in columns
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


    # Standarized publishers
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


    # Save the transformed file into a CSV
    df.to_csv(OUTPUT_FILE, index=False) 


if __name__ == "__main__":
    transform_data()

