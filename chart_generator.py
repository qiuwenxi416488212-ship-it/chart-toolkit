#!/usr/bin/env python3
"""
Data Visualization Toolkit
数据可视化: 图表生成/导出
"""

import os
import base64
from io import BytesIO
from typing import List, Dict, Any, Optional, Union

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# 设置中文字体
def setup_chinese_font():
    """设置中文字体"""
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # 尝试查找系统中的中文字体
    font_candidates = [
        'SimHei', 'Microsoft YaHei', 'SimSun', 
        'STHeiti', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC'
    ]
    
    for font in font_candidates:
        font_path = fm.findfont(font)
        if font_path:
            plt.rcParams['font.sans-serif'] = [font]
            break
    
    plt.rcParams['axes.unicode_minus'] = False


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self):
        setup_chinese_font()
        self.fig = None
    
    # ============== 折线图 ==============
    def line_chart(self, data: Union[pd.DataFrame, Dict], 
                   x: str, y: Union[str, List[str]],
                   title: str = '', **kwargs) -> 'ChartGenerator':
        """生成折线图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not installed')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        ys = [y] if isinstance(y, str) else y
        for y_col in ys:
            ax.plot(df[x], df[y_col], marker='o', label=y_col)
        
        ax.set_title(title or kwargs.get('title', ''))
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', ''))
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return self
    
    # ============== 柱状图 ==============
    def bar_chart(self, data: Union[pd.DataFrame, Dict],
                  x: str, y: Union[str, List[str]],
                  title: str = '', **kwargs) -> 'ChartGenerator':
        """生成柱状图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not installed')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        ys = [y] if isinstance(y, str) else y
        x_pos = range(len(df[x]))
        
        width = kwargs.get('width', 0.35)
        for i, y_col in enumerate(ys):
            offset = (i - len(ys)/2 + 0.5) * width
            ax.bar([p + offset for p in x_pos], df[y_col], width, label=y_col)
        
        ax.set_title(title or kwargs.get('title', ''))
        ax.set_xticks(x_pos)
        ax.set_xticklabels(df[x])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        return self
    
    # ============== 饼图 ==============
    def pie_chart(self, data: Union[pd.DataFrame, Dict],
                  names: str, values: str,
                  title: str = '', **kwargs) -> 'ChartGenerator':
        """生成饼图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not available')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (8, 8)))
        
        ax.pie(df[values], labels=df[names], autopct='%1.1f%%', startangle=90)
        ax.set_title(title or kwargs.get('title', ''))
        
        return self
    
    # ============== 散点图 ==============
    def scatter_chart(self, data: Union[pd.DataFrame, Dict],
                      x: str, y: str, size: str = None,
                      color: str = None, title: str = '',
                      **kwargs) -> 'ChartGenerator':
        """生成散点图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not installed')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        s = df[size] if size else 50
        c = df[color] if color else None
        
        ax.scatter(df[x], df[y], s=s, c=c, alpha=0.6)
        ax.set_title(title or kwargs.get('title', ''))
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.grid(True, alpha=0.3)
        
        return self
    
    # ============== 保存 ==============
    def save(self, path: str, dpi: int = 100, **kwargs):
        """保存图表"""
        if self.fig:
            self.fig.savefig(path, dpi=dpi, bbox_inches='tight', **kwargs)
            plt.close(self.fig)
            return path
        return None
    
    def to_base64(self, format: str = 'png', dpi: int = 100) -> str:
        """转为Base64"""
        if not self.fig:
            return None
        
        buffer = BytesIO()
        self.fig.savefig(buffer, format=format, dpi=dpi, bbox_inches='tight')
        buffer.seek(0)
        
        return base64.b64encode(buffer.read()).decode()
    
    def show(self):
        """显示图表"""
        if self.fig:
            plt.show()


# ============== Plotly 图表 ==============
class PlotlyChart:
    """Plotly交互式图表"""
    
    @staticmethod
    def line(df: pd.DataFrame, x: str, y: Union[str, List[str]], 
             title: str = '') -> go.Figure:
        """折线图"""
        fig = px.line(df, x=x, y=y, title=title)
        return fig
    
    @staticmethod
    def bar(df: pd.DataFrame, x: str, y: Union[str, List[str]],
            title: str = '', orientation: str = 'v') -> go.Figure:
        """柱状图"""
        fig = px.bar(df, x=x, y=y, title=title, orientation=orientation)
        return fig
    
    @staticmethod
    def scatter(df: pd.DataFrame, x: str, y: str,
                color: str = None, size: str = None,
                title: str = '') -> go.Figure:
        """散点图"""
        fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title)
        return fig
    
    @staticmethod
    def pie(df: pd.DataFrame, names: str, values: str,
            title: str = '') -> go.Figure:
        """饼图"""
        fig = px.pie(df, names=names, values=values, title=title)
        return fig
    
    @staticmethod
    def to_html(fig: go.Figure) -> str:
        """转为HTML"""
        return fig.to_html()
    
    @staticmethod
    def save(fig: go.Figure, path: str, format: str = 'html'):
        """保存图表"""
        if format == 'html':
            fig.write_html(path)
        elif format == 'png':
            fig.write_image(path)
        return path


# ============== 便捷函数 ==============
def quick_chart(data: Union[pd.DataFrame, Dict], 
                chart_type: str, x: str, y: str = None,
                **kwargs) -> ChartGenerator:
    """快速生成图表"""
    generator = ChartGenerator()
    
    if chart_type == 'line':
        return generator.line_chart(data, x, y, **kwargs)
    elif chart_type == 'bar':
        return generator.bar_chart(data, x, y, **kwargs)
    elif chart_type == 'pie':
        return generator.pie_chart(data, x, y, **kwargs)
    elif chart_type == 'scatter':
        return generator.scatter_chart(data, x, y, **kwargs)
    
    raise ValueError(f'Unknown chart type: {chart_type}')


def chart_to_image(data: Union[pd.DataFrame, Dict],
                   chart_type: str, x: str, y: str = None,
                   output_path: str = 'chart.png', **kwargs):
    """快速生成并保存图表"""
    chart = quick_chart(data, chart_type, x, y, **kwargs)
    return chart.save(output_path)


# ============== 测试 ==============
if __name__ == '__main__':
    print('Data Visualization toolkit loaded')
    print(f'matplotlib: {MATPLOTLIB_AVAILABLE}')
    print(f'plotly: {PLOTLY_AVAILABLE}')
    
    if MATPLOTLIB_AVAILABLE:
        # 测试
        data = {
            'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
            'sales': [100, 150, 130, 180],
            'profit': [20, 35, 25, 40]
        }
        
        chart = ChartGenerator()
        chart.line_chart(data, 'date', ['sales', 'profit'], title='Sales & Profit')
        chart.save('test_chart.png')
        print('Test chart saved to test_chart.png')