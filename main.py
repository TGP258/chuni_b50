import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from config import Config
import time

class MusicGameScoreRenderer:
    def __init__(self):
        self.config = Config()
        self._ensure_dirs()
        # 预加载字体
        self.font_cache = {}

    def _ensure_dirs(self):
        """确保所需目录存在"""
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.config.TEMPLATE_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.config.CSV_PATH), exist_ok=True)

    def _get_font(self, font_name, font_size):
        """获取字体对象，带缓存"""
        cache_key = f"{font_name}_{font_size}"
        if cache_key not in self.font_cache:
            try:
                font_path = os.path.join(self.config.FONT_DIR, font_name)
                if os.path.exists(font_path):
                    self.font_cache[cache_key] = ImageFont.truetype(font_path, font_size)
                else:
                    # 尝试使用系统回退字体
                    self.font_cache[cache_key] = ImageFont.truetype("arialuni.ttf", font_size)
            except:
                # 最终回退到默认字体
                self.font_cache[cache_key] = ImageFont.load_default()
        return self.font_cache[cache_key]
    # 这一块是0.0.1版的
    # def load_data(self, csv_path: str = None) -> pd.DataFrame:
    #     """加载CSV数据"""
    #     path = csv_path or self.config.CSV_PATH
    #     try:
    #         # 读取CSV，跳过标题行后的第一行(因为START_ROW=2表示从第2行开始)
    #         df = pd.read_csv(path, skiprows=1, nrows=self.config.END_ROW - 1)
    #
    #         # 重新设置列名(因为skiprows=1会丢失原列名)
    #         df.columns = [
    #             'id', 'song_name', 'level', 'level_index', 'score', 'rating',
    #             'over_power', 'clear', 'full_combo', 'full_chain', 'rank',
    #             'upload_time', 'play_time'
    #         ]
    #
    #         return df
    #     except Exception as e:
    #         raise Exception(f"无法加载CSV文件: {e}")
    def load_data(self, csv_path: str = None) -> pd.DataFrame:
        """加载CSV数据，确保正确处理中文编码"""
        path = csv_path or self.config.CSV_PATH
        try:
            # 尝试多种编码方式
            encodings = ['utf-8', 'shift_jis', 'gbk', 'big5']
            for encoding in encodings:
                try:
                    df = pd.read_csv(path, skiprows=1, nrows=self.config.END_ROW - 1, encoding=encoding)
                    df.columns = [
                        'id', 'song_name', 'level', 'level_index', 'score', 'rating',
                        'over_power', 'clear', 'full_combo', 'full_chain', 'rank',
                        'upload_time', 'play_time'
                    ]
                    return df
                except UnicodeDecodeError:
                    continue
            raise ValueError("无法确定CSV文件的编码，尝试过的编码: " + ", ".join(encodings))
        except Exception as e:
            raise Exception(f"无法加载CSV文件: {e}")

    start_time = time.time()
    def render_score_card(self, data: dict, template_name: str = None) -> Image.Image:
        """渲染单张成绩卡片"""
        # 加载模板图片
        template_path = os.path.join(
            self.config.TEMPLATE_DIR,
            template_name or self.config.DEFAULT_TEMPLATE
        )

        try:
            if os.path.exists(template_path):
                image = Image.open(template_path)
            else:
                # 如果没有模板，创建一个蓝白色背景图片
                image = Image.new('RGB', self.config.OUTPUT_IMAGE_SIZE, color=(248, 248, 255))
        except Exception as e:
            raise Exception(f"无法加载模板图片: {e}")

        draw = ImageDraw.Draw(image)
        # 转换难度


        # 绘制每个配置的字段
        for field, config in self.config.DRAW_CONFIG.items():
            if field in data and not pd.isna(data[field]):
                x, y, font_size, color, font_path = config
                value = str(data[field])

                # 特殊字段处理
                if field == 'level':
                    value = f"Lv.{data['level']}"
                elif field == 'clear' and data[field] == 'clear':
                    value = "CLEAR"
                elif field == 'full_combo' and data[field] == 'fullcombo':
                    value = "FULL COMBO"
                elif field == 'level_index':
                    level_mapping = {
                        0: "BASIC",
                        1: "ADVANCED",
                        2: "EXPERT",
                        3: "MASTER",
                        4: "ULTRA"
                    }
                    value = level_mapping.get(data[field], str(data[field]))
                # 加载字体

                try:
                    if font_path:
                        font = ImageFont.truetype(font_path, font_size)
                        print(font_size)
                    else:
                        font = ImageFont.load_default()
                        print('未找到字体！请检查font目录')
                except:
                    font = ImageFont.load_default()
                    print('异常！未找到字体！请检查font目录',font_path)
                    pass
                # 绘制文本
                draw.text((x, y), value, fill=color, font=font)

        return image

    # def process_csv(self, csv_path: str = None, output_prefix: str = "score"):
    #     """处理整个CSV文件"""
    #     df = self.load_data(csv_path)
    #
    #     # 计算需要生成多少张图片
    #     total_pages = (len(df) + self.config.ITEMS_PER_PAGE - 1) // self.config.ITEMS_PER_PAGE
    #
    #     for page in range(total_pages):
    #         # 创建一张新的组合图片
    #         composite_image = Image.new(
    #             'RGB',
    #             (self.config.OUTPUT_IMAGE_SIZE[0],
    #              self.config.OUTPUT_IMAGE_SIZE[1] * self.config.ITEMS_PER_PAGE),
    #             (40, 40, 50)
    #         )
    #
    #         # 获取当前页的数据
    #         start_idx = page * self.config.ITEMS_PER_PAGE
    #         end_idx = min((page + 1) * self.config.ITEMS_PER_PAGE, len(df))
    #         page_data = df.iloc[start_idx:end_idx]
    #
    #         for i, (_, row) in enumerate(page_data.iterrows()):
    #             # 渲染单张成绩卡片
    #             card = self.render_score_card(row.to_dict())
    #
    #             # 将卡片粘贴到组合图片上
    #             y_offset = i * self.config.OUTPUT_IMAGE_SIZE[1]
    #             composite_image.paste(card, (0, y_offset))
    #
    #         # 保存组合图片
    #         output_path = os.path.join(
    #             self.config.OUTPUT_DIR,
    #             f"{output_prefix}_page_{page + 1}.jpg"
    #         )
    #         composite_image.save(output_path, quality=self.config.OUTPUT_QUALITY)
    #         print(f"已生成成绩图片: {output_path} (包含{end_idx - start_idx}条记录)")
    def process_csv(self, csv_path: str = None, output_prefix: str = "score"):
        """处理整个CSV文件"""
        df = self.load_data(csv_path)

        # 计算需要生成多少张图片
        total_pages = (len(df) + self.config.ITEMS_PER_PAGE - 1) // self.config.ITEMS_PER_PAGE

        # for page in range(total_pages):
        #     # 创建一张新的组合图片 (50条数据，每行5个，共10行)
        #     composite_image = Image.new(
        #         'RGB',
        #         (self.config.OUTPUT_IMAGE_SIZE[0] * 5,  # 5列
        #          self.config.OUTPUT_IMAGE_SIZE[1] * 10),  # 10行
        #         (40, 40, 50)
        #     )
        #
        #     # 获取当前页的数据
        #     start_idx = page * self.config.ITEMS_PER_PAGE
        #     end_idx = min((page + 1) * self.config.ITEMS_PER_PAGE, len(df))
        #     page_data = df.iloc[start_idx:end_idx]
        #
        #     for i, (_, row) in enumerate(page_data.iterrows()):
        #         # 渲染单张成绩卡片
        #         card = self.render_score_card(row.to_dict())
        #
        #         # 计算卡片的行列位置
        #         row_num = i // 5  # 每行5个
        #         col_num = i % 5  # 当前列
        #
        #         # 计算卡片的偏移量
        #         x_offset = col_num * self.config.OUTPUT_IMAGE_SIZE[0]
        #         y_offset = row_num * self.config.OUTPUT_IMAGE_SIZE[1]
        #
        #         # 将卡片粘贴到组合图片上
        #         composite_image.paste(card, (x_offset, y_offset))
        #
        #     # 保存组合图片
        #     output_path = os.path.join(
        #         self.config.OUTPUT_DIR,
        #         f"{output_prefix}_page_{page + 1}.jpg"
        #     )
        #     composite_image.save(output_path, quality=self.config.OUTPUT_QUALITY)
        #     print(f"已生成成绩图片: {output_path} (包含{end_idx - start_idx}条记录)")


        for page in range(total_pages):
            # 加载背景板
            try:
                plate_path = os.path.join(self.config.TEMPLATE_DIR, 'plate.png')
                composite_image = Image.open(plate_path).convert('RGB')

                # 如果背景板尺寸不够大，则调整大小
                required_width = self.config.OUTPUT_IMAGE_SIZE[0] * 5
                required_height = self.config.OUTPUT_IMAGE_SIZE[1] * 7
                if composite_image.size != (required_width, required_height):
                    composite_image = composite_image.resize((required_width, required_height))
            except Exception as e:
                print(f"无法加载背景板，使用默认背景: {e}")
                composite_image = Image.new(
                    'RGB',
                    (required_width, required_height),
                    (40, 40, 50)
                )

            # 获取当前页的数据
            start_idx = page * self.config.ITEMS_PER_PAGE
            end_idx = min((page + 1) * self.config.ITEMS_PER_PAGE, len(df))
            page_data = df.iloc[start_idx:end_idx]

            for i, (_, row) in enumerate(page_data.iterrows()):
                # 渲染单张成绩卡片
                card = self.render_score_card(row.to_dict())

                # 计算粘贴位置 (5列10行布局)
                col = i % 5
                row = i // 5
                x_offset = col * self.config.OUTPUT_IMAGE_SIZE[0]
                y_offset = row * self.config.OUTPUT_IMAGE_SIZE[1]

                # 将卡片粘贴到组合图片上（使用alpha通道混合）
                if card.mode == 'RGBA':
                    # 如果卡片有透明通道，使用alpha混合
                    composite_image.paste(card, (x_offset, y_offset), card)
                else:
                    composite_image.paste(card, (x_offset, y_offset))

            # 保存组合图片
            output_path = os.path.join(
                self.config.OUTPUT_DIR,
                f"{output_prefix}_page_{page + 1}.jpg"
            )
            composite_image.save(output_path, quality=self.config.OUTPUT_QUALITY)
            print(f"已生成成绩图片: {output_path} (包含{end_idx - start_idx}条记录)")

if __name__ == "__main__":
    renderer = MusicGameScoreRenderer()
    renderer.process_csv()