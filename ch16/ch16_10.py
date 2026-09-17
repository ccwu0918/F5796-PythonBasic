# 參閱16-45頁

import numpy as np

def calc_angle(s, e, w):
    se = np.array(s) - np.array(e)  # 座標點轉換成向量
    we = np.array(w) - np.array(e)
    dot_product = np.dot(se, we)    # 計算向量的點積
    mag1 = np.linalg.norm(se)       # 肩→肘的向量長度
    mag2 = np.linalg.norm(we)       # 腕→肘的向量長度
    angle_rad = np.arccos(dot_product / (mag1 * mag2)) # 夾角的弧度
    angle_deg = np.degrees(angle_rad) # 弧度轉角度
    return angle_deg

shoulder = np.array([2, 2])  # 肩膀的座標
elbow = np.array([4, 6])     # 手肘的座標
wrist = np.array([7, 7])     # 手腕的座標

angle = calc_angle(shoulder, elbow, wrist)
print(f'手臂彎曲的角度：{angle:.2f}度')