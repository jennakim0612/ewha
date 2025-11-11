import matplotlib.pyplot as plt
import numpy as np

# 사용자에게 입력받기
n = int(input("금융 상품 개수를 입력하세요: "))

products = {}
for _ in range(n):
    name = input("상품 이름을 입력하세요: ")
    rate = float(input(f"{name}의 명목 이자율을 입력하세요 (예: 5 for 5%): ")) / 100
    products[name] = rate

# 물가상승률 범위 입력 (예: 0~10%)
min_infl = float(input("물가상승률 범위 시작값을 입력하세요 (예: 0): ")) / 100
max_infl = float(input("물가상승률 범위 끝값을 입력하세요 (예: 10): ")) / 100

# 물가상승률 범위 설정
inflation_rates = np.linspace(min_infl, max_infl, 100)

# 실질 이자율 함수
def real_interest_rate(nominal, inflation):
    return (1 + nominal) / (1 + inflation) - 1

# 그래프 설정
plt.figure(figsize=(10, 6))

# 상품별 실질 이자율 그래프 그리기
for name, rate in products.items():
    real_rates = real_interest_rate(rate, inflation_rates)
    plt.plot(inflation_rates * 100, real_rates * 100, label=f"{name} (명목 {rate*100:.1f}%)")

# 그래프 꾸미기
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.title("물가상승률에 따른 금융상품 실질 수익률 비교")
plt.xlabel("물가상승률 (%)")
plt.ylabel("실질 수익률 (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# 출력
plt.show()