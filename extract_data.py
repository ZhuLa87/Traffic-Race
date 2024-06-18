import os
import xml.etree.ElementTree as ET
import json

namespace = {'ns': 'http://traffic.transportdata.tw/standard/traffic/schema/'}

print(f'Processing...')

def extract(download_dir, section_id='0019', output_file='data.json'):

    # 如果文件存在，則讀取结果列表
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as json_file:
            results = json.load(json_file)
    else:
        # 否則建立空的結果列表
        results = []
    
    for file_name in os.listdir(download_dir):
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

                    result = {
                        'TravelTime': travel_time,
                        'TravelSpeed': travel_speed,
                        'DataCollectTime': data_collect_time
                    }

                    results.append(result)
                    break

        except ET.ParseError as e:
            print(f'Failed to parse {file_path}: {e}')

    # save the resault into file
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)

    print(f"Data extracted and saved to {output_file}")
