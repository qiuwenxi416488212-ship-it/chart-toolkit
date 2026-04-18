# Chart Toolkit
## 数据可视化工具箱 | 快速生成统计图表

<p align="center">
  <img src="https://img.shields.io/pypi/v/chart-toolkit" alt="PyPI">
  <img src="https://img.shields.io/github/stars/XiLi/chart-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/chart-toolkit" alt="License">
</p>

---

## 项目简介

Chart Toolkit (图表工具箱) 是简洁强大的数据可视化工具，帮助你快速生成各类统计图表。无论你需要制作数据分析报告、业务Dashboard还是趋势分析，这个工具都能满足你的需求。

> **让图表制作变得更简单!**

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 📈 折线图 | 趋势变化分析 |
| 📊 柱状图 | 类别对比 |
| 🥧 饼图 | 占比分布 |
| ⚪ 散点图 | 相关性分析 |
| 🎨 样式定制 | 颜色/标签/图例 |
| 💾 多格式导出 | PNG/SVG/HTML |
| 📊 交互图表 | Plotly支持(可选) |

---

## 快速开始

### 安装

```bash
pip install matplotlib pandas
# 交互式图表: pip install plotly
```

### 快速生成图表

```python
from chart_generator import ChartGenerator

# 准备数据
data = {
    '月份': ['1月','2月','3月','4月'],
    '销售额': [10000,15000,12000,18000],
    '利润': [2000,3500,2800,4200]
}

# 生成图表
chart = ChartGenerator()
chart.line_chart(data, '月份', ['销售额','利润'], title='月度业绩')
chart.save('chart.png')
```

---

## 详细功能

### 折线图

```python
data = {
    'date': ['2026-01','2026-02','2026-03','2026-04'],
    'sales': [1000,1500,1300,1800]
}

chart = ChartGenerator()
chart.line_chart(data, 'date', 'sales', title='销售趋势')
chart.save('line.png')
```

### 柱状图

```python
data = {
    'product': ['A','B','C','D'],
    'sales': [1500,2300,1800,2100]
}

chart.bar_chart(data, 'product', 'sales', title='产品销售')
chart.save('bar.png')
```

### 饼图

```python
data = {
    'category': ['手机','电脑','平板','配件'],
    'revenue': [35,30,20,15]
}

chart.pie_chart(data, 'category', 'revenue', title='收入占比')
chart.save('pie.png')
```

### 散点图

```python
data = {
    'advertising': [100,200,300,400,500],
    'sales': [1200,1800,2400,2900,3800]
}

chart.scatter_chart(data, 'advertising', 'sales', title='广告vs销售')
chart.save('scatter.png')
```

### 快速生成

```python
from chart_generator import quick_chart

chart = quick_chart(data, 'line', '月份', '销售额')
chart.save('quick.png')
```

### Plotly交互图表

```python
import pandas as pd
from chart_generator import PlotlyChart

df = pd.DataFrame(data)

# 交互式折线图
fig = PlotlyChart.line(df, 'date', 'sales', title='交互式图表')
html = PlotlyChart.to_html(fig)

# 保存
PlotlyChart.save(fig, 'interactive.html')
```

---

## API参考

| 方法 | 功能 |
|------|------|
| line_chart() | 折线图 |
| bar_chart() | 柱状图 |
| pie_chart() | 饼图 |
| scatter_chart() | 散点图 |
| save() | 保存图表 |
| to_base64() | 转为Base64 |

---

## 依赖

- matplotlib
- pandas
- plotly (可选)

---

## 许可证

MIT License