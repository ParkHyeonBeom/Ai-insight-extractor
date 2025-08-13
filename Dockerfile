# 1. 베이스 이미지 설정
FROM python:3.9-slim

# 2. 컨테이너 내 작업 디렉토리 설정 (가장 중요한 부분!)
# 'core'가 아닌 'app'으로 통일해서 혼란을 방지합니다.
WORKDIR /app

# 3. 파이썬 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. requirements.txt 파일을 현재 작업 디렉토리('/app')로 복사
COPY requirements.txt .

# 5. pip 업그레이드 및 requirements.txt에 명시된 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6. 로컬 프로젝트 폴더의 모든 파일을 현재 작업 디렉토리('/app')로 복사
COPY . .