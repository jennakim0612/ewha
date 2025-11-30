import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 이론 그래프 생성 함수
def generate_theoretical_graphs(a, t_exp):
    if t_exp[0] != 0:
        t_exp = t_exp - t_exp[0]

    t_exp = t_exp.astype(np.float64)
    a_th = np.full_like(t_exp, a)
    
    return t_exp, a_th

# 2. CSV/엑셀로부터 측정 데이터 처리 함수
def calculate_velocity(t, a):
    dt = np.diff(t)
    a_avg = (a[:-1] + a[1:]) / 2
    v = np.zeros_like(a)
    v[1:] = np.cumsum(a_avg * dt)
    return v

def process_measured_data(file_path, use_excel=False, t_start=0, t_end=None, normalize_distance=None):
    if use_excel:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    if 'time' not in df.columns or 'acc' not in df.columns:
        raise ValueError("CSV/엑셀 파일에 'time' 또는 'acc' 컬럼이 없습니다.")

    t = df['time'].to_numpy()
    a = df['acc'].to_numpy()

    mask = (t >= t_start) & (t <= (t_end if t_end else t[-1]))
    t = t[mask]
    a = a[mask]

    t = t - t[0]
    v = calculate_velocity(t, a)
    dt = np.diff(t, prepend=t[0])
    s = np.cumsum(v * dt)

    if normalize_distance:
        scale = normalize_distance / s[-1]
        s *= scale
        v *= scale

    return t, a, v, s

# 3. 그래프 그리기 함수 (이론 속도, 거리 제거)
def plot_all(t_th, a_th, t_exp, a_exp, v_exp, s_exp):
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    axs[0].plot(t_exp, a_exp, label='measured a(t)', alpha=0.7)
    axs[0].plot(t_th, a_th, label='theory a(t)')
    
    axs[0].set_ylabel('acc (m/s²)')
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(t_exp, v_exp, label='measured v(t)', alpha=0.7)
    axs[1].set_ylabel('vel (m/s)')
    axs[1].legend()
    axs[1].grid()

    axs[2].plot(t_exp, s_exp, label='measured s(t)', alpha=0.7)
    axs[2].set_xlabel('time (s)')
    axs[2].set_ylabel('dis (m)')
    axs[2].legend()
    axs[2].grid()

    plt.tight_layout()
    plt.show()

# 4. 실행부
if __name__ == "__main__":
    a_theoretical = 9.8
    file_path = "acc_data.csv"
    use_excel = False
    t_start = 0
    t_end = None
    final_distance = 155.0

    t_exp, a_exp, v_exp, s_exp = process_measured_data(
        file_path=file_path,
        use_excel=use_excel,
        t_start=t_start,
        t_end=t_end,
        normalize_distance=final_distance
    )

    t_th, a_th = generate_theoretical_graphs(a=a_theoretical, t_exp=t_exp)

    print("t_exp[:10]:", t_exp[:10])
    print("v_exp[:10]:", v_exp[:10])
    print("v_exp max:", np.max(v_exp))

    plot_all(t_th, a_th, t_exp, a_exp, v_exp, s_exp)
