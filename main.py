import os
import requests
import gzip
import shutil
import time
import extract_data
import datetime
import threading

def log_error(message):
    with open("error.log", "a") as error_log:
        error_log.write(f"{datetime.datetime.now()} - {message}\n")

def download_file(url, download_dir, headers, download_date, file_number):
    filename = url.split('/')[-1]
    filepath = os.path.join(download_dir, filename)
    new_filename = f'LiveTraffic_{download_date}_{file_number}.xml'
    extracted_filepath = os.path.join(download_dir, new_filename)

    # check if file already exists
    if os.path.exists(extracted_filepath):
        print(f'Skipping {filename} as it already exists.')
        return

    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_message = f'Failed to download {download_date} | {filename}: {e}'
        print(error_message)
        log_error(error_message)
        return
    
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')

        # 解壓縮
        try:
            with gzip.open(filepath, 'rb') as f_in:
                with open(extracted_filepath, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f'Extracted {filename[:-3]}')

            os.remove(filepath)

            # Rename the extracted file
            new_filename = f'LiveTraffic_{download_date}_{file_number}.xml'
            new_filepath = os.path.join(download_dir, new_filename)
            os.rename(extracted_filepath, new_filepath)
            print(f'Renamed to {new_filename}')
        except Exception as e:
            error_message = f'Failed to extract {filename}: {e}'
            print(error_message)
            log_error(error_message)
    else:
        error_message = f'Failed to download {filename}: HTTP {response.status_code}'
        print(error_message)
        log_error(error_message)
    # time.sleep(5)  # delay

def doanload_concurrently(urls, download_dir, headers, download_date, file_numbers):
    threads = []
    for url, file_number in zip(urls, file_numbers):
        t = threading.Thread(target=download_file, args=(url, download_dir, headers, download_date, file_number))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def main():
    download_dir = 'files'
    download_date_start = '20230101'
    download_date_end = '20231031'
    section_id = '0019'
    output_file = 'data.json'

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    start_date = datetime.datetime.strptime(download_date_start, '%Y%m%d')
    end_date = datetime.datetime.strptime(download_date_end, '%Y%m%d')
    current_date = start_date

    while current_date <= end_date:
        download_date = current_date.strftime('%Y%m%d')
        base_url = f'https://tisvcloud.freeway.gov.tw/history/motc20/Section/{download_date}/LiveTraffic_'

        urls = []
        file_numbers = []
        for hour in range(24):
            for minute in range(60):
                file_number = f'{hour:02}{minute:02}'
                file_url = f'{base_url}{file_number}.xml.gz'
                urls.append(file_url)
                file_numbers.append(file_number)

        # 併發下載
        doanload_concurrently(urls, download_dir, headers, download_date, file_numbers)

        current_date += datetime.timedelta(days=1)

    extract_data.extract(download_dir, section_id, output_file)

if __name__ == "__main__":
    main()
