from confluent_kafka import Producer
import json
import time
import random
from datetime import datetime
from faker import Faker

fake = Faker()

# Kafka 설정
config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'normal-producer'
}

p = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f'전송 실패: {err}')
    else:
        print(f'전송 성공: {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

def generate_transaction(user_id=None):
    """정상 거래 시나리오 생성"""
    if user_id is None:
        user_id = fake.uuid4()

    transaction = {
        "transaction_id": f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(0, 999)}",
        "transaction_time": datetime.now().isoformat(),
        "transaction_amount": random.randint(1000, 100000),
        "user_id": user_id,
        "account_id": fake.uuid4(),
        "card_number": fake.credit_card_number(),
        "merchant_id": f"MERCH00{random.randint(1,4)}",
        "ip_address": fake.ipv4(),
        "channel": random.choice(["ONLINE", "OFFLINE", "MOBILE"]),
        "is_fraud": 0
    }
    
    # 각 feature 필드 추가 (PCA 변환된 값 시뮬레이션)
    for i in range(1, 29):
        transaction[f"feature_{i}"] = random.uniform(-1, 1)
    
    p.produce(
        'transactions',
        key=user_id.encode('utf-8'),
        value=json.dumps(transaction).encode('utf-8'),
        callback=delivery_report
    )
    
    p.flush()
    print(f"정상 거래 전송 완료: {transaction['transaction_id']}")

if __name__ == "__main__":
    print("정상 거래 시나리오 시작...")
    for _ in range(5):
        generate_transaction()
        time.sleep(1)
    print("완료!")