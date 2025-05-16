## 前言

目前仅支持落雪查分器导出的CSV文件（正在加入查歌功能，歌曲数据来自水鱼Dving-Fish）
还没有做其他字体的支持，若要使用其他字体请先改名为NotoSansCJK-Regular.ttc

## 使用须知

本项目可以直接从水鱼API [diving-fish.com/api/chunithmprober/music_data](https://www.diving-fish.com/api/chunithmprober/music_data)拉取乐曲数据到数据库。

手动执行getAPI.py拉取API所给字典并转换为 json。

手动执行importDatabase.py将json导入到数据库中。

Tips：使用前请修改importDatabase.py中数据库连接配置，并参照根目录下create_database.sql文件创建数据库。

## 关于数据库

### 数据库设计

该项目使用MySQL作为数据库，建表语句详见根目录sql文件

表：songs

| 字段名      | 类型         | 说明         |
| ----------- | ------------ | ------------ |
| id          | int          | 乐曲ID       |
| title       | varchar(255) | 乐曲名       |
| artist      | varchar(255) | 作者         |
| genre       | varchar(100) | 分类         |
| bpm         | int          | 乐曲BPM值    |
| origin_from | varchar(100) | 收录版本     |
| created_at  | timestamp    | 数据创建时间 |
| updated_at  | timestamp    | 数据更新时间 |

表：difficulties

| 字段名          | 类型         | 说明                             |
| --------------- | ------------ | -------------------------------- |
| id              | int          | 主键                             |
| song_id         | int          | 外键 与songs表<br />的id字段关联 |
| difficulty_type | enum         | 难度类型                         |
| level_value     | decimal(4,1) | 难度定数                         |
| level_display   | varchar(10)  | 标识等级                         |
| chart_id        | int          | 谱面ID                           |
| combo           | int          | 该难度的物量                     |
| charter         | varchar(255) | 该难度的谱师名                   |

