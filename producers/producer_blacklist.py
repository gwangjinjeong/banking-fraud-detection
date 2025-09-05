from confluent_kafka import Producer
import json
import random
from datetime import datetime

config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'blacklist-producer'
}

p = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f'전송 실패: {err}')
    else:
        print(f'전송 성공: {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

def generate_blacklist_transaction():
    """블랙리스트 시나리오: 블랙리스트에 등록된 사용자/카드/IP를 이용한 거래 생성"""
    
    transaction = {
        "transaction_id": f"TXN_BLACKLIST_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "transaction_time": datetime.now().isoformat(),
        "transaction_amount": random.randint(10000, 100000),
        "user_id": "FRAUD_USER_001",  # 블랙리스트 사용자
        "account_id": "ACC999",  # 블랙리스트 계좌
        "card_number": "4111-1111-1111-1111",  # 블랙리스트 카드
        "merchant_id": f"MERCH00{random.randint(1,4)}",
        "ip_address": "192.168.100.50",  # 블랙리스트 IP
        "channel": "ONLINE",
        "is_fraud": 1  # 사기 거래로 표시
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
    print("블랙리스트 거래 전송 완료")

if __name__ == "__main__":
    print("블랙리스트 거래 시나리오 시작...")
    generate_blacklist_transaction()
    print("완료!")