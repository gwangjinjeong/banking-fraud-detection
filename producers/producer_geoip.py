from confluent_kafka import Producer
import json
import random
from datetime import datetime
from faker import Faker

fake = Faker()

config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'geoip-producer'
}

p = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f'전송 실패: {err}')
    else:
        print(f'전송 성공: {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

def generate_geoip_transaction():
    """GeoIP 시나리오: 해외 IP를 가진 거래 생성"""
    
    transaction = {
        "transaction_id": f"TXN_GEOIP_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "transaction_time": datetime.now().isoformat(),
        "transaction_amount": random.randint(100000, 500000),
        "user_id": fake.uuid4(),
        "account_id": fake.uuid4(),
        "card_number": fake.credit_card_number(),
        "merchant_id": f"MERCH00{random.randint(1,4)}",
        "ip_address": fake.ipv4(private=False),  # 해외 IP 시뮬레이션
        "channel": "ONLINE",
        "is_fraud": 0
    }
    
    # Feature 필드 추가
    for i in range(1, 29):
        transaction[f"feature_{i}"] = random.uniform(-2, 2)
    
    p.produce(
        'transactions',
        key=transaction["user_id"].encode('utf-8'),
        value=json.dumps(transaction).encode('utf-8'),
        callback=delivery_report
    )
    
    p.flush()
    print("GeoIP 거래 전송 완료")

if __name__ == "__main__":
    print("GeoIP 거래 시나리오 시작...")
    generate_geoip_transaction()
    print("완료!")