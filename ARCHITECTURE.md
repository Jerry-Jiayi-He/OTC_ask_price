# 项目架构说明

## 📁 文件结构

```
option_ask_price/
│
├── 📄 main.py                  # 主入口 (249 行) - 简洁的程序入口
├── 📄 config.py                # 配置模块 (58 行) - 所有配置常量
├── 📄 api_client.py            # API 客户端 (88 行) - HTTP 请求处理
├── 📄 data_processor.py        # 数据处理 (156 行) - 业务逻辑核心
├── 📄 __init__.py              # 包初始化 (50 行) - 导出接口
│
├── 📄 README.md                # 项目文档 (135 行)
├── 📄 requirements.txt         # 依赖列表 (3 行)
├── 📄 .gitignore               # Git 忽略规则 (43 行)
│
├── 📊 input.xlsx               # 输入文件（用户创建）
└── 📊 output.xlsx              # 输出文件（程序生成）
```

## 🔄 模块依赖关系

```
main.py
  ├── config.py
  └── data_processor.py
       ├── config.py
       └── api_client.py
            └── config.py
```

## 📦 模块职责划分

### 1️⃣ config.py - 配置中心
**职责：** 集中管理所有配置项
- ✅ 文件路径配置
- ✅ API 端点和认证
- ✅ 业务参数（券商、结构、期限）
- ✅ 轮询参数

**优势：**
- 单一配置源
- 易于维护和修改
- 避免硬编码

### 2️⃣ api_client.py - API 交互层
**职责：** 封装所有 HTTP 请求
- ✅ `submit_inquiry()` - 提交询价
- ✅ `fetch_result()` - 获取结果

**优势：**
- 解耦 API 调用逻辑
- 便于测试和 Mock
- 统一错误处理

### 3️⃣ data_processor.py - 业务逻辑层
**职责：** 处理数据流转和业务逻辑
- ✅ `read_stock_codes()` - 读取输入
- ✅ `process_stock()` - 处理单股票
- ✅ `parse_quotes()` - 解析报价
- ✅ `build_dataframe()` - 构建数据框
- ✅ `process_all_stocks()` - 批量处理

**优势：**
- 业务逻辑集中
- 函数职责单一
- 易于扩展和复用

### 4️⃣ main.py - 应用入口
**职责：** 协调各模块，提供用户界面
- ✅ 简洁的主函数
- ✅ 友好的进度提示
- ✅ 清晰的执行流程

**优势：**
- 代码简洁（仅 ~50 行核心代码）
- 流程清晰
- 易于理解

## 🎯 设计模式

### 1. 分层架构
```
表现层 (main.py)
    ↓
业务层 (data_processor.py)
    ↓
服务层 (api_client.py)
    ↓
配置层 (config.py)
```

### 2. 单一职责原则 (SRP)
每个模块只负责一个明确的职责：
- `config.py` → 配置管理
- `api_client.py` → API 通信
- `data_processor.py` → 数据处理
- `main.py` → 流程控制

### 3. 依赖注入
通过导入模块和参数传递实现松耦合

## 🚀 扩展建议

### 未来可以添加的模块：

1. **logger.py** - 日志模块
   - 统一日志格式
   - 文件和控制台输出
   - 日志级别控制

2. **validator.py** - 数据验证模块
   - 输入数据校验
   - 配置参数检查
   - 结果完整性验证

3. **exception.py** - 自定义异常模块
   - API 异常
   - 数据异常
   - 配置异常

4. **utils.py** - 工具函数模块
   - 通用辅助函数
   - 格式化工具
   - 时间处理

5. **cache.py** - 缓存模块
   - 结果缓存
   - 减少重复请求
   - 提高性能

## 📊 代码质量指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 总代码行数 | ~600 行 | 原始代码 ~300 行，重构后更清晰 |
| 模块数量 | 4 个核心模块 | 职责分明 |
| 函数平均长度 | ~20 行 | 易于理解和维护 |
| 最大文件行数 | 156 行 | 模块大小适中 |
| 注释覆盖率 | 100% | 所有函数都有文档字符串 |

## ✅ 重构优势

### 重构前（单文件）：
❌ 300+ 行代码在一个文件
❌ 配置和代码混杂
❌ 难以维护和测试
❌ 代码复用困难

### 重构后（模块化）：
✅ 代码分散到 4 个模块
✅ 配置独立管理
✅ 易于单元测试
✅ 便于团队协作
✅ 支持渐进式开发

## 🔧 使用示例

### 作为脚本使用：
```bash
python main.py
```

### 作为模块导入：
```python
from data_processor import process_stock
from config import STRUCTURES

# 处理单只股票
quotes = process_stock("300476")
print(quotes)
```

## 📝 维护建议

1. **配置变更** → 只需修改 `config.py`
2. **API 变更** → 只需修改 `api_client.py`
3. **业务逻辑变更** → 只需修改 `data_processor.py`
4. **界面优化** → 只需修改 `main.py`

每次修改都是局部的，不会影响其他模块！
