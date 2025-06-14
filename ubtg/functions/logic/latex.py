import matplotlib
from matplotlib import pyplot as plt
from ubtg import config


def _function(
        text: str,
        font_size: int = 30,
        transparent: bool = False,
        dpi: int = 300,
        output_path: str = f'{config.TEMP_PATH}latex.png'
) -> str:
    matplotlib.use('Agg')
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, text, fontsize=font_size, ha='center', va='center')
    ax.axis('off')
    plt.savefig(output_path, dpi=dpi, transparent=transparent)
    plt.close()
    return output_path