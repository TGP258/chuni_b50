import json
import pymysql
from typing import List, Dict


class ChunithmDBImporter:
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        self.connection = pymysql.connect(
            host=self.db_config['host'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database'],
            port=self.db_config['port'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

    def load_json_data(self, file_path: str) -> List[Dict]:
        """加载JSON数据"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def import_songs(self, songs_data: List[Dict]):
        """导入歌曲数据"""
        if not self.connection:
            self.connect()

        with self.connection.cursor() as cursor:
            # 准备插入歌曲数据
            songs_sql = """
            INSERT INTO songs (id, title, artist, genre, bpm, origin_from)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                title = VALUES(title),
                artist = VALUES(artist),
                genre = VALUES(genre),
                bpm = VALUES(bpm),
                origin_from = VALUES(origin_from)
            """

            # 准备插入难度数据
            difficulties_sql = """
            INSERT INTO difficulties 
                (song_id, difficulty_type, level_value, level_display, chart_id, combo, charter)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                level_value = VALUES(level_value),
                level_display = VALUES(level_display),
                combo = VALUES(combo),
                charter = VALUES(charter)
            """

            # 准备数据
            songs_values = []
            difficulties_values = []

            for song in songs_data:
                basic_info = song['basic_info']
                songs_values.append((
                    song['id'],
                    basic_info['title'],
                    basic_info['artist'],
                    basic_info['genre'],
                    basic_info['bpm'],
                    basic_info['from']
                ))

                # 难度类型映射
                difficulty_types = ['BASIC', 'ADVANCED', 'EXPERT', 'MASTER', 'ULTRA']

                for i, (ds, level, cid, chart) in enumerate(zip(
                        song['ds'],
                        song['level'],
                        song['cids'],
                        song['charts']
                )):
                    # 处理可能不存在的难度类型
                    diff_type = difficulty_types[i] if i < len(difficulty_types) else 'WORLD\'S END'

                    difficulties_values.append((
                        song['id'],
                        diff_type,
                        ds,
                        level,
                        cid,
                        chart['combo'],
                        chart['charter']
                    ))

            # 执行批量插入
            try:
                cursor.executemany(songs_sql, songs_values)
                cursor.executemany(difficulties_sql, difficulties_values)
                self.connection.commit()
                print(f"成功导入 {len(songs_values)} 首歌曲和 {len(difficulties_values)} 个难度数据")
            except Exception as e:
                self.connection.rollback()
                print(f"导入失败: {e}")
                raise


if __name__ == "__main__":
    # 数据库配置
    db_config = {
        'host': 'localhost',#访问服务器主机
        'port': 3308, #默认为3306#
        'user': 'your_name',#数据库用户名
        'password': 'your_passward',#数据库密码
        'database': 'chunithm_db',#数据库名
        'auth_plugin' : 'mysql_native_password',#旧版本验证，不需要可删
        'init_command' : 'SET time_zone = "+8:00"'#时区设置，不需要可删
    }

    # JSON文件路径
    json_file = 'music_data.json'

    # 创建导入器实例
    importer = ChunithmDBImporter(db_config)

    try:
        # 加载数据
        songs_data = importer.load_json_data(json_file)

        # 导入数据
        importer.import_songs(songs_data)

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        importer.disconnect()