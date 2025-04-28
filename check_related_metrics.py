import requests
import pandas as pd
import time

# Datadog UI에서 top Custom Metric을 CSV로 다운로드
# CSV에서 metric ID 불러오기
input_csv = "extracted-custom-metrics-xxx-xxx.csv"  # ← 파일명으로 교체
df_input = pd.read_csv(input_csv)


# 컬럼 이름 통일
df_input.columns = [col.strip() for col in df_input.columns]
metric_ids = df_input["Metric Name"].dropna().unique().tolist()


# Request 보내기 위한 설정
BASE_URL = "https://api.datadoghq.com/api/v2/metrics/{}/assets"
# HEADERS = {
#   ...
# }

results = []


for metric_id in metric_ids:
    url = BASE_URL.format(metric_id)
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch for {metric_id} - {response.status_code}")
        continue

    data = response.json()
    relationships = data.get("data", {}).get("relationships", {})

    # Est. Custom Metric 값 추출
    est_custom = df_input[df_input["Metric Name"] == metric_id]["Est. Custom Metrics"].values
    est_custom_metric = int(est_custom[0]) if len(est_custom) > 0 and pd.notna(est_custom[0]) else 0
    
    row = {
        "metric_id": metric_id,
        "est_custom_metric": est_custom_metric,
        "dashboards": len(relationships.get("dashboards", {}).get("data", [])),
        "monitors": len(relationships.get("monitors", {}).get("data", [])),
        "notebooks": len(relationships.get("notebooks", {}).get("data", [])),
        "slos": len(relationships.get("slos", {}).get("data", []))
    }

    results.append(row)

    # 0.2초 쉬기 (rate limit 보호)
    time.sleep(0.2)

# 결과를 pandas DataFrame으로 변환
df_result = pd.DataFrame(results)
df_result.to_csv("datadog_metric_assets_summary.csv", index=False)


print("완료: datadog_metric_assets_summary.csv 저장됨")

