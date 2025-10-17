"""
配置模块
========

本模块包含所有配置常量和参数。
"""

from typing import Dict, List

###############################################################################
# 文件路径配置
###############################################################################

# 输入 Excel 文件的路径。第一列应包含格式为 ``<代码>.<交易所>`` 的股票代码，
# 例如 ``300476.XSHE``。
INPUT_FILE: str = "input.xlsx"

# 将要生成的输出 Excel 文件的路径。
OUTPUT_FILE: str = "output.xlsx"

###############################################################################
# API 配置
###############################################################################

# API 端点。请将这些值替换为从 Fiddler 捕获中获得的实际端点。
# 例如，创建端点可能类似 ``https://option.example.com/app-api/option-ask/create``
# 结果端点可能是 ``https://option.example.com/app-api/option-ask/result``。
CREATE_URL: str = "https://option.example.com/app-api/option-ask/create"  # TODO: 替换此值
RESULT_URL: str = "https://option.example.com/app-api/option-ask/result"  # TODO: 替换此值

# API 所需的 HTTP 头。至少应包含 ``Content-Type`` 设置为 ``application/json;charset=UTF-8``。
# 很可能您还需要提供从 Fiddler 捕获的 ``Authorization`` 头或会话 ``Cookie``，
# 以便对后端进行身份验证。请填入在捕获中观察到的适当值。
HEADERS: Dict[str, str] = {
    "Content-Type": "application/json;charset=UTF-8",
    # "Authorization": "Bearer <your-token>",  # 如果需要身份验证，请取消注释并替换
}

# 询价所属机构 ID。通常可以在抓包数据中看到，例如 ``"organId": 1``。
ORGAN_ID: int = 1

###############################################################################
# 业务配置
###############################################################################

# 询价时需要提交的券商信息。``label`` 应与结果中返回的 ``brokerName`` 保持一致，
# ``value`` 是抓包请求中使用的券商 ID。
BROKERS: List[Dict[str, int]] = [
    {"label": "GF", "value": 35},
    {"label": "ZJ", "value": 17},
    {"label": "ZQSY", "value": 15},
    {"label": "YHDR", "value": 13},
    {"label": "GJFXZ", "value": 12},
    {"label": "YAZB", "value": 11},
    {"label": "HTCC", "value": 10},
    {"label": "ZZZB", "value": 9},
]

# ``TARGET_VENDORS`` 仍用于结果解析和 DataFrame 构建，仅包含券商简称。
TARGET_VENDORS: List[str] = [broker["label"] for broker in BROKERS]

# 要查询的结构。键是后端理解的结构代码（例如 ``90c`` 表示"实值90"，``100c`` 表示"平值100"，
# ``105c`` 表示"虚值105"），值是要在 Excel 输出中显示的人类可读标签。
# 您可以根据需要在此处添加或删除项目。所有结构将使用 ``DEADLINE`` 指定的相同期限。
STRUCTURES: Dict[str, str] = {
    "90c": "实值90",
    "100c": "平值100",
    "105c": "虚值105",
}

# 所有询价的期限（截止日期）。``1m`` 表示"1个月"。
DEADLINE: str = "1m"
DEADLINE_LABEL: str = "1个月"

# 商品类型：0 代表香草期权 (vanilla)。如果抓包显示不同，请调整。
PRODUCT_TYPE: int = 0

# 询价规模：100万。可根据需要调整。
INQUIRY_SCALE: int = 1_000_000
SCALE_NAME: str = "100万"

###############################################################################
# 轮询配置
###############################################################################

# 连续结果轮询之间的延迟（秒）。提交询价后，服务器可能需要短时间来计算报价。
# 如果结果未立即返回，脚本将每隔 ``POLL_INTERVAL`` 秒轮询结果端点，
# 最多轮询 ``MAX_POLL_ATTEMPTS`` 次。
POLL_INTERVAL: float = 0.5
MAX_POLL_ATTEMPTS: int = 10
