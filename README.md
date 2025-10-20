# 批量期权询价工具# 批量期权询价工具



一个自动化批量查询股票期权报价的 Python 工具。通过调用微信小程序后端 API，实现多期限、多券商的期权报价自动采集。一个用于批量查询股票期权报价的自动化工具。通过调用微信小程序后端 API，自动获取多只股票的期权报价信息。



---## 项目结构



## ✨ 核心特性```

option_ask_price/

- 🔄 **多期限支持**：一次运行可查询 1个月、2个月、3个月等多个期限├── main.py              # 主入口文件

- 📊 **多券商对比**：自动获取 8 家券商报价（GF、ZJ、ZQSY、YHDR、GJFXZ、YAZB、HTCC、ZZZB）├── config.py            # 配置模块（API 端点、业务参数等）

- 🎯 **多种期权结构**：实值90、实值95、平值100、虚值103、虚值105├── api_client.py        # API 客户端模块（负责与后端 API 交互）

- 💾 **批量保存**：每处理 500 只股票自动保存中间结果，防止数据丢失├── data_processor.py    # 数据处理模块（解析报价、构建 DataFrame）

- 📁 **智能分类**：按期限自动创建目录，结果文件清晰有序├── requirements.txt     # Python 依赖包列表

- 🔍 **进度跟踪**：实时显示处理进度，了解任务执行状态├── input.xlsx           # 输入文件（股票代码列表）

└── output.xlsx          # 输出文件（报价结果）

---```



## 📂 项目结构## 功能特性



```- ✅ 批量处理多只股票的期权询价

option_ask_price/- ✅ 支持多种期权结构（实值90、平值100、虚值105）

├── main.py              # 主程序：多期限循环处理入口- ✅ 从多个券商获取报价（GF、ZJ、ZQSY、YHDR、GJFXZ、YAZB、HTCC、ZZZB）

├── config.py            # 配置文件：API、券商、期限等参数- ✅ 自动轮询结果直到获取完整数据

├── api_client.py        # API 客户端：提交询价和获取结果- ✅ 输出格式化的 Excel 报表（包含 MultiIndex 列）

├── data_processor.py    # 数据处理：解析报价、构建 Excel

├── requirements.txt     # 依赖包列表## 安装依赖

├── input.xlsx           # 输入：股票代码列表（第一列）

└── output/              # 输出目录```bash

    ├── output_1m/       # 1个月期限结果pip install -r requirements.txt

    │   ├── intermediate/        # 中间批次文件```

    │   └── final_result_1m.xlsx # 最终完整结果

    ├── output_2m/       # 2个月期限结果## 配置说明

    └── output_3m/       # 3个月期限结果

```### 1. 配置 API 端点和认证信息



---编辑 `config.py` 文件，替换以下占位符：



## 🚀 快速开始```python

# API 端点

### 1. 安装依赖CREATE_URL = "https://your-actual-server.com/app-api/option-ask/create"

RESULT_URL = "https://your-actual-server.com/app-api/option-ask/result"

```bash

pip install pandas requests openpyxl# HTTP 头（包含认证信息）

```HEADERS = {

    "Content-Type": "application/json;charset=UTF-8",

### 2. 配置 API（重要！）    "Authorization": "Bearer <your-actual-token>",  # 如果需要

    "Cookie": "<your-actual-cookie>",              # 如果需要

编辑 `config.py`，填入你的 API 信息：}

```

```python

# 从 Fiddler 抓包获取**如何获取这些信息？**

HEADERS = {

    "Content-Type": "application/json;charset=UTF-8",1. 使用 Fiddler 或浏览器开发者工具抓包

    "Authorization": "Bearer 你的token",  # 必须填写！2. 在微信小程序中执行一次询价操作

}3. 找到对应的 HTTP 请求

```4. 复制 URL 和 Headers 信息



### 3. 配置期限### 2. 准备输入文件



在 `main.py` 中设置要查询的期限：创建 `input.xlsx` 文件，第一列填写股票代码（包含交易所后缀）：



```python| A列 |

DEADLINES_TO_QUERY = [|-----|

    ("1m", "1个月"),| 300476.XSHE |

    ("2m", "2个月"),| 000001.XSHE |

    ("3m", "3个月"),| 600000.XSHG |

]

```### 3. 调整业务参数（可选）



### 4. 准备输入文件在 `config.py` 中可以自定义：



创建 `input.xlsx`，第一列填入股票代码：- `CREATE_URL` / `RESULT_URL`: 实际 API 端点

- `HEADERS`: 认证信息（Token、Cookie 等）

```- `ORGAN_ID`: 询价所属机构 ID

300476.XSHE- `BROKERS`: 需要报价的券商及其 ID

000001.XSHE- `STRUCTURES`: 期权结构类型及展示名称

600000.XSHG- `DEADLINE` / `DEADLINE_LABEL`: 期限代码与展示名称

...- `INQUIRY_SCALE` / `SCALE_NAME`: 询价规模及展示名称

```- `POLL_INTERVAL` 和 `MAX_POLL_ATTEMPTS`: 轮询参数



### 5. 运行程序## 使用方法



```bash```bash

python main.pypython main.py

``````



---程序将：

1. 读取 `input.xlsx` 中的股票代码

## ⚙️ 配置说明2. 对每只股票执行询价

3. 等待并获取报价结果

### 修改期限（config.py）4. 将结果汇总到 `output.xlsx`



如果只需要单独修改默认期限：### 示例输出



```python```

DEADLINE: str = "1m"        # 期限代码============================================================

DEADLINE_LABEL: str = "1个月"  # 期限标签批量期权询价工具

```============================================================



### 修改券商列表（config.py）[1/3] 正在读取输入文件: input.xlsx

      成功读取 3 只股票代码

```python

BROKERS = [[2/3] 正在执行批量询价...

    {"label": "GF", "value": 35},      这可能需要一些时间，请耐心等待...

    {"label": "ZJ", "value": 17},

    # ... 添加或删除券商[3/3] 正在写入输出文件: output.xlsx

]      成功！已将结果写入 'output.xlsx'

```

============================================================

### 修改期权结构（config.py）处理完成！

============================================================

```python```

STRUCTURES = {

    "90c": "实值90",## 输出文件格式

    "100c": "平值100",

    "105c": "虚值105",输出的 Excel 文件包含 MultiIndex 列：

    # ... 添加或删除结构- 第一级：结构类型 + 期限（例如 "实值90 1个月"）

}- 第二级：券商名称（GF、ZJ、ZQSY、YHDR、GJFXZ、YAZB、HTCC、ZZZB）

```- 行索引：股票代码

- 单元格值：报价百分比（例如 13.33 表示 13.33%）

### 修改批量保存参数（data_processor.py）

## 模块说明

```python

# 默认每 500 只股票保存一次### config.py

process_all_stocks(stock_codes, batch_size=500)包含所有配置常量：

```- 文件路径配置

- API 配置（端点、认证）

---- 业务配置（券商、结构、期限）

- 轮询配置

## 📊 输出说明

### api_client.py

### 文件结构负责与 API 交互：

- `submit_inquiry()`: 提交期权询价请求

```- `fetch_result()`: 轮询并获取询价结果

output/

├── output_1m/### data_processor.py

│   ├── intermediate/处理数据流程：

│   │   ├── batch_1_20251020_130000.xlsx  # 前 500 只- `read_stock_codes()`: 从 Excel 读取股票代码

│   │   ├── batch_2_20251020_140000.xlsx  # 前 1000 只- `process_stock()`: 处理单只股票的完整流程

│   │   └── ...- `parse_quotes()`: 解析 API 返回的报价数据

│   └── final_result_1m.xlsx              # 最终完整结果- `build_dataframe()`: 构建输出 DataFrame

└── output_2m/- `process_all_stocks()`: 批量处理所有股票

    └── ...

```### main.py

程序入口，协调各模块完成整体流程。

### Excel 格式

## 注意事项

| 股票代码 | 实值90 1个月<br>GF | 实值90 1个月<br>ZJ | ... | 平值100 1个月<br>GF | ...

|---------|-------------------|-------------------|-----|-------------------|-----|⚠️ **重要提示**：

| 300476.XSHE | 0.0234 | 0.0256 | ... | 0.0189 | ... |

| 000001.XSHE | 0.0312 | 0.0298 | ... | 0.0267 | ... |1. 确保在 `config.py` 中填写正确的 API 端点和认证信息

2. 认证令牌可能会过期，需要定期更新

**注意**：数值为小数形式（如 0.0234 表示 2.34%）3. 输入文件第一列必须包含完整的股票代码（含交易所后缀）

4. 如果轮询超时，可以增加 `MAX_POLL_ATTEMPTS` 或 `POLL_INTERVAL`

---5. 大批量处理时注意 API 调用频率限制



## ⚡ 性能说明## 故障排查



- **处理速度**：每只股票约 2-3 秒（含 API 请求和轮询）**问题：提交询价失败**

- **5000 只股票**：预计 3-4 小时- 检查 API 端点是否正确

- **批量保存**：每 500 只自动保存，确保数据安全- 检查认证信息是否有效（Token/Cookie 是否过期）

- **建议**：大批量处理建议夜间运行- 查看错误消息中返回的具体错误码



---**问题：未在规定时间内获取到结果**

- 增加 `MAX_POLL_ATTEMPTS`

## 🔧 常见问题- 增加 `POLL_INTERVAL`

- 检查网络连接

### Q1: 运行时提示认证失败？

**A**: 检查 `config.py` 中的 `Authorization` token 是否正确，可能已过期，需重新抓包获取。**问题：输入文件读取失败**

- 确保 `input.xlsx` 存在于当前目录

### Q2: 中间文件保存在哪里？- 检查文件格式是否正确

**A**: 在 `output/output_{期限}/intermediate/` 目录下，每个期限独立存放。- 确保第一列包含股票代码



### Q3: 如何只查询单个期限？## 许可证

**A**: 在 `main.py` 中设置：

```python本项目仅供学习和研究使用。

DEADLINES_TO_QUERY = [("1m", "1个月")]

```## 作者



### Q4: 处理中断了怎么办？Jerry-Jiayi-He

**A**: 中间文件已保存，可以手动整理，或从中断处重新开始（需修改 `input.xlsx`）。

## 更新日志

### Q5: 如何修改批量保存的数量？

**A**: 在 `main.py` 的 `process_single_deadline` 函数中修改：### v1.0.0 (2025-10-18)

```python- 初始版本发布

df_result = process_all_stocks(stock_codes, batch_size=1000)  # 改为 1000- 支持批量期权询价

```- 模块化代码结构


---

## 📝 使用示例

### 场景 1：查询单个期限（1个月）

```python
# main.py
DEADLINES_TO_QUERY = [("1m", "1个月")]
```

### 场景 2：查询多个期限（1、2、3 个月）

```python
# main.py
DEADLINES_TO_QUERY = [
    ("1m", "1个月"),
    ("2m", "2个月"),
    ("3m", "3个月"),
]
```

### 场景 3：测试小批量（10 只股票）

在 `input.xlsx` 中只放 10 只股票代码，然后运行：

```bash
python main.py
```

---

## 📦 依赖说明

- **pandas** (≥2.0.0)：数据处理和 Excel 操作
- **requests** (≥2.28.0)：HTTP API 请求
- **openpyxl** (≥3.0.0)：Excel 文件读写

---

## 👤 作者

**Jerry-Jiayi-He**

---

## 📄 许可证

本项目仅供学习和研究使用。
