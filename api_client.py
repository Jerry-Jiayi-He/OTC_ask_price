"""
API 客户端模块
==============

本模块负责与期权询价 API 进行交互，包括提交询价请求和获取结果。
"""

import json
import time
from typing import Iterable, List, Optional

import requests

from config import (
    CREATE_URL,
    DEADLINE,
    HEADERS,
    MAX_POLL_ATTEMPTS,
    POLL_INTERVAL,
    PRODUCT_TYPE,
    INQUIRY_SCALE,
    RESULT_URL,
    TARGET_VENDORS,
)


def submit_inquiry(stock_code: str, structures: Iterable[str]) -> Optional[int]:
    """为单只股票提交期权询价。

    参数
    ----------
    stock_code : str
        股票代码的数字部分（例如 ``"300476"``）。此处不要包含交易所后缀。
    structures : Iterable[str]
        要请求的结构代码列表。每个结构必须对应于配置中的结构键。

    返回值
    -------
    Optional[int]
        后端返回的询价 ID，如果发生错误则返回 ``None``。

    注意事项
    -----
    如果请求失败（例如由于身份验证），此函数会打印错误消息并返回 ``None``。
    在运行脚本之前，您应确保配置文件中的 ``HEADERS`` 包含有效的授权值。
    """
    payload = {
        "stockCode": stock_code,
        "type": PRODUCT_TYPE,
        "scale": INQUIRY_SCALE,
        "deadline": DEADLINE,
        "structures": list(structures),
        "vendors": TARGET_VENDORS,
    }
    try:
        response = requests.post(CREATE_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        # Fiddler 捕获的接口返回格式通常是 {"code":0,"data":<id>,"msg":""}
        if data.get("code") != 0:
            print(f"提交询价失败: {data}")
            return None
        return data.get("data")
    except Exception as e:
        print(f"为 {stock_code} 提交询价时出错: {e}")
        return None


def fetch_result(inquiry_id: int) -> Optional[List[dict]]:
    """轮询结果端点直到返回询价项目。

    参数
    ----------
    inquiry_id : int
        由 :func:`submit_inquiry` 返回的 ID。

    返回值
    -------
    Optional[List[dict]]
        如果可用，返回结果项目（字典）列表。如果在最大轮询尝试次数内未获得结果
        或发生错误，则返回 ``None``。
    """
    for _ in range(MAX_POLL_ATTEMPTS):
        try:
            # 某些 API 使用查询参数，其他使用路径参数。
            # Fiddler 应该显示正确的形式。这里我们使用 ``params`` 将 ID 作为查询参数发送。
            response = requests.get(RESULT_URL, headers=HEADERS, params={"id": inquiry_id})
            response.raise_for_status()
            data = response.json()
            if data.get("code") != 0:
                print(f"查询结果失败: {data}")
                return None
            items = data.get("data", {}).get("items", [])
            if items:
                return items
        except Exception as e:
            print(f"获取 {inquiry_id} 的结果时出错: {e}")
            return None
        time.sleep(POLL_INTERVAL)
    print(f"未在规定时间内获取到结果 (id={inquiry_id})")
    return None
