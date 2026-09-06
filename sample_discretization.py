import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox, Button

# パラメータ
Ts = 0.001    # サンプリング周期[s]
omega = 500   # ローパスフィルタカットオフ周波数[rad/s](初期値:500)

t_start = 0.000     # シミュレーション開始時間[s]
t_final = 0.050     # シミュレーション最大時間[s]
dt = 5e-5           # ソルバー時間刻み幅[s](=0.05[ms])

step_analog = int(t_final/dt)       # ステップ数(連続時間シミュレーション)
step_digital = int(t_final/Ts)      # ステップ数(離散時間シミュレーション)

# 時間データの生成
t_analog = np.arange(t_start, t_final, dt)      # 連続時間データの生成
t_digital = np.arange(t_start, t_final, Ts)     # 離散時間データの生成

# 状態変数データの初期化
x_analog = np.zeros((step_analog, 1))           # 連続時間状態変数データ[ステップ数 x 1]
x_digital_fw = np.zeros((step_digital, 1))      # 離散時間状態変数データ(前進差分)[ステップ数 x 1]
x_digital_bw = np.zeros((step_digital, 1))      # 離散時間状態変数データ(後退差分)[ステップ数 x 1]

def sys_calc(x, u):
    """状態方程式 dx/dt = A@x + B@u 計算"""
    A = np.array([-omega])
    B = np.array([omega])
    return A @ x + B @ u

def solve_rk4(sys_func, x, u, dt):
    """4次ルンゲ・クッタ法による1ステップ数値積分
    引数:
    -----------
    sys_func : 状態方程式 dx/dt = A@x + B@u 計算用関数
    x : 現在の状態変数
    u : 現在の入力
    dt : 積分時間刻み幅[s]

    戻り値:
    --------
    x_next : dt 秒後の状態変数
    """
    k1 = sys_calc(x, u)
    k2 = sys_calc(x + 0.5 * dt * k1, u)
    k3 = sys_calc(x + 0.5 * dt * k2, u)
    k4 = sys_calc(x + dt * k3, u)

    x_next = x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return x_next

def simulation():
  """シミュレーション実行関数"""
  x = np.array([0])   # 連続時間状態変数の初期状態
  x_fw = 0            # 離散時間状態変数(前進差分)の初期状態
  x_bw = 0            # 離散時間状態変数(後退差分)の初期状態
  u = np.array([1])   # 入力(ステップ入力なので常に1)

  for k in range(step_analog):
    # 連続時間系シミュレーション
    x_analog[k] = x
    x = solve_rk4(sys_calc, x, u, dt)     # 1ステップ更新

  for k in range(step_digital):
    # 離散時間系シミュレーション
    x_digital_fw[k] = x_fw                      # 前ステップにおける１サンプル未来の値(現在値)
    x_fw = -(omega*Ts - 1) * x_fw + omega*Ts*u  # 前進差分法での計算

    x_digital_bw[k] = 1/(1 + omega*Ts) * (x_bw + omega * Ts * u)  # 後退差分での計算                     
    x_bw = x_digital_bw[k]                                        # データの保持


# グラフ描画準備
fig, ax = plt.subplots(figsize=(10, 7))                     # グラフのサイズ指定(横：10インチ、縦：7インチ)
plt.subplots_adjust(bottom=0.30)                            # グラフ下部にGUIスペースを確保(最上部～下30%までが描画スペース)
fig.text(0.06, 0.20, 'Sampling Time:1.0[ms]', fontsize=11)  # 画面左端6%,下端15%の点からテキスト表示

# 初期グラフの描画
simulation()
line_analog, = ax.plot(t_analog * 1000, x_analog, label='Analog')
line_digital_fw, = ax.plot(t_digital * 1000, x_digital_fw, label='Forward Difference', alpha=0.6)
line_digital_bw, = ax.plot(t_digital * 1000, x_digital_bw, label='Backward Difference', alpha=0.6)

# グラフ詳細設定
ax.set_xlim(t_start*1000, t_final*1000-10)              # X軸表示範囲指定(単位をmsにするため1000倍)
ax.set_ylim(-0.25, 2.25)                                # Y軸表示範囲指定
ax.set_title('Interactive Discretization Simulator')    # タイトル指定
ax.set_xlabel('Time[ms]')                               # X軸ラベル指定
ax.set_ylabel('Amplitude[-]')                           # Y軸ラベル指定
ax.grid(True)                                           # グリッド表示指定
ax.legend(loc='lower right')                            # 凡例表示指定

# スライダー
omega_min = 100
omega_max = 2500
ax_slider_omega  = plt.axes([0.20, 0.12, 0.35, 0.04])                                                                 # 画面左端20%,下端12%の点をスライダー描画開始点に指定(横幅：画面40%,縦幅：画面4%)
slider_omega  = Slider(ax_slider_omega, 'Cut-off Freq[rad/s]', omega_min, omega_max, valinit=omega, valfmt='%.0f')    # LPFカットオフ周波数設定用スライダー

# テキストボックス（直接入力用）
ax_text_omega  = plt.axes([0.245, 0.06, 0.10, 0.04])                                            # 画面左端24.5%,下端6%の点をテキストボックス描画開始点に指定(横幅：画面10%,縦幅：画面4%)
text_omega  = TextBox(ax_text_omega, 'Cut-off Freq[rad/s](Direct) ', initial=f"{omega:.0f}")    # LPFカットオフ周波数設定用テキストボックス

# リセットボタン
ax_button = plt.axes([0.75, 0.06, 0.10, 0.04])                                      # 画面左端75%,下端6%の点をスライダー描画開始点に指定(横幅：画面10%,縦幅：画面4%)
button_reset = Button(ax_button, 'Reset', color='lightgray', hovercolor='0.9')      # リセットボタン

def on_slider_change(val):
    """スライダー操作時イベント"""
    global omega
    omega = slider_omega.val                  # スライダーでのomega設定値の読み込み
    text_omega.set_val(f"{omega:.0f}")        # omega設定用テキストボックスの表示更新(スライダーに連動して更新)
    simulation()                              # simulationの実行
    line_analog.set_ydata(x_analog)           # 再計算した連続時間系データをセット
    line_digital_fw.set_ydata(x_digital_fw)   # 再計算した離散時間系データ(前進差分)をセット
    line_digital_bw.set_ydata(x_digital_bw)   # 再計算した離散時間系データ(後退差分)をセット
    fig.canvas.draw_idle()

def on_text_submit(text):
    """テキストボックス入力時イベント(Enterキー押下時)"""
    try:
        omega = float(text_omega.text)

        if omega<omega_min:
            omega = omega_min   # omega最小値チェック
        elif omega>omega_max:
            omega = omega_max   # omega最大値チェック

        slider_omega.set_val(omega)   # omega設定用スライダーの表示更新(テキストボックスに連動して更新)
    except ValueError:
        pass # 文字データなどが入力された場合は無視

def reset(event):
    """リセットボタン押下時イベント"""
    # テキストボックス表示はスライダーリセットに連動する形で更新
    slider_omega.reset()

# イベントの紐付け
slider_omega.on_changed(on_slider_change)
text_omega.on_submit(on_text_submit)
button_reset.on_clicked(reset)

plt.show()