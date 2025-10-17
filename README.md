# 批量期权询价工具

一个用于批量查询股票期权报价的自动化工具。通过调用微信小程序后端 API，自动获取多只股票的期权报价信息。

## 项目结构

```
option_ask_price/
├── main.py              # 主入口文件
├── config.py            # 配置模块（API 端点、业务参数等）
├── api_client.py        # API 客户端模块（负责与后端 API 交互）
├── data_processor.py    # 数据处理模块（解析报价、构建 DataFrame）
├── requirements.txt     # Python 依赖包列表
├── input.xlsx           # 输入文件（股票代码列表）
└── output.xlsx          # 输出文件（报价结果）
```

## 功能特性

- ✅ 批量处理多只股票的期权询价
- ✅ 支持多种期权结构（实值90、平值100、虚值105）
- ✅ 从多个券商获取报价（GJFXZ、YHDR、ZQSY、ZJ、GF）
- ✅ 自动轮询结果直到获取完整数据
- ✅ 输出格式化的 Excel 报表（包含 MultiIndex 列）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 1. 配置 API 端点和认证信息

编辑 `config.py` 文件，替换以下占位符：

```python
# API 端点
CREATE_URL = "https://your-actual-server.com/app-api/option-ask/create"
RESULT_URL = "https://your-actual-server.com/app-api/option-ask/result"

# HTTP 头（包含认证信息）
HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Authorization": "Bearer <your-actual-token>",
    "Cookie": "<your-actual-cookie>",
}
```

**如何获取这些信息？**

1. 使用 Fiddler 或浏览器开发者工具抓包
2. 在微信小程序中执行一次询价操作
3. 找到对应的 HTTP 请求
4. 复制 URL 和 Headers 信息

### 2. 准备输入文件

创建 `input.xlsx` 文件，第一列填写股票代码（包含交易所后缀）：

| A列 |
|-----|
| 300476.XSHE |
| 000001.XSHE |
| 600000.XSHG |

### 3. 调整业务参数（可选）

在 `config.py` 中可以自定义：

- `TARGET_VENDORS`: 券商列表
- `STRUCTURES`: 期权结构类型
- `DEADLINE`: 期限（默认 1 个月）
- `INQUIRY_SCALE`: 询价规模（默认 100 万）
- `POLL_INTERVAL` 和 `MAX_POLL_ATTEMPTS`: 轮询参数

## 使用方法

```bash
python main.py
```

程序将：
1. 读取 `input.xlsx` 中的股票代码
2. 对每只股票执行询价
3. 等待并获取报价结果
4. 将结果汇总到 `output.xlsx`

### 示例输出

```
============================================================
批量期权询价工具
============================================================

[1/3] 正在读取输入文件: input.xlsx
      成功读取 3 只股票代码

[2/3] 正在执行批量询价...
      这可能需要一些时间，请耐心等待...

[3/3] 正在写入输出文件: output.xlsx
      成功！已将结果写入 'output.xlsx'

============================================================
处理完成！
============================================================
```

## 输出文件格式

输出的 Excel 文件包含 MultiIndex 列：
- 第一级：结构类型 + 期限（例如 "90c 1m"）
- 第二级：券商名称（GJFXZ、YHDR、ZQSY、ZJ、GF）
- 行索引：股票代码
- 单元格值：报价百分比（例如 13.33 表示 13.33%）

## 模块说明

### config.py
包含所有配置常量：
- 文件路径配置
- API 配置（端点、认证）
- 业务配置（券商、结构、期限）
- 轮询配置

### api_client.py
负责与 API 交互：
- `submit_inquiry()`: 提交期权询价请求
- `fetch_result()`: 轮询并获取询价结果

### data_processor.py
处理数据流程：
- `read_stock_codes()`: 从 Excel 读取股票代码
- `process_stock()`: 处理单只股票的完整流程
- `parse_quotes()`: 解析 API 返回的报价数据
- `build_dataframe()`: 构建输出 DataFrame
- `process_all_stocks()`: 批量处理所有股票

### main.py
程序入口，协调各模块完成整体流程。

## 注意事项

⚠️ **重要提示**：

1. 确保在 `config.py` 中填写正确的 API 端点和认证信息
2. 认证令牌可能会过期，需要定期更新
3. 输入文件第一列必须包含完整的股票代码（含交易所后缀）
4. 如果轮询超时，可以增加 `MAX_POLL_ATTEMPTS` 或 `POLL_INTERVAL`
5. 大批量处理时注意 API 调用频率限制

## 故障排查

**问题：提交询价失败**
- 检查 API 端点是否正确
- 检查认证信息是否有效（Token/Cookie 是否过期）
- 查看错误消息中返回的具体错误码

**问题：未在规定时间内获取到结果**
- 增加 `MAX_POLL_ATTEMPTS`
- 增加 `POLL_INTERVAL`
- 检查网络连接

**问题：输入文件读取失败**
- 确保 `input.xlsx` 存在于当前目录
- 检查文件格式是否正确
- 确保第一列包含股票代码

## 许可证

本项目仅供学习和研究使用。

## 作者

Jerry-Jiayi-He

## 更新日志

### v1.0.0 (2025-10-18)
- 初始版本发布
- 支持批量期权询价
- 模块化代码结构
