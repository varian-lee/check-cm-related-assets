# check-cm-related-assets

Datadog UI에서 Metrics - Volumes 에서 Top 500 Metric 들을 가져와서 csv로 다운로드 하고,
해당 csv 파일을 읽고 Datadog Dashboard/Monitor 등의 Asset 이 있는지 확인하는 스크립트

```
# 아래와 같이 준비
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install pandas requests datadog-api-client urllib3

# 아래 명령어로 스크립트 실행
(venv) $ python check_related_metrics.py
(venv) $ DD_SITE="datadoghq.com" DD_API_KEY="xxxx" DD_APP_KEY="xxxx" python check_related_metrics.py
```
