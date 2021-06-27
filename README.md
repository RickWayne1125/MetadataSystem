# 元数据管理系统

## 结构说明

### 表结构 - Table类

| 属性名       | 类型               | 说明     |
| ------------ | ------------------ | -------- |
| table_name   | string             | 表名     |
| field_num    | int                | 字段个数 |
| fields       | List\<field\>      | 字段列表 |
| path         | string             | 存储位置 |
| foreign_keys | List\<ForeignKey\> | 外键列表 |

### 字段结构 - Field类

| 属性名     | 类型                | 说明                                       |
| ---------- | ------------------- | ------------------------------------------ |
| field_name | string              | 字段名                                     |
| type       | string              | 表示其类型                                 |
| length     | int                 | 字段长度                                   |
| tag        | map\<string, bool\> | 字段特殊标签（如not null, primary key...） |

*e.g. tag = {'not null': True, 'primary key': True, 'auto_increment': False, ...}*

tag可以初始化为一个固定key的map

### 外键结构 - ForeignKey类

| 属性名       | 类型  | 说明     |
| ------------ | ----- | -------- |
| origin_field | Field | 源字段   |
| target_field | Field | 目标字段 |
| origin_table | Table | 源表     |
| target_table | Table | 目标表   |

*注：目标字段为要绑定作为外键的字段*

### 用户结构 - User类

TO DO

## 功能说明

