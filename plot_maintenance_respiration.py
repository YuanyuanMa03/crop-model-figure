"""
维持呼吸速率公式可视化
公式：R_m = Σ r_{m,i} · W_i

其中：
- R_m: 维持呼吸速率 (g CH₂O m⁻² d⁻¹)
- r_{m,i}: 第i个器官的维持呼吸系数 (g CH₂O g⁻¹干重 d⁻¹ 或 g CH₂O g⁻¹蛋白质 d⁻¹)
- W_i: 第i个器官的干重 (g干重 m⁻²) 或蛋白质量 (g蛋白质 m⁻²)

输出：figures/maintenance_respiration_*.{png, pdf}
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def maintenance_respiration(organ_weights, organ_coeffs):
    """
    计算维持呼吸速率
    
    参数:
        organ_weights: 各器官干重 (g m⁻²)
        organ_coeffs: 各器官维持呼吸系数 (g CH₂O g⁻¹ d⁻¹)
    
    返回:
        Rm: 维持呼吸速率 (g CH₂O m⁻² d⁻¹)
    """
    return np.sum(np.array(organ_weights) * np.array(organ_coeffs))


def make_organ_contribution_plot():
    """
    绘制各器官对维持呼吸的贡献（堆积柱状图）
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

    # 定义器官及其参数（典型作物）
    organs = ['叶片', '茎', '根', '果实/籽粒']
    
    # 不同生育期的器官干重 (g m⁻²)
    growth_stages = ['营养生长期', '开花期', '灌浆期', '成熟期']
    weights = np.array([
        [150, 50, 80, 0],      # 营养生长期
        [250, 120, 150, 50],   # 开花期
        [200, 150, 120, 200],  # 灌浆期
        [150, 160, 100, 300],  # 成熟期
    ])
    
    # 各器官维持呼吸系数 (g CH₂O g⁻¹ d⁻¹)
    coeffs = np.array([0.015, 0.010, 0.012, 0.008])
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)

    # 计算各器官贡献
    contributions = weights * coeffs
    
    # 黑白填充图案和颜色
    colors = ['0.9', '0.7', '0.5', '0.3']
    hatches = ['', '///', '\\\\\\', 'xxx']
    
    # x轴位置
    x = np.arange(len(growth_stages))
    width = 0.6
    
    # 绘制堆积柱状图
    bottom = np.zeros(len(growth_stages))
    bars = []
    for i, organ in enumerate(organs):
        bar = ax.bar(x, contributions[:, i], width, bottom=bottom,
                    label=organ, color=colors[i], edgecolor='black',
                    linewidth=1.5, hatch=hatches[i])
        bars.append(bar)
        bottom += contributions[:, i]
    
    # 在柱顶标注总值
    for i, stage_total in enumerate(bottom):
        ax.text(i, stage_total + 0.1, f'{stage_total:.1f}',
               ha='center', va='bottom', fontsize=10, weight='bold')
    
    # 轴标签
    ax.set_xlabel('生育期', fontsize=13, weight='bold')
    ax.set_ylabel(r'$R_m$ - 维持呼吸速率 (g CH$_2$O m$^{-2}$ d$^{-1}$)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(growth_stages)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=11, ncol=2)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, 
            linewidth=0.8, axis='y')
    
    # 公式标注
    formula = r'$R_m = \sum_i r_{m,i} \cdot W_i$'
    ax.text(0.98, 0.95, formula, transform=ax.transAxes,
            ha='right', va='top', fontsize=13,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('不同生育期各器官对维持呼吸的贡献', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'maintenance_respiration_organs.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_weight_sensitivity_plot():
    """
    绘制维持呼吸对器官干重的响应
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
        'figure.figsize': (7.5, 5),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 器官名称
    organs = ['叶片', '茎', '根', '总计']
    
    # 维持呼吸系数
    r_leaf = 0.015
    r_stem = 0.010
    r_root = 0.012
    
    # 固定茎和根的干重
    W_stem = 100  # g m⁻²
    W_root = 100  # g m⁻²
    
    # 叶片干重范围
    W_leaf = np.linspace(0, 400, 300)
    
    # 计算各部分呼吸
    Rm_leaf = r_leaf * W_leaf
    Rm_stem = r_stem * W_stem * np.ones_like(W_leaf)
    Rm_root = r_root * W_root * np.ones_like(W_leaf)
    Rm_total = Rm_leaf + Rm_stem + Rm_root
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['-', '--', '-.', '-']
    colors = ['0.3', '0.5', '0.7', 'black']
    linewidths = [2, 2, 2, 3]
    markers = ['o', 's', '^', 'D']
    
    # 绘制各组分
    data = [Rm_leaf, Rm_stem, Rm_root, Rm_total]
    
    for i, (organ, Rm, ls, color, lw, marker) in enumerate(
        zip(organs, data, linestyles, colors, linewidths, markers)):
        
        ax.plot(W_leaf, Rm, color=color, linestyle=ls, linewidth=lw,
               label=organ, zorder=10 if organ == '总计' else 5)
        
        # 添加标记点
        if i < 3:  # 不在总计线上加太多点
            sample_indices = np.linspace(30, len(W_leaf)-30, 4, dtype=int)
        else:
            sample_indices = np.linspace(30, len(W_leaf)-30, 6, dtype=int)
            
        ax.plot(W_leaf[sample_indices], Rm[sample_indices], marker=marker,
               color=color, markersize=6 if organ != '总计' else 7,
               linestyle='None', markerfacecolor='white', markeredgewidth=1.5,
               zorder=11 if organ == '总计' else 6)
    
    # 轴标签
    ax.set_xlabel(r'$W_i$ - 叶片干重 (g m$^{-2}$)', fontsize=12)
    ax.set_ylabel(r'$R_m$ - 维持呼吸速率 (g CH$_2$O m$^{-2}$ d$^{-1}$)', fontsize=12)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=11)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)
    
    # 参数标注
    param_text = f'$W_{{stem}}$ = {W_stem} g m$^{{-2}}$\n$W_{{root}}$ = {W_root} g m$^{{-2}}$'
    ax.text(0.98, 0.35, param_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('维持呼吸速率对叶片干重的响应', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'maintenance_respiration_sensitivity.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_coefficient_comparison_plot():
    """
    比较不同器官维持呼吸系数的差异
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

    # 器官和对应的呼吸系数（典型值和范围）
    organs = ['叶片', '茎', '根', '果实/籽粒', '花']
    coeffs_mean = np.array([0.015, 0.010, 0.012, 0.008, 0.020])
    coeffs_min = np.array([0.012, 0.008, 0.010, 0.006, 0.016])
    coeffs_max = np.array([0.018, 0.012, 0.014, 0.010, 0.024])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    
    # 设置两个子图的边框
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1.2)
    
    # === 左图：柱状图显示系数对比 ===
    x = np.arange(len(organs))
    width = 0.6
    
    # 绘制柱状图
    bars = ax1.bar(x, coeffs_mean, width, color='0.7', edgecolor='black',
                   linewidth=1.5, label='典型值')
    
    # 添加误差线（显示范围）
    errors = np.array([coeffs_mean - coeffs_min, coeffs_max - coeffs_mean])
    ax1.errorbar(x, coeffs_mean, yerr=errors, fmt='none', ecolor='black',
                capsize=5, capthick=1.5, linewidth=1.5, label='变化范围')
    
    # 在柱顶标注数值
    for i, (mean, bar) in enumerate(zip(coeffs_mean, bars)):
        ax1.text(i, mean + 0.0005, f'{mean:.3f}',
                ha='center', va='bottom', fontsize=9)
    
    # 轴标签
    ax1.set_xlabel('器官', fontsize=12, weight='bold')
    ax1.set_ylabel(r'$r_{m,i}$ (g CH$_2$O g$^{-1}$ d$^{-1}$)', fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(organs, rotation=15, ha='right')
    ax1.set_ylim(0, max(coeffs_max) * 1.15)
    
    # 图例和网格
    ax1.legend(frameon=True, loc='upper right', edgecolor='black', fancybox=False)
    ax1.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, 
            linewidth=0.8, axis='y')
    ax1.set_title('各器官维持呼吸系数对比', fontsize=13, pad=10, weight='bold')
    
    # === 右图：固定干重下的呼吸速率对比 ===
    # 假设每个器官都有100 g m⁻²的干重
    W_fixed = 100  # g m⁻²
    Rm_values = coeffs_mean * W_fixed
    Rm_min = coeffs_min * W_fixed
    Rm_max = coeffs_max * W_fixed
    
    # 填充图案
    hatches = ['', '///', '\\\\\\', 'xxx', '|||']
    colors_pattern = ['0.9', '0.75', '0.6', '0.45', '0.3']
    
    bars2 = ax2.bar(x, Rm_values, width, edgecolor='black', linewidth=1.5)
    
    # 为每个柱子设置不同的填充
    for bar, color, hatch in zip(bars2, colors_pattern, hatches):
        bar.set_facecolor(color)
        bar.set_hatch(hatch)
    
    # 添加误差线
    errors2 = np.array([Rm_values - Rm_min, Rm_max - Rm_values])
    ax2.errorbar(x, Rm_values, yerr=errors2, fmt='none', ecolor='black',
                capsize=5, capthick=1.5, linewidth=1.5)
    
    # 在柱顶标注数值
    for i, val in enumerate(Rm_values):
        ax2.text(i, val + 0.05, f'{val:.2f}',
                ha='center', va='bottom', fontsize=9)
    
    # 轴标签
    ax2.set_xlabel('器官', fontsize=12, weight='bold')
    ax2.set_ylabel(r'$R_m$ (g CH$_2$O m$^{-2}$ d$^{-1}$)', fontsize=11)
    ax2.set_xticks(x)
    ax2.set_xticklabels(organs, rotation=15, ha='right')
    ax2.set_ylim(0, max(Rm_max) * 1.15)
    
    # 网格和标题
    ax2.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, 
            linewidth=0.8, axis='y')
    ax2.set_title(f'固定干重({W_fixed} g m$^{{-2}}$)下的呼吸速率',
                 fontsize=13, pad=10, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'maintenance_respiration_coefficients.{ext}', bbox_inches='tight')
    
    plt.close(fig)


if __name__ == '__main__':
    # 生成器官贡献图
    make_organ_contribution_plot()
    print('器官贡献图生成完成: figures/maintenance_respiration_organs.[png, pdf]')
    
    # 生成干重敏感性分析图
    make_weight_sensitivity_plot()
    print('干重敏感性图生成完成: figures/maintenance_respiration_sensitivity.[png, pdf]')
    
    # 生成呼吸系数对比图
    make_coefficient_comparison_plot()
    print('呼吸系数对比图生成完成: figures/maintenance_respiration_coefficients.[png, pdf]')

