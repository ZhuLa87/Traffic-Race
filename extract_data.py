import os
import xml.etree.ElementTree as ET
import json
import datetime

namespace = {'ns': 'http://traffic.transportdata.tw/standard/traffic/schema/'}

def extract(download_dir, section_id='0019', output_file='data.json'):

    print(f"{datetime.datetime.now()} | Starting extract data...")

    # 如果文件存在且不為空，則讀取结果列表
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, 'r', encoding='utf-8') as json_file:
            results = json.load(json_file)
    else:
        # 否則建立空的結果列表
        results = []
    
    # 遍例所有資料夾中的檔案
    for file_name in os.listdir(download_dir):

        # 若不是.xml結尾則跳過
        if not file_name.endswith('.xml'):
            continue
        
        file_path = os.path.join(download_dir, file_name)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for live_traffic in root.find('ns:LiveTraffics', namespace).findall('ns:LiveTraffic', namespace):
                sid = live_traffic.find('ns:SectionID', namespace).text
                if sid == section_id:
                    travel_time = live_traffic.find('ns:TravelTime', namespace).text
                    travel_speed = live_traffic.find('ns:TravelSpeed', namespace).text
                    data_collect_time = live_traffic.find('ns:DataCollectTime', namespace).text
                    data_collect_timestamp = iso_to_timestamp(data_collect_time)

                    result = {
                        'TravelTime': travel_time,
                        'TravelSpeed': travel_speed,
                        'DataCollectTime': data_collect_time,
                        'DataCollectTimestamp': data_collect_timestamp
                    }

                    results.append(result)
                    break

        except ET.ParseError as e:
            print(f'Failed to parse {file_path}: {e}')

    # save the result into file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)

    print(f"{datetime.datetime.now()} | Data extracted and saved to {output_file}")

def iso_to_timestamp(iso_time):
    dt = datetime.datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S%z")  # 根據 ISO 格式的日期時間字符串解析
    timestamp = str(int(dt.timestamp()))
    return timestamp
    
if __name__ == "__main__":
    extract('files')
