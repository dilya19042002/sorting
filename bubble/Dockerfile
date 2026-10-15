# 파이썬 공식 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 라이브러리 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run PORT 환경변수를 사용하며 app.py 안의 Flask 인스턴스(app) 실행
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
