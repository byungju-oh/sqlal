# 베이스 이미지 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 환경 변수 설정
ENV FLASK_ENV=production
ENV DATABASE_URI=mysql+mysqlconnector://ubu:pwd@ip/dba
ENV SECRET_KEY=your_secret_key
ENV FLASK_DEBUG=False
# 애플리케이션 실행
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
