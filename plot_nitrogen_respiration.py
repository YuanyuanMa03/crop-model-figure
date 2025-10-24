"""
氮含量对维持呼吸系数影响的可视化
公式：r'_{m,i} = r_{ref} × (N_i / N_{ref})

其中：
- r'_{m,i}: 当前氮含量下的维持呼吸系数
- r_{ref}: 参考氮含量下的维持呼吸系数
- N_i: 当前氮含量
- N_{ref}: 参考氮含量

输出：figures/nitrogen_respiration_*.{png, pdf}
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def nitrogen_respiration_coefficient(Ni, r_ref, N_ref):
    """
    计算当前氮含量下的维持呼吸系数
    
    参数:
        Ni: 当前氮含量 (g N g⁻¹干重 或 %)
        r_ref: 参考呼吸系数 (g CH₂O g⁻¹ d⁻¹)
        N_ref: 参考氮含量 (g N g⁻¹干重 或 %)
    
    返回:
        r_mi: 当前氮含量下的呼吸系数 (g CH₂O g⁻¹ d⁻¹)
    """
    return r_ref * (Ni / N_ref)


def make_nitrogen_response_plot():
    """
    绘制维持呼吸系数对氮含量的响应曲线
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

    # 参考值（典型叶片）
    N_ref = 3.0  # 参考氮含量 (%)
    r_ref_values = [0.012, 0.015, 0.018]  # 不同的参考呼吸系数
    
    # 氮含量范围 (%)
    Ni = np.linspace(0.5, 6.0, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['--', '-', '-.']
    colors = ['0.5', 'black', '0.3']
    markers = ['s', 'o', '^']
    linewidths = [2, 3, 2]
    
    # 绘制不同参考呼吸系数的曲线
    for i, r_ref in enumerate(r_ref_values):
        r_mi = nitrogen_respiration_coefficient(Ni, r_ref, N_ref)
        
        ls = linestyles[i]
        color = colors[i]
        marker = markers[i]
        lw = linewidths[i]
        
        label = f'$r_{{ref}}$ = {r_ref:.3f}' + (' (典型值)' if r_ref == 0.015 else '')
        
        ax.plot(Ni, r_mi, color=color, linestyle=ls, linewidth=lw, label=label,
               zorder=10 if r_ref == 0.015 else 5)
        
        # 添加标记点
        sample_indices = np.linspace(30, len(Ni)-30, 5, dtype=int)
        ax.plot(Ni[sample_indices], r_mi[sample_indices], marker=marker,
               color=color, markersize=6 if r_ref != 0.015 else 7,
               linestyle='None', markerfacecolor='white', markeredgewidth=1.5,
               zorder=11 if r_ref == 0.015 else 6)
    
    # 标注参考点
    r_ref_typical = 0.015
    ax.plot(N_ref, r_ref_typical, marker='*', color='black', markersize=15,
           markerfacecolor='white', markeredgewidth=2, zorder=15,
           label=f'参考点 ($N_{{ref}}$ = {N_ref:.1f}%)')
    
    # 添加参考线
    ax.axhline(y=r_ref_typical, color='0.7', linestyle=':', linewidth=1, 
              zorder=0, alpha=0.5)
    ax.axvline(x=N_ref, color='0.7', linestyle=':', linewidth=1, 
              zorder=0, alpha=0.5)
    
    # 轴标签
    ax.set_xlabel(r'$N_i$ - 氮含量 (%)', fontsize=13)
    ax.set_ylabel(r"$r'_{m,i}$ - 维持呼吸系数 (g CH$_2$O g$^{-1}$ d$^{-1}$)", fontsize=11)
    
    # 范围
    ax.set_xlim(0.5, 6.0)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=10)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)
    
    # 公式标注
    formula = r"$r'_{m,i} = r_{ref} \times \frac{N_i}{N_{ref}}$"
    param_text = f'$N_{{ref}}$ = {N_ref:.1f}%'
    ax.text(0.98, 0.35, formula + '\n' + param_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('维持呼吸系数对氮含量的响应', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'nitrogen_respiration.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_organ_comparison_plot():
    """
    绘制不同器官在不同氮含量下的呼吸系数对比
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

    # 不同器官的参考值
    organs = ['叶片', '茎', '根']
    r_ref_organs = [0.015, 0.010, 0.012]  # 各器官参考呼吸系数
    N_ref_organs = [3.0, 1.5, 2.0]  # 各器官参考氮含量 (%)
    
    # 氮含量范围
    Ni = np.linspace(0.5, 5.0, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['-', '--', '-.']
    colors = ['black', '0.4', '0.6']
    markers = ['o', 's', '^']
    linewidths = [2.5, 2.5, 2.5]
    
    # 绘制各器官曲线
    for i, (organ, r_ref, N_ref) in enumerate(zip(organs, r_ref_organs, N_ref_organs)):
        r_mi = nitrogen_respiration_coefficient(Ni, r_ref, N_ref)
        
        ls = linestyles[i]
        color = colors[i]
        marker = markers[i]
        lw = linewidths[i]
        
        ax.plot(Ni, r_mi, color=color, linestyle=ls, linewidth=lw, label=organ)
        
        # 添加标记点
        sample_indices = np.linspace(30, len(Ni)-30, 5, dtype=int)
        ax.plot(Ni[sample_indices], r_mi[sample_indices], marker=marker,
               color=color, markersize=6, linestyle='None',
               markerfacecolor='white', markeredgewidth=1.5)
        
        # 标注各器官的参考点
        ax.plot(N_ref, r_ref, marker=marker, color=color, markersize=10,
               markerfacecolor='white', markeredgewidth=2, zorder=10)
    
    # 轴标签
    ax.set_xlabel(r'$N_i$ - 氮含量 (%)', fontsize=13)
    ax.set_ylabel(r"$r'_{m,i}$ - 维持呼吸系数 (g CH$_2$O g$^{-1}$ d$^{-1}$)", fontsize=11)
    
    # 范围
    ax.set_xlim(0.5, 5.0)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=11)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)
    
    # 公式标注
    formula = r"$r'_{m,i} = r_{ref} \times \frac{N_i}{N_{ref}}$"
    ax.text(0.98, 0.95, formula, transform=ax.transAxes,
            ha='right', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('不同器官维持呼吸系数的氮含量响应', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'nitrogen_respiration_organs.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_relative_change_plot():
    """
    绘制相对于参考氮含量的呼吸系数变化倍数
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

    # 不同参考氮含量
    N_ref_values = [2.0, 3.0, 4.0]
    
    # 氮含量范围 (%)
    Ni = np.linspace(0.5, 6.0, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['--', '-', '-.']
    colors = ['0.5', 'black', '0.3']
    markers = ['s', 'o', '^']
    linewidths = [2, 3, 2]
    
    # 绘制相对变化曲线
    for i, N_ref in enumerate(N_ref_values):
        # 相对变化 = r'_mi / r_ref = Ni / N_ref
        relative_change = Ni / N_ref
        
        ls = linestyles[i]
        color = colors[i]
        marker = markers[i]
        lw = linewidths[i]
        
        label = f'$N_{{ref}}$ = {N_ref:.1f}%' + (' (典型值)' if N_ref == 3.0 else '')
        
        ax.plot(Ni, relative_change, color=color, linestyle=ls, linewidth=lw, 
               label=label, zorder=10 if N_ref == 3.0 else 5)
        
        # 添加标记点
        sample_indices = np.linspace(30, len(Ni)-30, 5, dtype=int)
        ax.plot(Ni[sample_indices], relative_change[sample_indices], marker=marker,
               color=color, markersize=6 if N_ref != 3.0 else 7,
               linestyle='None', markerfacecolor='white', markeredgewidth=1.5,
               zorder=11 if N_ref == 3.0 else 6)
    
    # 添加基准线 (倍数=1)
    ax.axhline(y=1, color='0.5', linestyle='-', linewidth=1.5, zorder=0,
              label='基准倍数 = 1')
    
    # 标注一些关键倍数
    for mult in [0.5, 1.5, 2]:
        ax.axhline(y=mult, color='0.8', linestyle=':', linewidth=0.8, 
                  zorder=0, alpha=0.5)
    
    # 轴标签
    ax.set_xlabel(r'$N_i$ - 当前氮含量 (%)', fontsize=13)
    ax.set_ylabel(r"$r'_{m,i} / r_{ref}$ - 相对呼吸系数", fontsize=12)
    
    # 范围
    ax.set_xlim(0.5, 6.0)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=10)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, linewidth=0.8)
    
    # 公式标注
    formula = r"$\frac{r'_{m,i}}{r_{ref}} = \frac{N_i}{N_{ref}}$"
    ax.text(0.98, 0.95, formula, transform=ax.transAxes,
            ha='right', va='top', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('相对于参考氮含量的呼吸系数变化', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'nitrogen_respiration_relative.{ext}', bbox_inches='tight')
    
    plt.close(fig)


if __name__ == '__main__':
    # 生成氮含量响应曲线
    make_nitrogen_response_plot()
    print('氮含量响应图生成完成: figures/nitrogen_respiration.[png, pdf]')
    
    # 生成器官对比图
    make_organ_comparison_plot()
    print('器官对比图生成完成: figures/nitrogen_respiration_organs.[png, pdf]')
    
    # 生成相对变化图
    make_relative_change_plot()
    print('相对变化图生成完成: figures/nitrogen_respiration_relative.[png, pdf]')

