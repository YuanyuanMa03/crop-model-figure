"""
作物呼吸速率与总光合速率的线性关系可视化
公式：R_p = α · P_g

输出：figures/rp_vs_pg.[png, svg, pdf, eps]
- PNG：300 dpi，适用于书籍排版
- SVG/PDF/EPS：矢量格式，适合印刷与放大

可编辑参数：alpha, alpha_min, alpha_max, unit, pg_max
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（macOS 优先使用 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STSong', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def make_plot(
    alpha: float = 0.45,
    alpha_min: float = 0.30,
    alpha_max: float = 0.60,
    unit: str = r'μmol CO$_2$ m$^{-2}$ s$^{-1}$',
    pg_max: float = 40.0,
):
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
        'figure.figsize': (6.5, 4.5),
        'axes.linewidth': 1.2,
        'lines.linewidth': 2,
        'savefig.dpi': 300,
        # 使用 TrueType 字体以获得更清晰的矢量文本
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    # 数据
    x = np.linspace(0, pg_max, 200)
    y_typ = alpha * x
    y_min = alpha_min * x
    y_max = alpha_max * x

    fig, ax = plt.subplots()
    
    # 设置边框颜色为黑色
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.2)

    # α 范围阴影带（黑白风格）
    ax.fill_between(x, y_min, y_max, color='0.75', alpha=0.5,
                    label=f'α范围 {alpha_min:.2f}–{alpha_max:.2f}')

    # 典型 α 的直线（黑色实线）
    ax.plot(x, y_typ, color='black', linestyle='-', linewidth=2.5,
            label=f'典型α = {alpha:.2f}')

    # 示例数据点（沿典型线加小噪声）
    rng = np.random.default_rng(42)
    n = 12
    pg_points = rng.uniform(0.1 * pg_max, 0.95 * pg_max, n)
    rp_points = alpha * pg_points + rng.normal(0, 0.03 * alpha * pg_max, n)
    ax.scatter(pg_points, rp_points, s=50, color='white',
               edgecolor='black', linewidth=1.5, label='示例数据点')

    # 轴与单位
    ax.set_xlabel(r'$P_g$ (' + unit + ')')
    ax.set_ylabel(r'$R_p$ (' + unit + ')')

    # 比例与范围
    ax.set_xlim(0, pg_max)
    ax.set_ylim(0, alpha_max * pg_max * 1.05)

    # 图例与网格（黑白风格）
    ax.legend(frameon=True, loc='upper left', edgecolor='black')
    ax.grid(True, which='major', linestyle=':', color='0.5', alpha=0.7, linewidth=0.8)

    # 公式标注
    ax.text(0.98, 0.06, r'$R_p = \alpha \cdot P_g$', transform=ax.transAxes,
            ha='right', va='bottom', fontsize=13)

    # 标题
    ax.set_title('作物呼吸速率与总光合速率的线性关系', fontsize=14, pad=12)

    # 保存PNG和PDF格式
    for ext in ['png', 'pdf']:
        fig.savefig(out_dir / f'rp_vs_pg.{ext}', bbox_inches='tight')

    plt.close(fig)


if __name__ == '__main__':
    make_plot()
    print('生成完成: figures/rp_vs_pg.[png, pdf]')