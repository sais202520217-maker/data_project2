import pandas as pd
import matplotlib.pyplot as plt

# 파일의 실제 컬럼 이름에 맞춰 데이터를 읽어옵니다.
df = pd.read_csv("bcycl_20251221.csv", encoding='cp949')

# 2. 대여 건수 계산하기 (출발 대여소 기준)
# '시작_대여소명'이 같은 것끼리 모아서 '전체_건수'를 더합니다.
rentals = df.groupby('시작_대여소명')['전체_건수'].sum().reset_index()
rentals.columns = ['대여소명', '대여건수']  # 컬럼 이름을 보기 좋게 바꿉니다.

# 3. 반납 건수 계산하기 (도착 대여소 기준)
# '종료_대여소명'이 같은 것끼리 모아서 '전체_건수'를 더합니다.
returns = df.groupby('종료_대여소명')['전체_건수'].sum().reset_index()
returns.columns = ['대여소명', '반납건수']

# 4. 두 데이터 합치기 (대여 + 반납)
# '대여소명'을 기준으로 두 표를 하나로 합칩니다. (빈칸은 0으로 채움)
station_stats = pd.merge(rentals, returns, on='대여소명', how='outer').fillna(0)

# 전처리 결과 확인
print(station_stats.head())

# 1. 총 이용 건수 만들기 (대여 + 반납)
station_stats['총이용건수'] = station_stats['대여건수'] + station_stats['반납건수']

# 2. 이상한 데이터 제거 (건수가 0보다 작은 경우)
# 혹시라도 계산 오류로 음수가 나오면 제거합니다.
station_stats = station_stats[station_stats['총이용건수'] > 0]

print("데이터 준비 완료!")

# 1. 정규화 준비하기 (최대값과 최소값 찾기)
# '총이용건수' 중에서 가장 작은 값(min)과 가장 큰 값(max)을 찾습니다.
min_val = station_stats['총이용건수'].min()
max_val = station_stats['총이용건수'].max()

# 2. 정규화 공식 적용하기 (Min-Max Scaling)
# 공식: (내 점수 - 꼴찌 점수) / (1등 점수 - 꼴찌 점수)
# 이렇게 계산하면 가장 적게 이용된 곳은 0, 가장 많이 이용된 곳은 1이 됩니다.
station_stats['이용건수_정규화'] = (station_stats['총이용건수'] - min_val) / (max_val - min_val)

# 3. 결과 확인하기
# 원래 건수와 0~1로 변한 숫자를 비교해 봅니다.
print(station_stats[['대여소명', '총이용건수', '이용건수_정규화']].head())

# 1. 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')

# 2. 인기 순위 Top 10 뽑기
# 총 이용 건수가 많은 순서대로(ascending=False) 정렬하여 10개만 뽑습니다.
top10 = station_stats.sort_values(by='총이용건수', ascending=False).head(10)

# 3. 그래프 그리기
plt.figure(figsize=(10, 6))  # 도화지 크기
plt.barh(top10['대여소명'], top10['총이용건수'], color='skyblue') # 가로 막대 그리기

plt.title('서울시 따릉이 이용 건수 Top 10 대여소') # 제목
plt.xlabel('총 이용 건수 (회)')  # x축 이름
plt.ylabel('대여소명')           # y축 이름

plt.gca().invert_yaxis()         # 1등이 맨 위에 오도록 뒤집기
plt.grid(axis='x', linestyle='--') # 눈금선 추가
plt.show()
