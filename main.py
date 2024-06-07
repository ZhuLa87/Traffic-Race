import os
import requests
import gzip
import shutil

download_dir = 'files'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# download and extract
def download_file(url, download_dir):
    filename = url.split('/')[-1]
    filepath = os.path.join(download_dir, filename)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')

        with gzip.open(filepath, 'rb') as f_in:
            with open(filepath[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f'Extracted {filename[:-3]}')

        os.remove(filepath)
    else:
        print(f'Failed to download {filename}')

base_url = 'https://tisvcloud.freeway.gov.tw/history/motc20/Section/20240607/LiveTraffic_'


for i in range(10):
    file_number = str(i).zfill(4)
    file_url = f'{base_url}{file_number}.xml.gz'
    download_file(file_url, download_dir)