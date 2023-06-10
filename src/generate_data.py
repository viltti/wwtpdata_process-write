import os
import sys
import time
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

'''

Here we use a Wastewater treatment plant dataset as a base. We interpolate the data such that 
we get 10 minute intervals instead of 1 day. 

Our methods do not account for the complex relationships between the features at all.
We basically just add some noise so that plotting the signal would somewhat look like real data.
The main goal of this is to get data that mimics real world data "well enough" for the purpose of testing data pipelines etc.

'''

def process_and_write_to_db():
    
    # timing
    start_time = time.time()

    try:
        data_path = os.environ['DATA_PATH']
        # straight from the notebook
        df_original = pd.read_csv(data_path)
        df_original['date'] = pd.to_datetime(df_original[['year', 'month', 'day']])
        df_original.set_index('date', inplace=True)
        df_original.drop(['year', 'month', 'day'], axis=1, inplace=True)
        df_resampled = df_original.resample('10T').asfreq()
        df_resampled = df_resampled.ffill()
        np.random.seed(0) 
        noise = np.random.normal(0, 0.03, df_resampled.shape)
        df_noisy = df_resampled + df_resampled * noise
        df_noisy.index = df_resampled.index
        df_last_month = df_noisy[df_noisy.index.month == df_noisy.index[-1].month]
        df_last_month.index = pd.date_range(start='2023-06-10 22:00:00', periods=len(df_last_month), freq='10T')
        modified_sensor_data = df_last_month

    except Exception as e:
        print(f"Data processing failed with error: {e}")
        return False

    try:
        # database connection
        DB_URL = os.environ['DB_URL']
        engine = create_engine(DB_URL)

        # write the DataFrame to a table in SQL database
        modified_sensor_data.to_sql('wwtp_data', engine, if_exists='append')
        print('ready')

    except Exception as e:
        print(f"Writing to database failed with error: {e}")
        return False
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    data_size_MB = sys.getsizeof(modified_sensor_data) / (1024 * 1024)
    print(f"Data processed and written successfully. Wrote approximately {data_size_MB:.2f} MB ({len(modified_sensor_data)} records) in {elapsed_time:.2f} seconds.")

    return True


if __name__ == "__main__":

    load_dotenv()
    if process_and_write_to_db():
        print('exiting...')
    else:
        print('Failed')
  