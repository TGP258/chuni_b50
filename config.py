import os
from typing import Dict, List, Tuple


class Config:
    # 路径配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH = os.path.join(BASE_DIR, 'data', 'input.csv')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

    # 默认使用哪个模板
    # 单曲背板
    DEFAULT_TEMPLATE = 'background.png'
    # 分表背板
    DEFAULT_BACKGROUND = 'plate.png'
    # 绘制范围配置
    START_ROW = 2  # 从第2行开始(跳过标题行)
    END_ROW = 51  # 到第51行结束

    # CSV列名映射到绘制位置的配置
    # 格式: {'csv_column': (x, y, font_size, color, font_path)}
    DRAW_CONFIG = {
        'song_name': (100, 50, 36, (255, 255, 255), 'NotoSansCJK-Regular.ttc'),
        'level': (100, 100, 28, (255, 255, 0), 'NotoSansCJK-Regular.ttc'),
        'level_index': (150, 100, 28, (255, 255, 0), None),
        'score': (100, 150, 28, (255, 255, 255), 'NotoSansCJK-Regular.ttc'),
        'rating': (100, 200, 28, (0, 255, 255), 'NotoSansCJK-Regular.ttc'),
        'rank': (100, 250, 48, (255, 215, 0), 'NotoSansCJK-Regular.ttc'),
        'clear': (300, 100, 24, (0, 255, 0), 'NotoSansCJK-Regular.ttc'),
        'full_combo': (300, 150, 24, (0, 255, 0), 'NotoSansCJK-Regular.ttc'),
        'play_time': (300, 200, 20, (200, 200, 200), 'NotoSansCJK-Regular.ttc')
    }


    # 图片输出配置
    FONT_DIR = os.path.join(BASE_DIR, 'font')
    #字体配置
    OUTPUT_IMAGE_SIZE = (400, 300)  # 输出图片尺寸
    OUTPUT_QUALITY = 95  # 输出图片质量(1-100)
    ITEMS_PER_PAGE = 50  # 每张图片显示多少条记录，方便后面扩展B100 B30功能