"""
项目包初始化文件
================

批量期权询价工具包。

主要模块：
- config: 配置管理
- api_client: API 客户端
- data_processor: 数据处理
- main: 主程序入口
"""

__version__ = "1.0.0"
__author__ = "Jerry-Jiayi-He"

from config import (
    CREATE_URL,
    DEADLINE,
    HEADERS,
    INPUT_FILE,
    OUTPUT_FILE,
    RESULT_URL,
    STRUCTURES,
    TARGET_VENDORS,
)
from api_client import fetch_result, submit_inquiry
from data_processor import (
    build_dataframe,
    parse_quotes,
    process_all_stocks,
    process_stock,
    read_stock_codes,
)

__all__ = [
    # 配置
    "CREATE_URL",
    "DEADLINE",
    "HEADERS",
    "INPUT_FILE",
    "OUTPUT_FILE",
    "RESULT_URL",
    "STRUCTURES",
    "TARGET_VENDORS",
    # API 客户端
    "fetch_result",
    "submit_inquiry",
    # 数据处理
    "build_dataframe",
    "parse_quotes",
    "process_all_stocks",
    "process_stock",
    "read_stock_codes",
]
