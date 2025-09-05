from confluent_kafka import Producer
import json
import time
import random
from datetime import datetime

# Kafka 설정
config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'high-freq-producer'
}

p = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f'전송 실패: {err}')
    else:
        print(f'전송 성공: {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

def generate_high_freq_transactions(user_id, count=10):
    """고빈도 거래 시나리오 생성"""
    
    for i in range(count):
        transaction = {
            "transaction_id": f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}",
            "transaction_time": datetime.now().isoformat(),
            "transaction_amount": random.randint(10000, 50000),
            "user_id": user_id,
            "account_id": f"ACC001",
            "card_number": "5234-5678-9012-3456",
            "merchant_id": f"MERCH00{random.randint(1,4)}",
            "ip_address": "192.168.1.100",
            "channel": "ONLINE",
            "is_fraud": 0
        }
        
        # 각 feature 필드 추가 (PCA 변환된 값 시뮬레이션)
        for j in range(1, 29):
            transaction[f"feature_{j}"] = random.uniform(-3, 3)
        
        # 동일 user_id를 키로 사용하여 같은 파티션으로 전송
        p.produce(
            'transactions',
            key=user_id.encode('utf-8'),
            value=json.dumps(transaction).encode('utf-8'),
            callback=delivery_report
        )
        
        # 짧은 간격으로 전송 (고빈도 시뮬레이션)
        time.sleep(0.5)
    
    p.flush()
    print(f"{user_id}의 고빈도 거래 {count}건 전송 완료")

if __name__ == "__main__":
    print("고빈도 거래 시나리오 시작...")
    generate_high_freq_transactions("USER_HIGH_FREQ_001", 10)
    print("완료!")