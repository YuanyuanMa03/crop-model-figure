"""
生长呼吸速率公式可视化
公式：R_g = m · GTW

其中：
- R_g: 生长呼吸速率 (g CO₂ m⁻² d⁻¹)
- m: 生长呼吸系数 (g CO₂ g⁻¹ DM)
- GTW: 当天总的同化量 (g DM m⁻² d⁻¹)

输出：figures/growth_respiration_*.{png, pdf}
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def growth_respiration(GTW, m):
    """
    计算生长呼吸速率
    
    参数:
        GTW: 当天总的同化量 (g DM m⁻² d⁻¹)
        m: 生长呼吸系数 (g CO₂ g⁻¹ DM)
    
    返回:
        Rg: 生长呼吸速率 (g CO₂ m⁻² d⁻¹)
    """
    return m * GTW


def make_linear_response_plot():
    """
    绘制生长呼吸速率对同化量的线性响应
    """
    # 创建输出目录
    out_dir = Path('figures')
    out_dir.mkdir(exist_ok=True)

    # 高质量出版参数
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except Exception:
        plt.style.use('seaborn-whitegrid')
    
    plt.rcParams.update({
        'font.size': 12,
        'font.sans-serif': ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'figure.figsize': (7.5, 5.5),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 不同的生长呼吸系数
    m_values = [0.20, 0.25, 0.30, 0.35]  # g CO₂ g⁻¹ DM
    
    # 同化量范围
    GTW = np.linspace(0, 30, 300)  # g DM m⁻² d⁻¹
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['--', '-', '-.', ':']
    colors = ['0.5', 'black', '0.3', '0.6']
    markers = ['s', 'o', '^', 'd']
    linewidths = [2, 3, 2, 2]
    
    # 绘制不同m值的曲线
    for i, m in enumerate(m_values):
        Rg = growth_respiration(GTW, m)
        
        ls = linestyles[i]
        color = colors[i]
        marker = markers[i]
        lw = linewidths[i]
        
        label = f'$m$ = {m:.2f}' + (' (典型值)' if m == 0.25 else '')
        
        ax.plot(GTW, Rg, color=color, linestyle=ls, linewidth=lw, label=label,
               zorder=10 if m == 0.25 else 5)
        
        # 添加标记点
        sample_indices = np.linspace(30, len(GTW)-30, 5, dtype=int)
        ax.plot(GTW[sample_indices], Rg[sample_indices], marker=marker,
               color=color, markersize=6 if m != 0.25 else 7,
               linestyle='None', markerfacecolor='white', markeredgewidth=1.5,
               zorder=11 if m == 0.25 else 6)
    
    # 轴标签
    ax.set_xlabel(r'$GTW$ - 当天总同化量 (g DM m$^{-2}$ d$^{-1}$)', fontsize=12)
    ax.set_ylabel(r'$R_g$ - 生长呼吸速率 (g CO$_2$ m$^{-2}$ d$^{-1}$)', fontsize=12)
    
    # 范围
    ax.set_xlim(0, 30)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=11)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)
    
    # 公式标注
    formula = r'$R_g = m \cdot GTW$'
    ax.text(0.98, 0.35, formula, transform=ax.transAxes,
            ha='right', va='top', fontsize=13,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('生长呼吸速率与同化量的线性关系', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'growth_respiration.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_coefficient_comparison_plot():
    """
    绘制不同组织/器官的生长呼吸系数对比
    基于表4.3-4 (Goudriaan & van Laar, 1994)
    """
    # 创建输出目录
    out_dir = Path('figures')
    out_dir.mkdir(exist_ok=True)

    # 高质量出版参数
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except Exception:
        plt.style.use('seaborn-whitegrid')
    
    plt.rcParams.update({
        'font.size': 12,
        'font.sans-serif': ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'figure.figsize': (8, 5.5),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 不同组分的生长呼吸系数（表4.3-4真实数据）
    components = ['碳水化合物', '蛋白质', '脂类化合物', '木质素', '有机酸']
    m_values = np.array([0.17, 2.01, 1.72, 0.66, -0.01])  # g CO₂ g⁻¹ DM
    carbon_content = np.array([0.450, 0.532, 0.773, 0.690, 0.375])  # g C g⁻¹ DM
    glucose_req = np.array([1.242, 2.70, 3.11, 2.17, 0.93])  # g 葡萄糖 g⁻¹ DM
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    x = np.arange(len(components))
    width = 0.6
    
    # 填充图案和颜色（处理负值）
    hatches = ['///', '\\\\\\', 'xxx', '|||', '...']
    colors_pattern = ['0.85', '0.4', '0.55', '0.7', '0.95']
    
    # 绘制柱状图
    bars = ax.bar(x, m_values, width, edgecolor='black', linewidth=1.5)
    
    # 为每个柱子设置不同的填充
    for bar, color, hatch in zip(bars, colors_pattern, hatches):
        bar.set_facecolor(color)
        bar.set_hatch(hatch)
    
    # 在柱顶/底标注数值
    for i, val in enumerate(m_values):
        if val >= 0:
            ax.text(i, val + 0.05, f'{val:.2f}',
                   ha='center', va='bottom', fontsize=9, weight='bold')
        else:
            ax.text(i, val - 0.05, f'{val:.2f}',
                   ha='center', va='top', fontsize=9, weight='bold')
    
    # 轴标签
    ax.set_xlabel('化学组分', fontsize=12, weight='bold')
    ax.set_ylabel(r'$m$ - 生长呼吸系数 (g CO$_2$ g$^{-1}$ DM)', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(components, rotation=15, ha='right')
    ax.set_ylim(min(m_values) * 1.2, max(m_values) * 1.15)
    
    # 添加零线
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, zorder=0)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, 
            linewidth=0.8, axis='y')
    
    # 数据来源标注
    note_text = '数据来源: Goudriaan & van Laar (1994)\n表4.3-4'
    ax.text(0.02, 0.98, note_text, transform=ax.transAxes,
            ha='left', va='top', fontsize=8, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='0.5', linewidth=0.8))
    
    # 标题
    ax.set_title('不同化学组分的生长呼吸系数', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'growth_respiration_coefficients.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_daily_pattern_plot():
    """
    绘制生长季节中同化量和生长呼吸的日变化模式
    """
    # 创建输出目录
    out_dir = Path('figures')
    out_dir.mkdir(exist_ok=True)

    # 高质量出版参数
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except Exception:
        plt.style.use('seaborn-whitegrid')
    
    plt.rcParams.update({
        'font.size': 12,
        'font.sans-serif': ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'figure.figsize': (9, 5.5),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 模拟生长季节（100天）
    days = np.arange(0, 100)
    
    # 模拟同化量的季节变化（先增后减）
    peak_day = 50
    max_GTW = 25
    GTW = max_GTW * np.exp(-((days - peak_day) / 25)**2)
    
    # 生长呼吸系数
    m = 0.25
    
    # 计算生长呼吸
    Rg = growth_respiration(GTW, m)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    
    # 设置边框
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1.2)
    
    # === 上图：同化量 ===
    ax1.fill_between(days, 0, GTW, color='0.85', alpha=0.7, 
                     edgecolor='black', linewidth=1.5, label='GTW')
    ax1.plot(days, GTW, color='black', linestyle='-', linewidth=2.5)
    
    # 标注峰值
    ax1.plot(peak_day, max_GTW, marker='o', color='black', markersize=10,
            markerfacecolor='white', markeredgewidth=2)
    ax1.annotate(f'峰值: {max_GTW:.0f} g DM m$^{{-2}}$ d$^{{-1}}$',
                xy=(peak_day, max_GTW), xytext=(peak_day + 15, max_GTW - 3),
                fontsize=10, ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='black', linewidth=1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    
    ax1.set_ylabel(r'$GTW$ (g DM m$^{-2}$ d$^{-1}$)', fontsize=12)
    ax1.set_ylim(0, max_GTW * 1.2)
    ax1.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, linewidth=0.8)
    ax1.set_title('生长季节的同化量变化', fontsize=13, pad=10, weight='bold')
    
    # === 下图：生长呼吸 ===
    ax2.fill_between(days, 0, Rg, color='0.6', alpha=0.7, hatch='///',
                     edgecolor='black', linewidth=1.5, label='$R_g$')
    ax2.plot(days, Rg, color='black', linestyle='-', linewidth=2.5)
    
    # 标注峰值
    peak_Rg = m * max_GTW
    ax2.plot(peak_day, peak_Rg, marker='o', color='black', markersize=10,
            markerfacecolor='white', markeredgewidth=2)
    ax2.annotate(f'峰值: {peak_Rg:.1f} g CO$_2$ m$^{{-2}}$ d$^{{-1}}$',
                xy=(peak_day, peak_Rg), xytext=(peak_day + 15, peak_Rg - 0.8),
                fontsize=10, ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='black', linewidth=1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    
    ax2.set_xlabel('生长季节天数 (d)', fontsize=12)
    ax2.set_ylabel(r'$R_g$ (g CO$_2$ m$^{-2}$ d$^{-1}$)', fontsize=12)
    ax2.set_ylim(0, peak_Rg * 1.2)
    ax2.set_xlim(0, 100)
    ax2.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, linewidth=0.8)
    ax2.set_title(f'生长呼吸速率变化 ($m$ = {m:.2f})', fontsize=13, pad=10, weight='bold')
    
    # 公式标注
    formula = r'$R_g = m \cdot GTW$'
    ax2.text(0.02, 0.95, formula, transform=ax2.transAxes,
            ha='left', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'growth_respiration_seasonal.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_composite_coefficient_plot():
    """
    绘制器官综合生长呼吸系数的计算示例
    展示公式：m_i = Σ f_j · m_j
    """
    # 创建输出目录
    out_dir = Path('figures')
    out_dir.mkdir(exist_ok=True)

    # 高质量出版参数
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except Exception:
        plt.style.use('seaborn-whitegrid')
    
    plt.rcParams.update({
        'font.size': 12,
        'font.sans-serif': ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'figure.figsize': (9, 6),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 各组分的生长呼吸系数（表4.3-4）
    components = ['碳水化合物', '蛋白质', '脂类化合物', '木质素', '有机酸']
    m_j = np.array([0.17, 2.01, 1.72, 0.66, -0.01])
    
    # 不同器官的组分比例示例
    organs = ['叶片', '茎', '根', '籽粒']
    
    # 各器官中各组分的质量分数 f_j (假设值，总和=1)
    fractions = {
        '叶片': np.array([0.30, 0.20, 0.10, 0.15, 0.25]),    # 蛋白质含量较高
        '茎': np.array([0.45, 0.08, 0.05, 0.35, 0.07]),      # 碳水化合物和木质素多
        '根': np.array([0.40, 0.12, 0.08, 0.30, 0.10]),      # 类似茎
        '籽粒': np.array([0.60, 0.20, 0.15, 0.03, 0.02]),    # 碳水化合物和蛋白质多
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
    
    # 设置边框
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1.2)
    
    # === 左图：组分比例堆积图 ===
    x = np.arange(len(organs))
    width = 0.6
    
    colors_pattern = ['0.85', '0.4', '0.55', '0.7', '0.95']
    hatches = ['///', '\\\\\\', 'xxx', '|||', '...']
    
    bottom = np.zeros(len(organs))
    for i, comp in enumerate(components):
        values = np.array([fractions[organ][i] for organ in organs])
        bars = ax1.bar(x, values, width, bottom=bottom, 
                      label=comp, color=colors_pattern[i], 
                      edgecolor='black', linewidth=1, hatch=hatches[i])
        bottom += values
    
    ax1.set_xlabel('器官', fontsize=12, weight='bold')
    ax1.set_ylabel(r'组分质量分数 $f_j$', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(organs)
    ax1.set_ylim(0, 1.05)
    ax1.legend(frameon=True, loc='upper right', edgecolor='black', 
              fancybox=False, fontsize=9, ncol=1)
    ax1.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, 
            linewidth=0.8, axis='y')
    ax1.set_title('不同器官的化学组分构成', fontsize=13, pad=10, weight='bold')
    
    # === 右图：计算的综合呼吸系数 ===
    m_i_values = []
    for organ in organs:
        f_j = fractions[organ]
        m_i = np.sum(f_j * m_j)  # m_i = Σ f_j · m_j
        m_i_values.append(m_i)
    
    m_i_values = np.array(m_i_values)
    
    # 绘制柱状图
    bars2 = ax2.bar(x, m_i_values, width, edgecolor='black', linewidth=1.5)
    
    # 为每个柱子设置渐变颜色
    organ_colors = ['0.3', '0.5', '0.65', '0.8']
    organ_hatches = ['', '///', '\\\\\\', 'xxx']
    for bar, color, hatch in zip(bars2, organ_colors, organ_hatches):
        bar.set_facecolor(color)
        bar.set_hatch(hatch)
    
    # 标注数值
    for i, val in enumerate(m_i_values):
        ax2.text(i, val + 0.015, f'{val:.3f}',
                ha='center', va='bottom', fontsize=10, weight='bold')
    
    ax2.set_xlabel('器官', fontsize=12, weight='bold')
    ax2.set_ylabel(r'$m_i$ - 综合生长呼吸系数 (g CO$_2$ g$^{-1}$ DM)', fontsize=11)
    ax2.set_xticks(x)
    ax2.set_xticklabels(organs)
    ax2.set_ylim(0, max(m_i_values) * 1.15)
    ax2.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, 
            linewidth=0.8, axis='y')
    ax2.set_title('计算得到的综合生长呼吸系数', fontsize=13, pad=10, weight='bold')
    
    # 公式标注
    formula = r'$m_i = \sum_j f_j \cdot m_j$'
    ax2.text(0.98, 0.95, formula, transform=ax2.transAxes,
            ha='right', va='top', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'growth_respiration_composite.{ext}', bbox_inches='tight')
    
    plt.close(fig)


if __name__ == '__main__':
    # 生成线性响应图
    make_linear_response_plot()
    print('线性响应图生成完成: figures/growth_respiration.[png, pdf]')
    
    # 生成呼吸系数对比图
    make_coefficient_comparison_plot()
    print('呼吸系数对比图生成完成: figures/growth_respiration_coefficients.[png, pdf]')
    
    # 生成季节变化图
    make_daily_pattern_plot()
    print('季节变化图生成完成: figures/growth_respiration_seasonal.[png, pdf]')
    
    # 生成综合系数计算图
    make_composite_coefficient_plot()
    print('综合系数计算图生成完成: figures/growth_respiration_composite.[png, pdf]')

