<h1>Banking Fraud Detection – 실시간 이상거래 탐지 파이프라인</h1>

  <!-- Core Technologies -->
  [![Kafka](https://img.shields.io/badge/streaming_platform-kafka-black.svg?style=flat-square)](https://kafka.apache.org)
  [![Docker](https://img.shields.io/badge/docker-compose-blue.svg?style=flat-square)](https://docs.docker.com/compose/)
  [![Elasticsearch](https://img.shields.io/badge/search-elasticsearch-yellow.svg?style=flat-square)](https://www.elastic.co/elasticsearch/)
  [![Logstash](https://img.shields.io/badge/data_processing-logstash-4CAF50.svg?style=flat-square)](https://www.elastic.co/logstash)
  [![Filebeat](https://img.shields.io/badge/log_shipper-filebeat-2196F3.svg?style=flat-square)](https://www.elastic.co/beats/filebeat)
  [![Redis](https://img.shields.io/badge/cache-redis-DC382D.svg?style=flat-square)](https://redis.io)
  [![MariaDB](https://img.shields.io/badge/database-mariadb-003545.svg?style=flat-square)](https://mariadb.org)
  [![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=flat-square)](https://www.python.org)

## 레파짓토리 설명
이 저장소는 **Docker Compose 기반**으로 **실시간 이상거래 탐지(FDS, Fraud Detection System)** 파이프라인을 구축한 오픈소스 예제입니다.  

여기서 다루는 기능:
- Kafka → Logstash → Elasticsearch → Kibana/Grafana
- MariaDB (계정계 / FDS DB) 및 Redis 기반 데이터 강화
- 정상 거래, 고빈도 거래, 블랙리스트, 휴면계좌 등 **실습 시나리오 코드 포함**
- 금융 보안(FinSec) 환경에서 재사용 가능 아키텍처

## 문제 정의

신용카드 혹은 계좌를 이용한 온라인 거래는 매 순간 사기 위험에 노출됩니다.  
은행/전자금융사는 거래가 발생할 때마다 즉시 검증해야 합니다:

1. **거래 데이터 수집** (Kafka, TCP, 로그 파일 등)
2. **데이터 강화** (블랙리스트 조회, Redis 카운터, GeoIP)
3. **ML 모델 적용** (Autoencoder, Anomaly Detection 등)
4. **실시간 분석 및 알림**

문제는, 이런 시스템을 **엔드-투-엔드로 구성**하는 것이 복잡하다는 점입니다.

## 솔루션 개요

이 저장소는 **은행/전자금융 환경에서 사용 가능한 오픈소스 FDS 파이프라인**을 제공합니다.

- **다중 입력 경로**: Kafka, Filebeat, TCP
- **DB 이중화**: 계정계(MariaDB) + FDS 전용 DB
- **실시간 Redis 카운터**: 사용자별 빈도/금액 추적
- **Elasticsearch 3노드 클러스터**: 고가용성 보장
- **시각화/모니터링**: Kibana(분석), Grafana(운영)

## 아키텍처 
<img width="500"  alt="Mermaid Chart-2025-09-05-061057" src="https://github.com/user-attachments/assets/639c025a-265f-4b45-9b8a-d71d15a71f1b" />

## 프로젝트 구조
```
fds-pipeline-project/
├── docker-compose.yml                     # 모든 서비스 정의 및 오케스트레이션
│
├── config/
│   ├── init-account-db.sql               # 계정계 MariaDB 초기화 스크립트
│   ├── init-fds-db.sql                   # FDS MariaDB 초기화 스크립트
│   └── mysql-connector-j-8.0.33.jar      # Logstash JDBC 드라이버
│
├── logstash/
│   ├── pipelines.yml                     # 다중 파이프라인 구성
│   └── pipeline/
│       ├── 10_input_kafka.conf           # Kafka 입력 파이프라인
│       ├── 11_input_beats.conf           # Filebeat 입력 파이프라인
│       ├── 12_input_tcp.conf             # TCP 입력 파이프라인
│       └── 30_process_enrich.conf        # 데이터 처리/강화 파이프라인
│
├── filebeat/
│   └── filebeat.yml                      # Docker 컨테이너 로그 수집 설정
│
├── producers/
│   ├── Dockerfile                        # Python 프로듀서 컨테이너
│   ├── requirements.txt                  # Python 의존성
│   ├── producer_normal.py                # 정상 거래 시나리오
│   ├── producer_high_freq.py             # 고빈도 거래 시나리오
│   ├── producer_blacklist.py             # 블랙리스트 시나리오
│   ├── producer_dormant.py               # 휴면계좌 시나리오
│   ├── producer_geoip.py                 # GeoIP 시나리오
│   └── tcp_legacy_sender.py              # 레거시 시스템 TCP 전송
│
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml            # Elasticsearch 데이터소스
│       └── dashboards/
│           ├── dashboard.yml              # 대시보드 프로비저닝
│           ├── FDS_Analytics.json        # FDS 분석 대시보드
│           └── System_Monitoring.json    # 시스템 모니터링 대시보드
│
└── data/
    └── GeoLite2-City.mmdb                # GeoIP 데이터베이스 (옵션)
```

## 실습 단계
### 1. 환경 준비
```bash
git clone https://github.com/your-org/banking-fraud-detection.git
cd banking-fraud-detection
docker-compose up -d
```

### 2. Kafka 토픽 생성
```bash
docker exec -it kafka kafka-topics --create \
  --topic transactions \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

### 3. 거래 데이터 프로듀서 실행
```bash
docker exec producer python producers/producer_normal.py
docker exec producer python producers/producer_high_freq.py
```

### 4. Logstash 데이터 처리 및 강화
- 블랙리스트 조회 (MariaDB FDS)
- 계정 상태 확인 (MariaDB 계정계)
- Redis 카운터 기반 빈도 탐지
- GeoIP 위치 정보 추가

### 5. Elasticsearch 저장 및 조회
```bash
curl -X GET "localhost:9200/transactions-*/_search?pretty"
```

### 6. Kibana/Grafana 시각화
- Kibana: http://localhost:5601
- Grafana: http://localhost:3000 (기본 계정 admin/admin)

### 7. 통합 테스트
- 정상 거래: risk_level=NORMAL
- 고빈도 거래: risk_level=HIGH
- 휴면계좌: risk_level=CRITICAL


## 실습 시나리오
다양한 거래 패턴을 시뮬레이션할 수 있도록 **Kafka Producer** 및 **TCP Sender** 스크립트를 제공합니다.  
1. 정상 거래 (normal transcation): 정상적인 일반 거래 `producers/producer_normal.py`
1. 고빈도 거래 (High Frequency): 1분 내 다수 거래 발생 `producers/producer_high_freq.py`
2. 휴면 계좌 (Dormant Account): 장기간 거래 없는 계좌에서 대규모 거래 `producers/producer_dormant.py`
3. 블랙리스트 거래: 위험 사용자/계좌/카드/IP `producers/producer_blacklist.py`
4. GeoIP 테스트 시나리오 `producers/producer_geoip.py`
5. 레거시 TCP 연동: CSV over TCP 데이터 수집 `producers/tcp_legacy_sender.py`

