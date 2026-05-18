# Kiwoom Auto Trading (Mock/Live)

키움증권 REST/WebSocket 기반 자동매매 기본 골격입니다.

## 특징
- 모의투자/실전투자 모드 전환 지원
- 앱키/시크릿키 GUI 입력 지원(환경변수 미설정 시)
- 토큰 발급/갱신 클라이언트
- 시세 조회/주문/계좌조회 래퍼
- 단순 전략 + 리스크 체크 + 실행기 분리

## 빠른 시작
1. Python 3.11+
2. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
3. `.env.example`를 복사해 `.env` 작성 (앱키/시크릿키는 비워도 실행 시 GUI로 입력 가능)
4. 실행
   ```bash
   python -m app.main
   ```

## 모드 전환
- `KIWOOM_ENV=mock` : 모의투자
- `KIWOOM_ENV=live` : 실전투자

## 주의
- 실전투자는 반드시 소액/검증된 전략으로 시작하세요.
- 주문 전 리스크 룰을 반드시 점검하세요.
