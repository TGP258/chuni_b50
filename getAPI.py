import os

import requests
import sys
import io
import json
from typing import List, Dict

import config

# from config import DATA_DIR

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# url = "https://www.diving-fish.com/api/chunithmprober/music_data"
url = 'http://localhost:3000/api'
response = requests.get(url)
data = response.json()
if response.status_code == 200:
    # data = response.json()
    # # print(data)
    # output_file = ""
    # 打开输出文件，并将标准输出重定向到文件
    # with open(output_file, 'w',encoding="utf-8") as f:
    #     sys.stdout = f
    #     print(data)
    # 恢复标准输出
    # sys.stdout = sys.__stdout__
    print("拉取成功")
else:
    print(f"请求失败，状态码: {response.status_code}")


def convert_api_data_to_json(api_data: List[Dict], output_file:data) -> None:
    """
    将 API 返回的 Python 字典数据转换为标准 JSON 文件

    参数:
        api_data: 从 API 获取的 Python 字典列表
        output_file: 输出的 JSON 文件路径
    """
    try:
        # 将数据转换为标准 JSON 格式
        json_data = json.dumps(api_data, ensure_ascii=False, indent=2)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_data)

        print(f"成功将数据保存为 JSON 文件: {output_file}")

    except Exception as e:
        print(f"转换失败: {e}")
        raise


def validate_api_data(api_data: List[Dict]) -> bool:
    """
    验证 API 数据格式是否符合预期

    参数:
        api_data: 从 API 获取的数据

    返回:
        bool: 数据是否有效
    """
    if not isinstance(api_data, list):
        print("错误: API 数据应该是一个列表")
        return False

    required_keys = ['id', 'title', 'ds', 'level', 'cids', 'charts', 'basic_info']

    for item in api_data:
        if not isinstance(item, dict):
            print(f"错误: 列表项应该是字典，实际是 {type(item)}")
            return False

        missing_keys = [key for key in required_keys if key not in item]
        if missing_keys:
            print(f"错误: 缺少必要的键: {missing_keys}")
            return False

    return True

def main():
    api_data =data
    # 输出文件路径
    # 使用导入的DATA_DIR变量构建完整路径
    output_json = os.path.join(config.Config.DATA_DIR, 'music_data.json')

    # 转换为JSON文件
    convert_api_data_to_json(api_data, output_json)
    # output_json='music_data.json'
    # # 转换为 JSON 文件
    # convert_api_data_to_json(api_data, output_json)
if __name__ == "__main__":
    main()