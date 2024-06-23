# 如何使用

編輯 `download_date_start` 和 `download_date_end` 想要下載的起始日期和最終日期

執行
```bash
python main.py
```
> 如過程中遇到問題請查看 `error.log`

# 輸出資料格式說明(data.json)

這個 JSON 結構包含了有關通過時間、通過速度和數據收集時間的相關資訊。以下是各個字段的詳細說明：

1. **TravelTime** (string)
    - **描述**: 通過時間，以秒為單位表示。
    - **範例**: "248"

2. **TravelSpeed** (string)
    - **描述**: 通過速度，以公里每小時（km/h）表示。
    - **範例**: "92"

3. **DataCollectTime** (string)
    - **描述**: 數據收集的時間，格式為 ISO 8601 標準。
    - **格式**: YYYY-MM-DDTHH:MM:SS+TZD
        - YYYY: 四位數字年份
        - MM: 兩位數字月份（01-12）
        - DD: 兩位數字日期（01-31）
        - T: 日期與時間之間的分隔符
        - HH: 兩位數字小時（00-23）
        - MM: 兩位數字分鐘（00-59）
        - SS: 兩位數字秒（00-59）
        - TZD: 時區設置（例如 +08:00 表示東八區）
    - **範例**: "2023-10-31T23:58:00+08:00"

4. **DataCollectTimestamp** (string)
    - **描述**: 數據收集的 UNIX 時間戳，從1970年1月1日00:00:00 UTC到數據收集時的秒數。
    - **範例**: "1698767880"

## JSON 結構範例

```json
{
    "TravelTime": "248",
    "TravelSpeed": "92",
    "DataCollectTime": "2023-10-31T23:58:00+08:00",
    "DataCollectTimestamp": "1698767880"
}
