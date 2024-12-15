# 기본 이미지로 Python 3.8을 사용합니다.
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일들을 컨테이너에 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 작업 디렉토리로 복사
COPY . .

# 포트 8000 열기
EXPOSE 8000

# 컨테이너가 시작될 때 실행될 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

