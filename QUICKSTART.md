# 快速开始指南

## 🚀 5 分钟快速上手

### 第 1 步：安装依赖

```bash
pip install -r requirements.txt
```

### 第 2 步：配置 API

编辑 `config.py`，替换以下内容：

```python
# 第 27-28 行：替换 API 端点
CREATE_URL = "https://你的服务器地址/app-api/option-ask/create"
RESULT_URL = "https://你的服务器地址/app-api/option-ask/result"

# 第 35-38 行：替换认证信息
HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Authorization": "Bearer 你的令牌",
    "Cookie": "你的Cookie",
}
```

💡 **提示：** 使用 Fiddler 或浏览器 F12 开发者工具抓包获取这些信息

### 第 3 步：准备输入文件

创建 `input.xlsx`，在第一列输入股票代码：

```
300476.XSHE
000001.XSHE
600000.XSHG
```

### 第 4 步：运行程序

```bash
python main.py
```

### 第 5 步：查看结果

程序会生成 `output.xlsx`，包含所有股票的期权报价。

---

## 📋 完整工作流程

```
┌─────────────────┐
│   准备输入文件   │  input.xlsx
│  (股票代码列表)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  运行 main.py   │  python main.py
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  读取股票代码   │  read_stock_codes()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  批量处理股票   │  process_all_stocks()
│                 │
│  对每只股票：    │
│  1. 提交询价    │  submit_inquiry()
│  2. 轮询结果    │  fetch_result()
│  3. 解析报价    │  parse_quotes()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  构建 DataFrame │  build_dataframe()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  保存到 Excel   │  output.xlsx
└─────────────────┘
```

---

## ⚙️ 可选配置

### 修改券商列表

编辑 `config.py` 第 45 行：

```python
TARGET_VENDORS = ["GJFXZ", "YHDR", "ZQSY", "ZJ", "GF"]
```

### 修改期权结构

编辑 `config.py` 第 50-54 行：

```python
STRUCTURES = {
    "90c": "实值90",
    "100c": "平值100",
    "105c": "虚值105",
}
```

### 修改期限

编辑 `config.py` 第 57 行：

```python
DEADLINE = "1m"  # 1个月，可改为 "2m", "3m" 等
```

### 调整轮询参数

编辑 `config.py` 第 74-75 行：

```python
POLL_INTERVAL = 0.5      # 轮询间隔（秒）
MAX_POLL_ATTEMPTS = 10   # 最大轮询次数
```

---

## 🔍 常见问题

### Q1: 如何获取 API 端点和认证信息？

**A:** 使用 Fiddler 或浏览器开发者工具：

1. 打开 Fiddler / 浏览器 F12
2. 在微信小程序中执行一次询价
3. 找到对应的 HTTP 请求
4. 复制 URL → `CREATE_URL` 和 `RESULT_URL`
5. 复制 Headers → `Authorization` 和 `Cookie`

### Q2: 认证令牌过期怎么办？

**A:** 重新抓包获取新的令牌，更新 `config.py` 中的 `HEADERS`。

### Q3: 如何处理大批量股票？

**A:** 可以：
- 增加 `MAX_POLL_ATTEMPTS` 避免超时
- 添加进度显示（在 `process_all_stocks` 中）
- 分批处理（将输入文件拆分）

### Q4: 可以导入为 Python 包使用吗？

**A:** 可以！示例：

```python
from data_processor import process_stock

# 单独处理一只股票
quotes = process_stock("300476")
print(quotes)
```

### Q5: 如何自定义输出格式？

**A:** 修改 `data_processor.py` 中的 `build_dataframe()` 函数，调整列名和数据格式。

---

## 📞 获取帮助

1. **查看详细文档：** `README.md`
2. **了解架构设计：** `ARCHITECTURE.md`
3. **检查代码注释：** 每个函数都有详细的文档字符串

---

## ✅ 检查清单

部署前确认：

- [ ] 已安装所有依赖 (`pip install -r requirements.txt`)
- [ ] 已配置 API 端点 (`CREATE_URL`, `RESULT_URL`)
- [ ] 已配置认证信息 (`HEADERS`)
- [ ] 已准备输入文件 (`input.xlsx`)
- [ ] 测试运行成功

---

**祝使用愉快！** 🎉
