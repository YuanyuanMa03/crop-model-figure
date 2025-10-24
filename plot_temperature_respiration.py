"""
温度对维持呼吸速率影响的可视化
公式：R_m(T) = R_m0 · Q10^((T-T0)/10)

其中：
- R_m(T): 温度T时的维持呼吸速率
- R_m0: 基准温度T0（通常25°C）下的维持呼吸速率
- Q10: 温度系数，作物呼吸时一般取Q10 = 2
- T0: 基准温度（通常25°C）

输出：figures/temperature_respiration_*.{png, pdf}
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def temperature_respiration(T, Rm0, Q10, T0=25):
    """
    计算温度T下的维持呼吸速率
    
    参数:
        T: 温度 (°C)
        Rm0: 基准温度下的维持呼吸速率 (g CH₂O m⁻² d⁻¹)
        Q10: 温度系数
        T0: 基准温度 (°C)
    
    返回:
        Rm: 温度T下的维持呼吸速率 (g CH₂O m⁻² d⁻¹)
    """
    return Rm0 * Q10**((T - T0) / 10)


def make_temperature_response_plot():
    """
    绘制不同Q10值下的温度响应曲线
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

    # 参数
    Rm0 = 5.0  # 基准呼吸速率
    T0 = 25    # 基准温度
    Q10_values = [1.5, 2.0, 2.5, 3.0]  # 不同的Q10值
    
    # 温度范围
    T = np.linspace(0, 40, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['-', '--', '-.', ':']
    colors = ['black', '0.3', '0.5', '0.7']
    markers = ['o', 's', '^', 'd']
    
    # 绘制不同Q10的曲线
    for i, Q10 in enumerate(Q10_values):
        Rm = temperature_respiration(T, Rm0, Q10, T0)
        
        ls = linestyles[i % len(linestyles)]
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        label = f'$Q_{{10}}$ = {Q10:.1f}' + (' (典型值)' if Q10 == 2.0 else '')
        lw = 3 if Q10 == 2.0 else 2.5
        
        ax.plot(T, Rm, color=color, linestyle=ls, linewidth=lw, label=label,
               zorder=10 if Q10 == 2.0 else 5)
        
        # 添加标记点
        sample_indices = np.linspace(20, len(T)-20, 5, dtype=int)
        ax.plot(T[sample_indices], Rm[sample_indices], marker=marker,
               color=color, markersize=6 if Q10 != 2.0 else 7,
               linestyle='None', markerfacecolor='white', markeredgewidth=1.5,
               zorder=11 if Q10 == 2.0 else 6)
    
    # 标注基准点
    ax.plot(T0, Rm0, marker='*', color='black', markersize=15,
           markerfacecolor='white', markeredgewidth=2, zorder=15,
           label=f'基准点 ($T_0$ = {T0}°C)')
    
    # 添加基准线
    ax.axhline(y=Rm0, color='0.7', linestyle='--', linewidth=1, zorder=0,
              alpha=0.5)
    ax.axvline(x=T0, color='0.7', linestyle='--', linewidth=1, zorder=0,
              alpha=0.5)
    
    # 轴标签
    ax.set_xlabel(r'$T$ - 温度 (°C)', fontsize=13)
    ax.set_ylabel(r'$R_m(T)$ - 维持呼吸速率 (g CH$_2$O m$^{-2}$ d$^{-1}$)', fontsize=12)
    
    # 范围
    ax.set_xlim(0, 40)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=10)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)
    
    # 公式标注
    formula = r'$R_m(T) = R_{m0} \cdot Q_{10}^{(T-T_0)/10}$'
    param_text = f'$R_{{m0}}$ = {Rm0:.1f} g CH$_2$O m$^{{-2}}$ d$^{{-1}}$\n$T_0$ = {T0}°C'
    ax.text(0.98, 0.45, formula + '\n\n' + param_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('维持呼吸速率的温度响应', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'temperature_respiration.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_q10_sensitivity_plot():
    """
    绘制Q10值对不同温度下呼吸速率的影响
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

    # 参数
    Rm0 = 5.0
    T0 = 25
    
    # 特定温度
    temperatures = [10, 20, 25, 30, 35]
    
    # Q10范围
    Q10 = np.linspace(1.2, 3.5, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = [':', '-.', '--', '-', '-']
    colors = ['0.7', '0.5', '0.3', 'black', '0.2']
    linewidths = [2, 2, 2, 2.5, 3]
    markers = ['d', '^', 's', 'o', 'p']
    
    # 绘制不同温度的曲线
    for i, T in enumerate(temperatures):
        Rm = temperature_respiration(T, Rm0, Q10, T0)
        
        ls = linestyles[i]
        color = colors[i]
        marker = markers[i]
        lw = linewidths[i]
        
        label = f'$T$ = {T}°C' + (' (基准)' if T == T0 else '')
        
        ax.plot(Q10, Rm, color=color, linestyle=ls, linewidth=lw, label=label)
        
        # 添加标记点
        if T == T0:
            # 基准温度是水平线，只标注一个点
            ax.plot([2.0], [Rm0], marker=marker, color=color, markersize=8,
                   linestyle='None', markerfacecolor='white', markeredgewidth=1.5)
        else:
            sample_indices = np.linspace(30, len(Q10)-30, 4, dtype=int)
            ax.plot(Q10[sample_indices], Rm[sample_indices], marker=marker,
                   color=color, markersize=6, linestyle='None',
                   markerfacecolor='white', markeredgewidth=1.5)
    
    # 标注典型Q10值
    ax.axvline(x=2.0, color='0.7', linestyle='--', linewidth=1.5, 
              zorder=0, alpha=0.6, label='典型$Q_{10}$ = 2.0')
    
    # 轴标签
    ax.set_xlabel(r'$Q_{10}$ - 温度系数', fontsize=13)
    ax.set_ylabel(r'$R_m(T)$ - 维持呼吸速率 (g CH$_2$O m$^{-2}$ d$^{-1}$)', fontsize=12)
    
    # 范围
    ax.set_xlim(1.2, 3.5)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=10, ncol=2)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)
    
    # 参数标注
    param_text = f'$R_{{m0}}$ = {Rm0:.1f} g CH$_2$O m$^{{-2}}$ d$^{{-1}}$\n$T_0$ = {T0}°C'
    ax.text(0.98, 0.35, param_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('不同温度下呼吸速率对$Q_{10}$的敏感性', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'temperature_respiration_q10.{ext}', bbox_inches='tight')
    
    plt.close(fig)


def make_relative_change_plot():
    """
    绘制相对于基准温度的呼吸速率变化倍数
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

    # 参数
    T0 = 25
    Q10_values = [1.5, 2.0, 2.5, 3.0]
    
    # 温度范围
    T = np.linspace(0, 40, 300)
    
    fig, ax = plt.subplots()
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)
    
    # 黑白线型样式
    linestyles = ['-', '--', '-.', ':']
    colors = ['black', '0.3', '0.5', '0.7']
    markers = ['o', 's', '^', 'd']
    
    # 绘制相对变化曲线
    for i, Q10 in enumerate(Q10_values):
        # 相对变化 = Rm(T) / Rm0 = Q10^((T-T0)/10)
        relative_change = Q10**((T - T0) / 10)
        
        ls = linestyles[i % len(linestyles)]
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        label = f'$Q_{{10}}$ = {Q10:.1f}' + (' (典型值)' if Q10 == 2.0 else '')
        lw = 3 if Q10 == 2.0 else 2.5
        
        ax.plot(T, relative_change, color=color, linestyle=ls, linewidth=lw, 
               label=label, zorder=10 if Q10 == 2.0 else 5)
        
        # 添加标记点
        sample_indices = np.linspace(20, len(T)-20, 5, dtype=int)
        ax.plot(T[sample_indices], relative_change[sample_indices], marker=marker,
               color=color, markersize=6 if Q10 != 2.0 else 7,
               linestyle='None', markerfacecolor='white', markeredgewidth=1.5,
               zorder=11 if Q10 == 2.0 else 6)
    
    # 添加基准线 (倍数=1)
    ax.axhline(y=1, color='0.5', linestyle='-', linewidth=1.5, zorder=0,
              label='基准倍数 = 1')
    ax.axvline(x=T0, color='0.7', linestyle='--', linewidth=1, zorder=0,
              alpha=0.5)
    
    # 标注一些关键倍数
    for mult in [0.5, 2, 4]:
        ax.axhline(y=mult, color='0.8', linestyle=':', linewidth=0.8, 
                  zorder=0, alpha=0.5)
    
    # 轴标签
    ax.set_xlabel(r'$T$ - 温度 (°C)', fontsize=13)
    ax.set_ylabel(r'$R_m(T) / R_{m0}$ - 相对呼吸速率', fontsize=12)
    
    # 范围
    ax.set_xlim(0, 40)
    ax.set_ylim(0, None)
    
    # 图例
    ax.legend(frameon=True, loc='upper left', edgecolor='black', 
              fancybox=False, fontsize=10)
    
    # 网格
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.5, linewidth=0.8)
    
    # 公式标注
    formula = r'$\frac{R_m(T)}{R_{m0}} = Q_{10}^{(T-T_0)/10}$'
    param_text = f'$T_0$ = {T0}°C'
    ax.text(0.98, 0.95, formula + '\n' + param_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # 标题
    ax.set_title('相对于基准温度的呼吸速率变化', fontsize=14, pad=12, weight='bold')
    
    plt.tight_layout()
    
    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'temperature_respiration_relative.{ext}', bbox_inches='tight')
    
    plt.close(fig)


if __name__ == '__main__':
    # 生成温度响应曲线
    make_temperature_response_plot()
    print('温度响应图生成完成: figures/temperature_respiration.[png, pdf]')
    
    # 生成Q10敏感性分析
    make_q10_sensitivity_plot()
    print('Q10敏感性图生成完成: figures/temperature_respiration_q10.[png, pdf]')
    
    # 生成相对变化图
    make_relative_change_plot()
    print('相对变化图生成完成: figures/temperature_respiration_relative.[png, pdf]')

