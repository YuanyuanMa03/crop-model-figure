"""
Rubisco呼吸速率与CO₂和O₂浓度的关系可视化
公式：R_p = R_{pmax} * [O₂/Ks] / [(CO₂/Kc) + (1 + O₂/Ko)]

输出：figures/rubisco_rp.[png, svg, pdf, eps]
- PNG：300 dpi，适用于书籍排版
- SVG/PDF/EPS：矢量格式，适合印刷与放大

可编辑参数：Rpmax, Ks, Kc, Ko, CO2范围, O2浓度
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def rubisco_rp(CO2, O2, Rpmax, Ks, Kc, Ko):
    """
    计算Rubisco呼吸速率
    
    参数:
        CO2: CO₂浓度 (μmol mol⁻¹ 或 ppm)
        O2: O₂浓度 (mmol mol⁻¹ 或 %)
        Rpmax: 最大呼吸速率 (μmol CO₂ m⁻² s⁻¹)
        Ks: O₂的Michaelis常数
        Kc: CO₂的Michaelis常数
        Ko: O₂的抑制常数
    """
    numerator = (O2 / Ks)
    denominator = (CO2 / Kc) + (1 + O2 / Ko)
    return Rpmax * numerator / denominator

def make_plot(
    Rpmax: float = 20.0,        # 最大呼吸速率
    Ks: float = 2.5,            # O₂的Michaelis常数 (mmol mol⁻¹)
    Kc: float = 40.0,           # CO₂的Michaelis常数 (μmol mol⁻¹)
    Ko: float = 25.0,           # O₂的抑制常数 (mmol mol⁻¹)
    co2_range: tuple = (0, 1000),  # CO₂浓度范围 (μmol mol⁻¹)
    o2_levels: list = None,     # 不同的O₂浓度水平 (mmol mol⁻¹)
):
    # 默认O₂浓度水平（21%约等于210 mmol mol⁻¹）
    if o2_levels is None:
        o2_levels = [10, 21, 30, 40]  # 不同O₂百分比（转换为mmol mol⁻¹需×10）
    
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
        'figure.figsize': (7, 5),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # CO₂浓度数组
    co2 = np.linspace(co2_range[0] + 1, co2_range[1], 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框颜色为黑色
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)

    # 黑白线型样式
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'd']
    colors = ['black', '0.3', '0.5', '0.7']
    
    # 绘制不同O₂浓度下的曲线
    for i, o2_pct in enumerate(o2_levels):
        o2 = o2_pct * 10  # 转换为 mmol mol⁻¹
        rp = rubisco_rp(co2, o2, Rpmax, Ks, Kc, Ko)
        
        ls = linestyles[i % len(linestyles)]
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        ax.plot(co2, rp, color=color, linestyle=ls, linewidth=2.5,
                label=f'O$_2$ = {o2_pct}%')
        
        # 添加一些标记点
        sample_indices = np.linspace(30, len(co2)-30, 5, dtype=int)
        ax.plot(co2[sample_indices], rp[sample_indices], marker=marker,
                color=color, markersize=6, linestyle='None',
                markerfacecolor='white', markeredgewidth=1.5)

    # 轴标签
    ax.set_xlabel(r'CO$_2$浓度 (μmol mol$^{-1}$)', fontsize=13)
    ax.set_ylabel(r'$R_p$ (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=13)

    # 范围
    ax.set_xlim(co2_range)
    ax.set_ylim(0, None)

    # 图例与网格（黑白风格）
    ax.legend(frameon=True, loc='best', edgecolor='black', fancybox=False)
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)

    # 公式标注
    formula = r'$R_p = R_{p,max} \cdot \frac{O_2/K_s}{(CO_2/K_c) + (1 + O_2/K_o)}$'
    ax.text(0.98, 0.95, formula, transform=ax.transAxes,
            ha='right', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))

    # 标题
    ax.set_title('Rubisco呼吸速率对CO$_2$浓度的响应', fontsize=14, pad=12, weight='bold')

    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'rubisco_rp.{ext}', bbox_inches='tight')

    plt.close(fig)


def make_3d_plot(
    Rpmax: float = 20.0,
    Ks: float = 2.5,
    Kc: float = 40.0,
    Ko: float = 25.0,
):
    """
    创建3D曲面图展示Rp对CO₂和O₂的双重依赖
    """
    from mpl_toolkits.mplot3d import Axes3D
    
    # 创建输出目录
    out_dir = Path('figures')
    out_dir.mkdir(exist_ok=True)

    # 高质量出版参数
    plt.rcParams.update({
        'font.size': 11,
        'font.sans-serif': ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'figure.figsize': (8, 6),
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 创建网格
    co2 = np.linspace(1, 1000, 100)
    o2_pct = np.linspace(5, 50, 100)
    CO2, O2_PCT = np.meshgrid(co2, o2_pct)
    O2 = O2_PCT * 10  # 转换为 mmol mol⁻¹
    
    # 计算Rp
    RP = rubisco_rp(CO2, O2, Rpmax, Ks, Kc, Ko)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # 黑白风格的曲面图
    surf = ax.plot_surface(CO2, O2_PCT, RP, cmap='gray', 
                           edgecolor='black', linewidth=0.2, alpha=0.8,
                           antialiased=True)

    # 轴标签
    ax.set_xlabel(r'CO$_2$ (μmol mol$^{-1}$)', fontsize=11, labelpad=10)
    ax.set_ylabel(r'O$_2$ (%)', fontsize=11, labelpad=10)
    ax.set_zlabel(r'$R_p$ (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=11, labelpad=10)

    # 标题
    ax.set_title('Rubisco呼吸速率的CO$_2$-O$_2$响应曲面', fontsize=13, pad=15, weight='bold')

    # 添加颜色条
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label(r'$R_p$', fontsize=11)

    # 调整视角
    ax.view_init(elev=25, azim=45)

    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'rubisco_rp_3d.{ext}', bbox_inches='tight', dpi=300)

    plt.close(fig)


if __name__ == '__main__':
    # 生成2D图
    make_plot()
    print('2D图生成完成: figures/rubisco_rp.[png, pdf]')
    
    # 生成3D图
    make_3d_plot()
    print('3D图生成完成: figures/rubisco_rp_3d.[png, pdf]')

