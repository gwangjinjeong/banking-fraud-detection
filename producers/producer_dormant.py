from confluent_kafka import Producer
import json
import random
from datetime import datetime

config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'dormant-producer'
}

p = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f'전송 실패: {err}')
    else:
        print(f'전송 성공: {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

def generate_dormant_account_transaction():
    """휴면 계좌 거래 시나리오"""
    
    transaction = {
        "transaction_id": f"TXN_DORMANT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "transaction_time": datetime.now().isoformat(),
        "transaction_amount": 3000000,  # 큰 금액
        "user_id": "USER003",  # 휴면 계좌 소유자
        "account_id": "ACC003",  # 휴면 계좌
        "card_number": "6234-5678-9012-3456",
        "merchant_id": "MERCH004",  # 고위험 가맹점
        "ip_address": "203.0.113.25",  # 해외 IP
        "channel": "ONLINE",
        "is_fraud": 0
    }
    
    # Feature 필드 추가
    for i in range(1, 29):
        transaction[f"feature_{i}"] = random.uniform(-2, 2)
    
    p.produce(
        'transactions',
        key="USER003".encode('utf-8'),
        value=json.dumps(transaction).encode('utf-8'),
        callback=delivery_report
    )
    
    p.flush()
    print("휴면 계좌 거래 전송 완료")

if __name__ == "__main__":
    print("휴면 계좌 거래 시나리오 시작...")
    generate_dormant_account_transaction()
    print("완료!")