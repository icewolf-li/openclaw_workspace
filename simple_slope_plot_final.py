# ============================================================ 
# 简单斜率图生成代码 - 有调节的中介模型 
# 基于你的真实数据结果 
# ============================================================ 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm

# 查找并设置中文字体
font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
try:
    # 创建字体属性对象
    chinese_font = fm.FontProperties(fname=font_path)
    # 设置全局字体
    rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    rcParams['axes.unicode_minus'] = False
    print("成功设置中文字体")
except:
    # 如果找不到指定字体，使用系统默认
    rcParams['font.sans-serif'] = ['DejaVu Sans']
    rcParams['axes.unicode_minus'] = False
    print("使用默认字体")

# ------------------------------------------------------------
# 1. 输入你的回归系数（来自 PROCESS 输出）
# ------------------------------------------------------------

# 文化认同感 = b0 + b1*参与频率 + b2*是否了解 + b3*参与频率×是否了解
# 根据输出：
b0 = 4.1468  # 常数项
b1 = 0.4118  # 参与频率主效应  
b2 = 0.3502  # 是否了解主效应
b3 = -0.4846 # 交互项系数

# 调节变量编码：1=了解，2=不了解
W_了解 = 1
W_不了解 = 2

# ------------------------------------------------------------
# 2. 计算两条简单斜率
# ------------------------------------------------------------

# 参与频率的取值范围（假设是 1-5 点量表）
X = np.linspace(1, 5, 100)

# 当 W=1 (了解) 时：Y = b0 + b1*X + b2*1 + b3*X*1
Y_了解 = b0 + b1*X + b2*W_了解 + b3*X*W_了解

# 当 W=2 (不了解) 时：Y = b0 + b1*X + b2*2 + b3*X*2  
Y_不了解 = b0 + b1*X + b2*W_不了解 + b3*X*W_不了解

# ------------------------------------------------------------
# 3. 绘制图形
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# 绘制两条斜率线
ax.plot(X, Y_了解, linewidth=2.5, color='#2E86AB', label='了解非遗 (W=1)\n斜率 = -0.07, p=0.319')
ax.plot(X, Y_不了解, linewidth=2.5, color='#A23B72', label='不了解非遗 (W=2)\n斜率 = -0.56, p<0.001***')

# 填充置信区间（可选，模拟）
# 这里用虚线表示大致范围
ax.plot(X, Y_了解 + 0.3, linestyle='--', color='#2E86AB', alpha=0.3)
ax.plot(X, Y_了解 - 0.3, linestyle='--', color='#2E86AB', alpha=0.3)
ax.plot(X, Y_不了解 + 0.3, linestyle='--', color='#A23B72', alpha=0.3)
ax.plot(X, Y_不了解 - 0.3, linestyle='--', color='#A23B72', alpha=0.3)

# 设置标签和标题
ax.set_xlabel('参与频率', fontsize=12, fontweight='bold')
ax.set_ylabel('文化认同感', fontsize=12, fontweight='bold')
ax.set_title('图4-1 是否了解非遗的调节效应', fontsize=14, fontweight='bold', pad=15)

# 设置图例
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

# 设置网格
ax.grid(True, linestyle=':', alpha=0.5)

# 设置坐标轴范围
ax.set_xlim(1, 5)
ax.set_ylim(2.5, 5.5)

# 设置刻度
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_yticks([3, 3.5, 4, 4.5, 5, 5.5])

# 添加注释
ax.annotate('不了解组：\n参与越多，认同越低', xy=(4, 3.2), xytext=(3, 3.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            fontsize=10, color='#A23B72', fontweight='bold')
ax.annotate('了解组：\n参与影响不显著', xy=(4, 4.3), xytext=(2.5, 4.8),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            fontsize=10, color='#2E86AB', fontweight='bold')

# 调整布局
plt.tight_layout()

# 保存高清图片
png_file = '简单斜率图_调节效应_final.png'
pdf_file = '简单斜率图_调节效应_final.pdf'

plt.savefig(png_file, dpi=300, bbox_inches='tight')
plt.savefig(pdf_file, dpi=300, bbox_inches='tight')

print(f"✅ 图形已生成并保存为 '{png_file}' 和 '{pdf_file}'")
print(f"当前工作目录: {os.getcwd()}")