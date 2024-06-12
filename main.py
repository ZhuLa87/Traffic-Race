import os
import requests
import gzip
import shutil
import time
import extract_data

def download_file(url, download_dir, headers):
    filename = url.split('/')[-1]
    filepath = os.path.join(download_dir, filename)
    extracted_filepath = filepath[:-3]

    # check if file already exists
    if os.path.exists(extracted_filepath):
        print(f'Skipping {filename} as it already exists.')
        return

    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Fail to download {filename}: {e}')
        return
    
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')

        try:
            with gzip.open(filepath, 'rb') as f_in:
                with open(filepath[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f'Extracted {filename[:-3]}')

            os.remove(filepath)
        except Exception as e:
            print(f'Failed to extract {filename}: {e}')
    else:
        print(f'Failed to download {filename}: HTTP {response.status_code}')
    time.sleep(5)  # delay

def main():
    download_dir = 'files'
    base_url = 'https://tisvcloud.freeway.gov.tw/history/motc20/Section/20240606/LiveTraffic_'
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

    for hour in range(24):
        for minute in range(60):
            file_number = f'{hour:02}{minute:02}'
            file_url = f'{base_url}{file_number}.xml.gz'
            download_file(file_url, download_dir, headers)

    extract_data.extract(download_dir, section_id, output_file)

if __name__ == "__main__":
    main()
