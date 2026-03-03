# 选题筛选模块

## 功能
对发现的选题进行综合评分排序

## 评分维度
- 热度 (40%): (点赞+收藏+评论) / 最大值
- 差异化 (30%): 与已有选题的相似度(越低越高分)
- 时效性 (30%): 发布时间越近分数越高

## 参数
- topics: 选题列表
- existing_topics: 已有选题(用于差异化计算)

## 输出格式
```json
[
  {
    "original_data": {...},
    "scores": {
      "hotness": 0.8,
      "differentiation": 0.6,
      "timeliness": 0.9
    },
    "total_score": 0.77
  }
]
```
