# 作物呼吸模型公式汇总

## 1. 呼吸速率与总光合速率的线性关系

**公式：**
$$R_p = \alpha \cdot P_g$$

**参数说明：**
- $R_p$: 作物呼吸速率 (μmol CO₂ m⁻² s⁻¹)
- $P_g$: 总光合速率 (μmol CO₂ m⁻² s⁻¹)
- $\alpha$: 呼吸系数（典型值：0.45，范围：0.30-0.60）

**对应图表：**
- `rp_vs_pg.png`
- `rp_vs_pg.pdf`

---

## 2. Rubisco呼吸速率公式

**公式：**
$$R_p = R_{p,max} \cdot \frac{O_2/K_s}{(CO_2/K_c) + (1 + O_2/K_o)}$$

**参数说明：**
- $R_p$: 呼吸速率 (μmol CO₂ m⁻² s⁻¹)
- $R_{p,max}$: 最大呼吸速率 (μmol CO₂ m⁻² s⁻¹)
- $CO_2$: CO₂浓度 (μmol mol⁻¹)
- $O_2$: O₂浓度 (mmol mol⁻¹)
- $K_s$: O₂的Michaelis常数 (mmol mol⁻¹)
- $K_c$: CO₂的Michaelis常数 (μmol mol⁻¹)
- $K_o$: O₂的抑制常数 (mmol mol⁻¹)

**默认参数值：**
- $R_{p,max}$ = 20 μmol CO₂ m⁻² s⁻¹
- $K_s$ = 2.5 mmol mol⁻¹
- $K_c$ = 40 μmol mol⁻¹
- $K_o$ = 25 mmol mol⁻¹

**对应图表：**
- `rubisco_rp.png` (2D图)
- `rubisco_rp.pdf` (2D图)
- `rubisco_rp_3d.png` (3D曲面图)
- `rubisco_rp_3d.pdf` (3D曲面图)

---

## 3. 净光合速率公式

**公式：**
$$A_n = V_c - 0.5 \cdot V_o - R_d$$

**参数说明：**
- $A_n$: 净光合速率 (μmol CO₂ m⁻² s⁻¹)
- $V_c$: Rubisco羧化速率 (μmol CO₂ m⁻² s⁻¹)
- $V_o$: Rubisco加氧速率 (μmol O₂ m⁻² s⁻¹)
- $R_d$: 暗呼吸速率 (μmol CO₂ m⁻² s⁻¹)

**公式含义：**
- $V_c$: 总羧化作用产生的CO₂固定
- $-0.5 \cdot V_o$: 光呼吸导致的CO₂损失（每次加氧反应释放0.5个CO₂）
- $-R_d$: 暗呼吸导致的CO₂损失

**默认参数值：**
- $V_c$ 范围：0-100 μmol CO₂ m⁻² s⁻¹
- $V_o$ 范围：0-80 μmol O₂ m⁻² s⁻¹
- $R_d$ = 2 μmol CO₂ m⁻² s⁻¹

**对应图表：**
- `net_photosynthesis.png` (组分分析图)
- `net_photosynthesis.pdf` (组分分析图)
- `net_photosynthesis_stacked.png` (堆积分析图)
- `net_photosynthesis_stacked.pdf` (堆积分析图)
- `net_photosynthesis_vo_response.png` (敏感性分析图)
- `net_photosynthesis_vo_response.pdf` (敏感性分析图)

---

## 4. 维持呼吸速率公式

**公式：**
$$R_m = \sum_i r_{m,i} \cdot W_i$$

**参数说明：**
- $R_m$: 维持呼吸速率 (g CH₂O m⁻² d⁻¹)
- $r_{m,i}$: 第i个器官的维持呼吸系数 (g CH₂O g⁻¹干重 d⁻¹ 或 g CH₂O g⁻¹蛋白质 d⁻¹)
- $W_i$: 第i个器官的干重 (g干重 m⁻²) 或蛋白质量 (g蛋白质 m⁻²)

**典型呼吸系数（基于干重）：**
- 叶片：0.015 g CH₂O g⁻¹ d⁻¹ (范围：0.012-0.018)
- 茎：0.010 g CH₂O g⁻¹ d⁻¹ (范围：0.008-0.012)
- 根：0.012 g CH₂O g⁻¹ d⁻¹ (范围：0.010-0.014)
- 果实/籽粒：0.008 g CH₂O g⁻¹ d⁻¹ (范围：0.006-0.010)
- 花：0.020 g CH₂O g⁻¹ d⁻¹ (范围：0.016-0.024)

**对应图表：**
- `maintenance_respiration_organs.png` (器官贡献分析)
- `maintenance_respiration_organs.pdf` (器官贡献分析)
- `maintenance_respiration_sensitivity.png` (干重敏感性分析)
- `maintenance_respiration_sensitivity.pdf` (干重敏感性分析)
- `maintenance_respiration_coefficients.png` (呼吸系数对比)
- `maintenance_respiration_coefficients.pdf` (呼吸系数对比)

---

## 5. 温度对维持呼吸速率的影响

**公式：**
$$R_m(T) = R_{m0} \cdot Q_{10}^{(T-T_0)/10}$$

**参数说明：**
- $R_m(T)$: 温度T时的维持呼吸速率 (g CH₂O m⁻² d⁻¹)
- $R_{m0}$: 基准温度$T_0$下的维持呼吸速率 (g CH₂O m⁻² d⁻¹)
- $Q_{10}$: 温度系数，作物呼吸时一般取 $Q_{10} = 2$
- $T$: 当前温度 (°C)
- $T_0$: 基准温度，通常为 25°C

**温度系数说明：**
- $Q_{10} = 2$ 表示温度每升高10°C，呼吸速率增加1倍
- 典型范围：1.5 - 3.0
- 作物呼吸常用值：$Q_{10} = 2$

**对应图表：**
- `temperature_respiration.png` (温度响应曲线)
- `temperature_respiration.pdf` (温度响应曲线)
- `temperature_respiration_q10.png` (Q₁₀敏感性分析)
- `temperature_respiration_q10.pdf` (Q₁₀敏感性分析)
- `temperature_respiration_relative.png` (相对变化分析)
- `temperature_respiration_relative.pdf` (相对变化分析)

---

## 6. 氮含量对维持呼吸系数的影响

**公式：**
$$r'_{m,i} = r_{ref} \times \frac{N_i}{N_{ref}}$$

**参数说明：**
- $r'_{m,i}$: 当前氮含量下的维持呼吸系数 (g CH₂O g⁻¹ d⁻¹)
- $r_{ref}$: 参考氮含量下的维持呼吸系数 (g CH₂O g⁻¹ d⁻¹)
- $N_i$: 当前氮含量 (% 或 g N g⁻¹干重)
- $N_{ref}$: 参考氮含量 (% 或 g N g⁻¹干重)

**典型参考值：**
- 叶片：$N_{ref} = 3.0\%$, $r_{ref} = 0.015$ g CH₂O g⁻¹ d⁻¹
- 茎：$N_{ref} = 1.5\%$, $r_{ref} = 0.010$ g CH₂O g⁻¹ d⁻¹
- 根：$N_{ref} = 2.0\%$, $r_{ref} = 0.012$ g CH₂O g⁻¹ d⁻¹

**公式含义：**
- 呼吸系数与氮含量成正比
- 氮含量高的组织代谢更活跃，呼吸速率更高
- 此公式用于根据实际氮含量调整维持呼吸系数

**对应图表：**
- `nitrogen_respiration.png` (氮含量响应曲线)
- `nitrogen_respiration.pdf` (氮含量响应曲线)
- `nitrogen_respiration_organs.png` (器官对比)
- `nitrogen_respiration_organs.pdf` (器官对比)
- `nitrogen_respiration_relative.png` (相对变化分析)
- `nitrogen_respiration_relative.pdf` (相对变化分析)

---

## 7. 生长呼吸速率

**主公式：**
$$R_g = m \cdot GTW$$

**参数说明：**
- $R_g$: 生长呼吸速率 (g CO₂ m⁻² d⁻¹)
- $m$: 生长呼吸系数 (g CO₂ g⁻¹ DM)
- $GTW$: 当天总的同化量 (g DM m⁻² d⁻¹)

**综合生长呼吸系数计算：**
$$m_i = \sum_j f_j \cdot m_j$$

其中：
- $m_i$: 器官i的综合生长呼吸系数
- $f_j$: 器官i中化学组分j的质量分数
- $m_j$: 化学组分j的生长呼吸系数

**生长呼吸系数（表4.3-4，Goudriaan & van Laar, 1994）：**
| 化学组分 | 碳含量 (g C g⁻¹) | 葡萄糖需求量 (g g⁻¹) | 生长呼吸系数 (g CO₂ g⁻¹) |
|---------|------------------|---------------------|------------------------|
| 碳水化合物 | 0.450 | 1.242 | 0.17 |
| 蛋白质 | 0.532 | 2.70 | 2.01 |
| 脂类化合物 | 0.773 | 3.11 | 1.72 |
| 木质素 | 0.690 | 2.17 | 0.66 |
| 有机酸 | 0.375 | 0.93 | -0.01 |

**公式含义：**
- 生长呼吸是合成新组织所需的能量消耗
- 呼吸速率与同化量成正比
- 不同化学组分的合成成本差异很大
- 蛋白质和脂类合成需要最多能量（系数最高）
- 器官的综合呼吸系数取决于其化学组成

**对应图表：**
- `growth_respiration.png` (线性响应曲线)
- `growth_respiration.pdf` (线性响应曲线)
- `growth_respiration_coefficients.png` (化学组分系数对比)
- `growth_respiration_coefficients.pdf` (化学组分系数对比)
- `growth_respiration_seasonal.png` (季节变化模式)
- `growth_respiration_seasonal.pdf` (季节变化模式)
- `growth_respiration_composite.png` (综合系数计算示例)
- `growth_respiration_composite.pdf` (综合系数计算示例)

---

## 图表说明

### 格式
所有图表提供两种格式：
- **PNG**: 300 dpi，适用于演示和书籍排版
- **PDF**: 矢量格式，适合学术出版和印刷

### 风格
所有图表采用黑白风格设计：
- 适合黑白打印和复印
- 层次分明，易于区分
- 符合学术期刊要求
- 成本低廉

### 文件列表

**图1：呼吸速率与总光合速率**
- rp_vs_pg.png
- rp_vs_pg.pdf

**图2：Rubisco呼吸速率**
- rubisco_rp.png (2D)
- rubisco_rp.pdf (2D)
- rubisco_rp_3d.png (3D)
- rubisco_rp_3d.pdf (3D)

**图3：净光合速率**
- net_photosynthesis.png (组分分析)
- net_photosynthesis.pdf (组分分析)
- net_photosynthesis_stacked.png (堆积图)
- net_photosynthesis_stacked.pdf (堆积图)
- net_photosynthesis_vo_response.png (敏感性分析)
- net_photosynthesis_vo_response.pdf (敏感性分析)

**图4：维持呼吸速率**
- maintenance_respiration_organs.png (器官贡献)
- maintenance_respiration_organs.pdf (器官贡献)
- maintenance_respiration_sensitivity.png (干重敏感性)
- maintenance_respiration_sensitivity.pdf (干重敏感性)
- maintenance_respiration_coefficients.png (呼吸系数对比)
- maintenance_respiration_coefficients.pdf (呼吸系数对比)

**图5：温度对呼吸的影响**
- temperature_respiration.png (温度响应)
- temperature_respiration.pdf (温度响应)
- temperature_respiration_q10.png (Q₁₀敏感性)
- temperature_respiration_q10.pdf (Q₁₀敏感性)
- temperature_respiration_relative.png (相对变化)
- temperature_respiration_relative.pdf (相对变化)

**图6：氮含量对呼吸的影响**
- nitrogen_respiration.png (氮含量响应)
- nitrogen_respiration.pdf (氮含量响应)
- nitrogen_respiration_organs.png (器官对比)
- nitrogen_respiration_organs.pdf (器官对比)
- nitrogen_respiration_relative.png (相对变化)
- nitrogen_respiration_relative.pdf (相对变化)

**图7：生长呼吸速率**
- growth_respiration.png (线性响应)
- growth_respiration.pdf (线性响应)
- growth_respiration_coefficients.png (化学组分系数)
- growth_respiration_coefficients.pdf (化学组分系数)
- growth_respiration_seasonal.png (季节变化)
- growth_respiration_seasonal.pdf (季节变化)
- growth_respiration_composite.png (综合系数计算)
- growth_respiration_composite.pdf (综合系数计算)

---

## 使用方法

### 运行脚本
```bash
# 生成图1：呼吸速率与总光合速率
python plot_rp_pg.py

# 生成图2：Rubisco呼吸速率（2D和3D）
python plot_rubisco_rp.py

# 生成图3：净光合速率（三张图）
python plot_net_photosynthesis.py

# 生成图4：维持呼吸速率（三张图）
python plot_maintenance_respiration.py

# 生成图5：温度对呼吸的影响（三张图）
python plot_temperature_respiration.py

# 生成图6：氮含量对呼吸的影响（三张图）
python plot_nitrogen_respiration.py

# 生成图7：生长呼吸速率（三张图）
python plot_growth_respiration.py
```

### 修改参数
每个脚本中的参数都可以在函数调用时修改，例如：

```python
# 在 plot_rp_pg.py 中
make_plot(
    alpha=0.50,          # 修改呼吸系数
    alpha_min=0.35,      # 修改最小值
    alpha_max=0.65,      # 修改最大值
    pg_max=50.0,         # 修改最大光合速率
)
```

---

**生成时间：** 2025年10月24日  
**Python版本：** 需要 numpy, matplotlib  
**依赖包：** `pip install numpy matplotlib`

