import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 车辆参数
L_f = 1.25
L_r = 1.25
V = 10  # 车辆速度，单位：米/秒
delta = np.deg2rad(20)  # 前轮偏转角，单位：弧度

# 运动参数
dt = 0.1  # 时间间隔，单位：秒
total_time = 5  # 总仿真时间，单位：秒
steps = int(total_time / dt)  # 总步数

# 初始化车辆状态
x = 0  # 车辆x坐标，单位：米
y = 0  # 车辆y坐标，单位：米
psi = 0  # 车辆航向角，单位：弧度
beta = np.arctan((L_r / (L_r + L_f)) * np.tan(delta))


# 车辆运动轨迹
x_traj = [x]
y_traj = [y]

for _ in range(steps):
    # 更新x、y坐标以及与x轴夹角
    x += V * np.cos(psi + beta) * dt
    y += V * np.sin(psi + beta) * dt
    print(psi + beta)
    psi += (V / L_r) * np.sin(beta) * dt

    x_traj.append(x)
    y_traj.append(y)

# 绘制车辆轨迹
plt.figure(figsize=(8, 6))
plt.plot(x_traj, y_traj, label='车辆轨迹')
plt.scatter(x_traj[0], y_traj[0], color='r', marker='o', label='起点')
plt.scatter(x_traj[-1], y_traj[-1], color='g', marker='o', label='终点')
plt.axis('equal')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('前轮驱动单车运动模型仿真')
plt.legend()
plt.show()
