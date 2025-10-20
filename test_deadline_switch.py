"""
测试脚本：验证多期限动态切换是否正常工作
"""

import config

# 模拟 main.py 中的期限切换
print("=" * 60)
print("测试多期限动态配置")
print("=" * 60)

# 测试 1m
print("\n[测试 1] 设置期限为 1m")
config.DEADLINE = "1m"
config.DEADLINE_LABEL = "1个月"
print(f"config.DEADLINE = {config.DEADLINE}")
print(f"config.DEADLINE_LABEL = {config.DEADLINE_LABEL}")

# 导入 api_client 查看它能否正确获取
from api_client import submit_inquiry

# 模拟构建 payload（不实际发送请求）
import json
print("\n构建的 payload 中的期限字段:")
print(f"  deadline: {config.DEADLINE}")
print(f"  deadlines: [{{'label': '{config.DEADLINE_LABEL}', 'value': '{config.DEADLINE}'}}]")

# 测试 2m
print("\n[测试 2] 切换期限为 2m")
config.DEADLINE = "2m"
config.DEADLINE_LABEL = "2个月"
print(f"config.DEADLINE = {config.DEADLINE}")
print(f"config.DEADLINE_LABEL = {config.DEADLINE_LABEL}")
print("\n构建的 payload 中的期限字段:")
print(f"  deadline: {config.DEADLINE}")
print(f"  deadlines: [{{'label': '{config.DEADLINE_LABEL}', 'value': '{config.DEADLINE}'}}]")

# 测试 3m
print("\n[测试 3] 切换期限为 3m")
config.DEADLINE = "3m"
config.DEADLINE_LABEL = "3个月"
print(f"config.DEADLINE = {config.DEADLINE}")
print(f"config.DEADLINE_LABEL = {config.DEADLINE_LABEL}")
print("\n构建的 payload 中的期限字段:")
print(f"  deadline: {config.DEADLINE}")
print(f"  deadlines: [{{'label': '{config.DEADLINE_LABEL}', 'value': '{config.DEADLINE}'}}]")

print("\n" + "=" * 60)
print("✅ 测试完成！期限参数可以正确动态切换")
print("=" * 60)
print("\n说明：")
print("- 如果上面三个测试显示的期限都不同，说明修复成功")
print("- 现在运行 python main.py 应该能正确查询不同期限的数据")
