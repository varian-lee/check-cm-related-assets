import requests
import pandas as pd
import time

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi

configuration = Configuration()
configuration.verify_ssl = False 

# 워닝 메세지 보기 싫으면 넣으면 좋음.
import urllib3
urllib3.disable_warnings()

# CSV에서 metric ID 불러오기
input_csv = "extracted-custom-metrics-xxx-xxx.csv"  # ← 파일명으로 교체
df_input = pd.read_csv(input_csv)

# 컬럼 이름 통일
df_input.columns = [col.strip() for col in df_input.columns]
metric_ids = df_input["Metric Name"].dropna().unique().tolist()

results = []

for metric_id in metric_ids:
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.list_metric_assets(
            metric_name=metric_id,
        )

        relationships = response.get("data", {}).get("relationships", {})

        # Est. Custom Metric 값 추출
        est_custom = df_input[df_input["Metric Name"] == metric_id]["Est. Custom Metrics"].values
        est_custom_metric = int(est_custom[0]) if len(est_custom) > 0 and pd.notna(est_custom[0]) else 0
        
        row = {
            "metric_id": metric_id,
            "est_custom_metric": est_custom_metric,
            #"est_custom_ingest_metric": est_custom_ingest_metric,
            "dashboards": len(relationships.get("dashboards", {}).get("data", [])),
            "monitors": len(relationships.get("monitors", {}).get("data", [])),
            "notebooks": len(relationships.get("notebooks", {}).get("data", [])),
            "slos": len(relationships.get("slos", {}).get("data", []))
        }

        results.append(row)

    #0.2초 쉬기 (rate limit 보호)
    time.sleep(0.2)

# 결과를 pandas DataFrame으로 변환
df_result = pd.DataFrame(results)
df_result.to_csv("datadog_metric_assets_summary.csv", index=False)

print("완료: datadog_metric_assets_summary.csv 저장됨")
