#!/usr/bin/env python3
"""
Redis Debug Test Script

[역할]
Redis Streams 신호 발행 기능을 디버깅하는 테스트 스크립트입니다.
직접 Redis 연결 및 SignalPublisher를 테스트하여 문제를 진단합니다.

[주요 테스트 항목]
1. 직접 Redis 연결 테스트
   - upstash-redis 클라이언트 직접 사용
   - xadd 명령어 직접 테스트
2. SignalPublisher 테스트
   - SignalPublisher 클래스를 통한 신호 발행
   - 매수 신호 발행 테스트

[실행 방법]
    python test_debug_redis.py

[필수 환경변수]
- UPSTASH_REDIS_REST_URL: Redis REST API URL
- UPSTASH_REDIS_REST_TOKEN: Redis REST API Token

[사용 시나리오]
- Redis 연결 문제 진단
- SignalPublisher 동작 확인
- xadd 명령어 동작 확인
"""
import os
import json
import asyncio
from pathlib import Path

# .env 로드
from dotenv import load_dotenv
load_dotenv(Path('.env'))

print('=== Debug Test ===')

from upstash_redis import Redis
from messaging.redis_signal_publisher import SignalPublisher

# Redis 직접 테스트
redis = Redis(
    url=os.environ['UPSTASH_REDIS_REST_URL'],
    token=os.environ['UPSTASH_REDIS_REST_TOKEN']
)

# xadd 직접 테스트
print('Testing direct xadd...')
try:
    result = redis.xadd('prism:trading-signals', {'data': json.dumps({'test': 'direct_test'})})
    print(f'Direct xadd result: {result}')
    print(f'Result type: {type(result)}')
except Exception as e:
    import traceback
    print(f'Direct xadd error: {type(e).__name__}: {e}')
    traceback.print_exc()

# SignalPublisher 테스트
publisher = SignalPublisher()
publisher._redis = redis
print(f'Publisher _redis is set: {publisher._is_connected()}')

async def test_publish():
    print('Testing publisher...')
    try:
        result = await publisher.publish_buy_signal(
            ticker='TEST001',
            company_name='테스트',
            price=10000
        )
        print(f'Publisher result: {result}')
        print(f'Result type: {type(result)}')
    except Exception as e:
        import traceback
        print(f'Publisher error: {type(e).__name__}: {e}')
        traceback.print_exc()

asyncio.run(test_publish())
print('=== Done ===')
