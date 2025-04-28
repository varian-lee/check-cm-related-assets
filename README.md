# check-cm-related-assets

Datadog UI에서 Metrics - Volumes 에서 Top Metric 들을 가져와서 csv로 다운로드 하고,
해당 csv 파일을 읽고 Datadog Dashboard/Monitor 등의 Asset 이 있는지 확인하는 스크립트

```
# 아래와 같이 준비
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install pandas requests

# 아래 명령어로 스크립트 실행
$ python check_related_metrics.py
```
