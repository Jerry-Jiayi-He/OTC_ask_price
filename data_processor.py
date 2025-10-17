"""
数据处理模块
============

本模块负责处理股票数据、解析报价结果并构建输出 DataFrame。
"""

from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

from api_client import fetch_result, submit_inquiry
from config import DEADLINE, DEADLINE_LABEL, STRUCTURES, TARGET_VENDORS


def parse_quotes(items: List[dict], structures: Iterable[str]) -> Dict[str, Dict[str, Optional[float]]]:
    """从结果项目中提取选定结构和券商的报价。

    参数
    ----------
    items : List[dict]
        结果端点返回的字典列表。
    structures : Iterable[str]
        要筛选的结构代码列表。

    返回值
    -------
    Dict[str, Dict[str, Optional[float]]]
        嵌套字典，将结构代码映射到券商名称再映射到数值报价值
        （例如 0.1333 表示 13.33%），如果未提供报价则为 ``None``。

    注意事项
    -----
    后端返回的结果项目通常具有以下键：``structure``（结构代码）、
    ``brokerName``（例如 "GF"）和 ``offer``（表示报价的字符串，例如 "0.067" 表示 6.7%）。
    此函数忽略不在所需列表中的结构或券商。
    """
    result: Dict[str, Dict[str, Optional[float]]] = {
        struct: {vendor: None for vendor in TARGET_VENDORS} for struct in structures
    }
    for item in items:
        struct = item.get("structure")
        broker = item.get("brokerName")
        offer = item.get("offer")
        if struct in structures and broker in TARGET_VENDORS:
            if offer and offer != "0":
                try:
                    result[struct][broker] = float(offer)
                except ValueError:
                    result[struct][broker] = None
    return result


def process_stock(stock_code: str) -> Dict[str, Dict[str, Optional[float]]]:
    """处理单个股票代码，从提交到结果解析。

    参数
    ----------
    stock_code : str
        数字股票代码字符串（不含交易所后缀）。

    返回值
    -------
    Dict[str, Dict[str, Optional[float]]]
        按结构和券商键入的报价字典。如果发生错误，返回空字典。
    """
    inquiry_id = submit_inquiry(stock_code, STRUCTURES.keys())
    if inquiry_id is None:
        return {}
    items = fetch_result(inquiry_id)
    if not items:
        return {}
    return parse_quotes(items, STRUCTURES.keys())


def build_dataframe(records: List[Dict[str, Dict[str, Optional[float]]]],
                    codes: List[str]) -> pd.DataFrame:
    """从多个股票报价字典组装 DataFrame。

    参数
    ----------
    records : List[Dict[str, Dict[str, Optional[float]]]]
        报价字典列表，每只股票一个。
    codes : List[str]
        原始股票代码列表（包括交易所后缀），与 ``records`` 的顺序匹配。
        这些将成为结果 DataFrame 的索引。

    返回值
    -------
    pandas.DataFrame
        具有 MultiIndex 列的 DataFrame：第一级是 ``<结构标签> <期限>``
        （例如 ``实值90 1m``），第二级是券商名称。索引是完整的股票代码
        （例如 ``300476.XSHE``）。值是浮点数（或 ``None``）。
    """
    # 构建列元组列表：(结构标签 + ' ' + 期限, 券商)
    column_tuples: List[tuple] = []
    deadline_display = DEADLINE_LABEL or DEADLINE
    for struct_code, struct_label in STRUCTURES.items():
        # 将期限后缀添加到结构名称以匹配示例（例如 "实值90 1个月"）
        header = f"{struct_label} {deadline_display}"
        for vendor in TARGET_VENDORS:
            column_tuples.append((header, vendor))
    
    # 准备数据行
    rows: List[List[Optional[float]]] = []
    for quote_dict in records:
        row: List[Optional[float]] = []
        for struct_code in STRUCTURES.keys():
            # 如果未检索到此结构（例如错误），则填充 None
            broker_dict = quote_dict.get(struct_code, {vendor: None for vendor in TARGET_VENDORS})
            for vendor in TARGET_VENDORS:
                row.append(broker_dict.get(vendor))
        rows.append(row)
    
    # 创建 MultiIndex 列
    columns = pd.MultiIndex.from_tuples(column_tuples, names=["Structure", "Broker"])
    df = pd.DataFrame(rows, index=codes, columns=columns)
    return df


def read_stock_codes(input_file: str) -> List[str]:
    """从输入 Excel 文件中读取股票代码。

    参数
    ----------
    input_file : str
        输入文件的路径。

    返回值
    -------
    List[str]
        股票代码列表（包括交易所后缀）。

    异常
    ------
    FileNotFoundError
        如果输入文件不存在。
    ValueError
        如果文件第一列不包含股票代码。
    """
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"未找到输入文件 '{input_file}'。请创建包含股票代码列表的文件。")
    
    df_input = pd.read_excel(input_path, header=None)
    stock_codes_full = df_input.iloc[:, 0].dropna().astype(str).tolist()
    
    if not stock_codes_full:
        raise ValueError("输入文件的第一列不包含股票代码。")
    
    return stock_codes_full


def process_all_stocks(stock_codes_full: List[str]) -> pd.DataFrame:
    """批量处理所有股票并返回结果 DataFrame。

    参数
    ----------
    stock_codes_full : List[str]
        完整的股票代码列表（包括交易所后缀）。

    返回值
    -------
    pandas.DataFrame
        包含所有股票报价的 DataFrame，值已转换为百分比。
    """
    # 提取股票代码的数字部分（点之前的部分）
    stock_codes_numeric = [code.split(".")[0] for code in stock_codes_full]
    
    # 对每只股票执行询价
    quote_records: List[Dict[str, Dict[str, Optional[float]]]] = []
    for numeric_code in stock_codes_numeric:
        quotes = process_stock(numeric_code)
        quote_records.append(quotes)
    
    # 构建 DataFrame
    df_quotes = build_dataframe(quote_records, stock_codes_full)
    
    # 乘以 100 将小数转换为百分比（如果需要）
    df_percentage = df_quotes.applymap(lambda x: round(x * 100, 2) if isinstance(x, float) else x)
    
    return df_percentage
