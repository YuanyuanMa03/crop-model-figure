"""
净光合速率公式可视化
公式：A_n = V_c - 0.5·V_o - R_d

其中：
- A_n: 净光合速率
- V_c: Rubisco羧化速率
- V_o: Rubisco加氧速率  
- R_d: 暗呼吸速率

输出：figures/net_photosynthesis.[png, svg, pdf, eps]
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def net_photosynthesis(Vc, Vo, Rd):
    """
    计算净光合速率
    
    参数:
        Vc: Rubisco羧化速率 (μmol CO₂ m⁻² s⁻¹)
        Vo: Rubisco加氧速率 (μmol O₂ m⁻² s⁻¹)
        Rd: 暗呼吸速率 (μmol CO₂ m⁻² s⁻¹)
    
    返回:
        An: 净光合速率 (μmol CO₂ m⁻² s⁻¹)
    """
    return Vc - 0.5 * Vo - Rd


def make_component_plot(
    Vc_max: float = 100.0,
    Vo_levels: list = None,
    Rd: float = 2.0,
):
    """
    绘制An的组分分析图，展示各部分对净光合的贡献
    """
    if Vo_levels is None:
        Vo_levels = [0, 20, 40, 60]  # 不同的加氧速率水平
    
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

    # Vc范围
    Vc = np.linspace(0, Vc_max, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框颜色为黑色
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)

    # 黑白线型样式
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'd']
    colors = ['black', '0.3', '0.5', '0.7']
    
    # 绘制不同Vo水平下的An曲线
    for i, Vo in enumerate(Vo_levels):
        An = net_photosynthesis(Vc, Vo, Rd)
        
        ls = linestyles[i % len(linestyles)]
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        label = f'$V_o$ = {Vo:.0f}' if Vo > 0 else '$V_o$ = 0 (无光呼吸)'
        ax.plot(Vc, An, color=color, linestyle=ls, linewidth=2.5, label=label)
        
        # 添加标记点
        sample_indices = np.linspace(30, len(Vc)-30, 5, dtype=int)
        ax.plot(Vc[sample_indices], An[sample_indices], marker=marker,
                color=color, markersize=6, linestyle='None',
                markerfacecolor='white', markeredgewidth=1.5)

    # 添加参考线：Vc线（无呼吸损失时的理论最大值）
    ax.plot(Vc, Vc, color='0.8', linestyle=':', linewidth=2, 
            label='理论最大值 ($V_c$)', zorder=0)

    # 轴标签
    ax.set_xlabel(r'$V_c$ - Rubisco羧化速率 (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=12)
    ax.set_ylabel(r'$A_n$ - 净光合速率 (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=12)

    # 范围
    ax.set_xlim(0, Vc_max)
    ax.set_ylim(None, None)
    
    # 添加y=0参考线
    ax.axhline(y=0, color='0.5', linestyle='-', linewidth=0.8, zorder=0)

    # 图例与网格
    ax.legend(frameon=True, loc='lower right', edgecolor='black', 
              fancybox=False, fontsize=10)
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)

    # 公式标注
    formula = r'$A_n = V_c - 0.5 \cdot V_o - R_d$'
    param_text = f'($R_d$ = {Rd:.1f})'
    ax.text(0.98, 0.06, formula + '\n' + param_text, transform=ax.transAxes,
            ha='right', va='bottom', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))

    # 标题
    ax.set_title('净光合速率的组分分析', fontsize=14, pad=12, weight='bold')

    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'net_photosynthesis.{ext}', bbox_inches='tight')

    plt.close(fig)


def make_stacked_plot(
    Vc_max: float = 100.0,
    Vo: float = 40.0,
    Rd: float = 2.0,
):
    """
    绘制堆积图，展示光合速率的各个组分
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

    # Vc范围
    Vc = np.linspace(0, Vc_max, 300)
    
    # 计算各组分
    photorespiration = -0.5 * Vo  # 光呼吸损失（负值）
    dark_respiration = -Rd         # 暗呼吸损失（负值）
    An = net_photosynthesis(Vc, Vo, Rd)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)

    # 绘制各组分（使用不同的灰度和图案）
    # 羧化速率（总光合）
    ax.fill_between(Vc, 0, Vc, color='0.85', alpha=0.8, 
                    label=r'$V_c$ (羧化速率)', edgecolor='black', linewidth=0.5)
    
    # 光呼吸损失（从Vc往下）
    ax.fill_between(Vc, Vc, Vc + photorespiration, color='0.6', alpha=0.7,
                    hatch='///', label=r'$-0.5 \cdot V_o$ (光呼吸损失)',
                    edgecolor='black', linewidth=0.5)
    
    # 暗呼吸损失
    ax.fill_between(Vc, Vc + photorespiration, Vc + photorespiration + dark_respiration,
                    color='0.4', alpha=0.7, hatch='\\\\\\',
                    label=r'$-R_d$ (暗呼吸损失)', edgecolor='black', linewidth=0.5)
    
    # 净光合速率线
    ax.plot(Vc, An, color='black', linestyle='-', linewidth=3,
            label=r'$A_n$ (净光合速率)', zorder=10)
    
    # 添加标记点
    sample_indices = np.linspace(30, len(Vc)-30, 5, dtype=int)
    ax.plot(Vc[sample_indices], An[sample_indices], marker='o',
            color='black', markersize=7, linestyle='None',
            markerfacecolor='white', markeredgewidth=2, zorder=11)

    # 轴标签
    ax.set_xlabel(r'$V_c$ - Rubisco羧化速率 (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=12)
    ax.set_ylabel(r'光合速率组分 (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=12)

    # 范围
    ax.set_xlim(0, Vc_max)
    ax.set_ylim(min(An) * 1.1, Vc_max * 1.05)
    
    # 零线
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, zorder=0)

    # 图例与网格
    ax.legend(frameon=True, loc='upper center', edgecolor='black', 
              fancybox=False, fontsize=10, ncol=2)
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, linewidth=0.8)

    # 参数标注
    param_text = f'$V_o$ = {Vo:.0f}, $R_d$ = {Rd:.1f}'
    ax.text(0.98, 0.95, param_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor='black', linewidth=1))

    # 标题
    ax.set_title('净光合速率的组分堆积分析', fontsize=14, pad=12, weight='bold')

    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'net_photosynthesis_stacked.{ext}', bbox_inches='tight')

    plt.close(fig)


def make_sensitivity_plot(
    Vc: float = 80.0,
    Vo_max: float = 80.0,
    Rd_levels: list = None,
):
    """
    绘制An对Vo的敏感性分析（不同Rd水平）
    """
    if Rd_levels is None:
        Rd_levels = [0, 1, 2, 4]
    
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

    # Vo范围
    Vo = np.linspace(0, Vo_max, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)

    # 黑白线型样式
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'd']
    colors = ['black', '0.3', '0.5', '0.7']
    
    # 绘制不同Rd水平下的An曲线
    for i, Rd in enumerate(Rd_levels):
        An = net_photosynthesis(Vc, Vo, Rd)
        
        ls = linestyles[i % len(linestyles)]
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        label = f'$R_d$ = {Rd:.1f}' if Rd > 0 else '$R_d$ = 0'
        ax.plot(Vo, An, color=color, linestyle=ls, linewidth=2.5, label=label)
        
        # 添加标记点
        sample_indices = np.linspace(30, len(Vo)-30, 5, dtype=int)
        ax.plot(Vo[sample_indices], An[sample_indices], marker=marker,
                color=color, markersize=6, linestyle='None',
                markerfacecolor='white', markeredgewidth=1.5)

    # 轴标签
    ax.set_xlabel(r'$V_o$ - Rubisco加氧速率 (μmol O$_2$ m$^{-2}$ s$^{-1}$)', fontsize=12)
    ax.set_ylabel(r'$A_n$ - 净光合速率 (μmol CO$_2$ m$^{-2}$ s$^{-1}$)', fontsize=12)

    # 范围
    ax.set_xlim(0, Vo_max)
    
    # 零线
    ax.axhline(y=0, color='0.5', linestyle='-', linewidth=0.8, zorder=0)

    # 图例与网格
    ax.legend(frameon=True, loc='upper right', edgecolor='black', 
              fancybox=False, fontsize=10)
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)

    # 公式标注
    formula = r'$A_n = V_c - 0.5 \cdot V_o - R_d$'
    param_text = f'($V_c$ = {Vc:.0f})'
    ax.text(0.02, 0.65, formula + '\n' + param_text, transform=ax.transAxes,
            ha='left', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))

    # 标题
    ax.set_title('净光合速率对加氧速率的响应', fontsize=14, pad=12, weight='bold')

    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'net_photosynthesis_vo_response.{ext}', bbox_inches='tight')

    plt.close(fig)


if __name__ == '__main__':
    # 生成组分分析图
    make_component_plot()
    print('组分分析图生成完成: figures/net_photosynthesis.[png, pdf]')
    
    # 生成堆积图
    make_stacked_plot()
    print('堆积分析图生成完成: figures/net_photosynthesis_stacked.[png, pdf]')
    
    # 生成敏感性分析图
    make_sensitivity_plot()
    print('敏感性分析图生成完成: figures/net_photosynthesis_vo_response.[png, pdf]')

