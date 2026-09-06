# Interactive Discretization Simulator

PythonとMatplotlibを用いた、離散時間化1次ローパスフィルタ挙動の動的可視化ツールです。

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 概要 (Overview)
1次ローパスフィルタを前進差分法で離散時間化するとき、ローパスフィルタカットオフ周波数を高くするにつて挙動が不安定になっていく様子をインタラクティブに観察できます。

- スライダーまたは数値の直接入力により、ローパスフィルタカットオフ周波数をリアルタイムに変更可能（単位は[rad/s]）
- 連続時間系、前進差分法、後退差分法の波形比較により、前進差分法の危うさを直感的に理解可能

---

## 理論的背景 (Theoretical Background)

1次ローパスフィルタを前進差分法で離散時間化した場合、以下の条件を満たすと、ローパスフィルタが不安定極を持ち、挙動が不安定化します。
（サンプリング周期： $T_s$[s]、カットオフ周波数：$\omega$[rad/s]）

$$\omega*T_s >2$$

本ツールでは$T_s$=1.0[ms]（固定）のため、カットオフ周波数が2000[rad/s]を超えると、前進差分法でのシミュレーション波形が不安定化します。

---

## 設計上のこだわり (Design Note)
ルンゲ・クッタ法（4次）により、高精度な連続時間系シミュレーションができるようにしています。

---

## 実行方法 (Usage)

### 必要なライブラリ
```bash
pip install numpy matplotlib
```
### 実行手順
```bash
python sample_discretization.py
```
