import socket
import time
from datetime import datetime

def send_legacy_transaction(host='logstash', port=5000):
    """레거시 시스템의 TCP 전송 시뮬레이션"""
    
    # CSV 형식의 거래 데이터
    transactions = [
        f"LEG001,USER001,ACC001,150000,MERCH001,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"LEG002,USER002,ACC002,75000,MERCH003,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"LEG003,USER004,ACC004,2500000,MERCH002,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    try:
        # TCP 소켓 연결
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            
            for tx in transactions:
                # 각 거래를 줄바꿈 문자와 함께 전송
                s.send((tx + '\n').encode('utf-8'))
                print(f"전송: {tx}")
                time.sleep(1)
            
            print("레거시 거래 데이터 전송 완료")
    
    except Exception as e:
        print(f"전송 실패: {e}")

if __name__ == "__main__":
    print("레거시 시스템 TCP 전송 시작...")
    send_legacy_transaction()
