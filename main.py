import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from config import Config


class MusicGameScoreRenderer:
    def __init__(self):
        self.config = Config()
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保所需目录存在"""
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.config.TEMPLATE_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.config.CSV_PATH), exist_ok=True)

    def load_data(self, csv_path: str = None) -> pd.DataFrame:
        """加载CSV数据"""
        path = csv_path or self.config.CSV_PATH
        try:
            # 读取CSV，跳过标题行后的第一行(因为START_ROW=2表示从第2行开始)
            df = pd.read_csv(path, skiprows=1, nrows=self.config.END_ROW - 1)

            # 重新设置列名(因为skiprows=1会丢失原列名)
            df.columns = [
                'id', 'song_name', 'level', 'level_index', 'score', 'rating',
                'over_power', 'clear', 'full_combo', 'full_chain', 'rank',
                'upload_time', 'play_time'
            ]

            return df
        except Exception as e:
            raise Exception(f"无法加载CSV文件: {e}")

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
                # 如果没有模板，创建一个深色背景图片
                image = Image.new('RGB', self.config.OUTPUT_IMAGE_SIZE, color=(30, 30, 40))
        except Exception as e:
            raise Exception(f"无法加载模板图片: {e}")

        draw = ImageDraw.Draw(image)

        # 绘制每个配置的字段
        for field, config in self.config.DRAW_CONFIG.items():
            if field in data and not pd.isna(data[field]):
                x, y, font_size, color, font_path = config
                value = str(data[field])

                # 特殊字段处理
                if field == 'level':
                    value = f"Lv.{data['level']}+{data.get('level_index', 0)}"
                elif field == 'clear' and data[field] == 'clear':
                    value = "CLEAR"
                elif field == 'full_combo' and data[field] == 'fullcombo':
                    value = "FULL COMBO"

                # 加载字体
                try:
                    if font_path:
                        font = ImageFont.truetype(font_path, font_size)
                    else:
                        font = ImageFont.load_default()
                except:
                    font = ImageFont.load_default()

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

        for page in range(total_pages):
            # 创建一张新的组合图片 (50条数据，每行5个，共10行)
            composite_image = Image.new(
                'RGB',
                (self.config.OUTPUT_IMAGE_SIZE[0] * 5,  # 5列
                 self.config.OUTPUT_IMAGE_SIZE[1] * 10),  # 10行
                (40, 40, 50)
            )

            # 获取当前页的数据
            start_idx = page * self.config.ITEMS_PER_PAGE
            end_idx = min((page + 1) * self.config.ITEMS_PER_PAGE, len(df))
            page_data = df.iloc[start_idx:end_idx]

            for i, (_, row) in enumerate(page_data.iterrows()):
                # 渲染单张成绩卡片
                card = self.render_score_card(row.to_dict())

                # 计算卡片的行列位置
                row_num = i // 5  # 每行5个
                col_num = i % 5  # 当前列

                # 计算卡片的偏移量
                x_offset = col_num * self.config.OUTPUT_IMAGE_SIZE[0]
                y_offset = row_num * self.config.OUTPUT_IMAGE_SIZE[1]

                # 将卡片粘贴到组合图片上
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