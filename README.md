# 💰 개인 지출 분석 대시보드 (AI 기반 소비 패턴 분석)

## 📌 프로젝트 소개

본 프로젝트는 개인 지출 데이터를 업로드하면 자동으로 소비 패턴을 분석하고  
카테고리별 지출 비율, 월별 추이, AI 기반 소비 인사이트 및 예산 추천을 제공하는 웹 대시보드입니다.

사용자는 CSV 또는 Excel 파일을 업로드하여 자신의 소비 패턴을 시각적으로 확인하고  
AI 분석을 통해 절약 전략과 다음 달 예산 가이드를 받을 수 있습니다.

---

## 🎯 주요 기능

### 1️⃣ 데이터 업로드
- CSV / Excel 파일 업로드 지원
- UTF-8 / CP949 인코딩 자동 처리

### 2️⃣ 데이터 전처리
- 날짜(datetime) 변환
- 금액 숫자형 변환
- 결측치 제거 및 유효 데이터 필터링

### 3️⃣ 대시보드 시각화
- 📊 KPI 카드 (총 지출, 평균 지출, 최대 지출, 거래 건수)
- 🥧 카테고리별 지출 도넛 차트
- 📈 월별 지출 추이 라인 차트
- 🔎 기간 및 카테고리 필터 기능

### 4️⃣ AI 소비 분석
- OpenAI API 연동
- 소비 패턴 분석
- 절약 가능 영역 제안
- 다음 달 예산 추천

### 5️⃣ 월간 리포트 생성
- 지출 요약 통계 자동 생성
- 카테고리 분석 포함
- AI 인사이트 포함
- Markdown 파일 다운로드 기능

---

## 🛠 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python 3.10 |
| Data Processing | Pandas |
| Visualization | Plotly |
| Web Framework | Streamlit |
| AI | OpenAI API |
| Deployment | Streamlit Cloud |

---

## 🚀 실행 방법

### 1️⃣ 패키지 설치

```bash
pip install -r requirements.txt
```

### 2️⃣ 로컬 실행

```bash
streamlit run app.py
```

---

## 🌍 배포

Streamlit Cloud를 통해 배포 가능합니다.

1. GitHub 저장소에 코드 업로드
2. https://share.streamlit.io 접속
3. Repository 및 app.py 선택
4. Deploy 클릭

---

## 📊 시스템 구조

1. 파일 업로드  
2. 데이터 전처리  
3. KPI 계산  
4. 시각화 생성  
5. AI 분석 실행  
6. 리포트 생성 및 다운로드  

---

## 💡 프로젝트를 통해 배운 점

- Pandas 기반 데이터 전처리 및 집계 로직 설계
- Plotly를 활용한 인터랙티브 데이터 시각화 구현
- Streamlit 기반 웹 애플리케이션 개발 경험
- OpenAI API 연동 및 프롬프트 설계
- 실제 서비스 배포 경험 (Streamlit Cloud)

---

## 🔮 향후 개선 방향

- 소비 패턴 예측 모델 추가 (Machine Learning)
- 고정비 자동 감지 기능
- PDF 리포트 생성 기능 추가
- 자동 카테고리 분류 기능 개선

---

## 👨‍💻 Author

개인 프로젝트 – 데이터 분석 및 AI 기반 웹 대시보드 구현
