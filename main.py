"""
批量期权询价工具 - 主入口
=========================

本模块演示如何通过调用内部微信小程序使用的后端 API 来自动批量查询多只股票的期权报价。
它读取包含股票代码列表的输入 Excel 文件，对每只股票执行询价，并将结果写入输出 Excel 文件。

使用方法
--------
1. 在 config.py 中配置 API 端点和认证信息
2. 准备 input.xlsx 文件，第一列包含股票代码（例如 300476.XSHE）
3. 在 main.py 中配置 DEADLINES_TO_QUERY 列表，指定要查询的期限
4. 运行此脚本：python main.py
5. 查看生成的 output/output_{期限}/ 目录下的结果文件

作者: Jerry-Jiayi-He
项目: option_ask_price
"""

from pathlib import Path
from typing import List, Tuple
import config
from data_processor import process_all_stocks, read_stock_codes


###############################################################################
# 多期限查询配置 - 在这里设置要查询的期限
###############################################################################
# 格式：[(期限代码, 期限标签), ...]
# 期限代码用于 API 请求，期限标签用于显示和文件名
DEADLINES_TO_QUERY: List[Tuple[str, str]] = [
    ("1m", "1个月"),
    ("2m", "2个月"),
    ("3m", "3个月"),
]

# 如果只想查询单个期限，可以这样设置：
# DEADLINES_TO_QUERY = [("1m", "1个月")]


def process_single_deadline(deadline: str, deadline_label: str, stock_codes: List[str]) -> None:
    """处理单个期限的询价。
    
    参数
    ----------
    deadline : str
        期限代码（例如 "1m", "2m", "3m"）
    deadline_label : str
        期限标签（例如 "1个月", "2个月", "3个月"）
    stock_codes : List[str]
        股票代码列表
    """
    print("\n" + "=" * 60)
    print(f"开始处理期限: {deadline} ({deadline_label})")
    print("=" * 60)
    
    # 动态更新 config 模块的期限参数
    config.DEADLINE = deadline
    config.DEADLINE_LABEL = deadline_label
    
    # 重新计算输出路径
    output_dir = f"output/output_{deadline}"
    intermediate_dir = f"{output_dir}/intermediate"
    output_file = f"{output_dir}/final_result_{deadline}.xlsx"
    
    # 更新 config 模块的路径
    config.OUTPUT_DIR = output_dir
    config.INTERMEDIATE_DIR = intermediate_dir
    config.OUTPUT_FILE = output_file
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"\n输出目录: {output_dir}")
    print(f"最终文件: {output_file}")
    
    # 批量处理所有股票
    print(f"\n正在执行批量询价...")
    print(f"这可能需要一些时间，请耐心等待...")
    df_result = process_all_stocks(stock_codes)
    
    # 写入结果
    print(f"\n正在写入输出文件: {output_file}")
    df_result.to_excel(output_file)
    print(f"✅ 成功！已将结果写入 '{output_file}'")
    
    print("\n" + "=" * 60)
    print(f"期限 {deadline} ({deadline_label}) 处理完成！")
    print("=" * 60)


def main() -> None:
    """主入口点，用于读取输入、执行多期限询价并写入输出。"""
    print("=" * 80)
    print(" " * 30 + "批量期权询价工具")
    print("=" * 80)
    
    # 显示要查询的期限
    print(f"\n将查询以下期限: {', '.join([f'{d}({l})' for d, l in DEADLINES_TO_QUERY])}")
    print(f"共 {len(DEADLINES_TO_QUERY)} 个期限\n")
    
    # 读取股票代码（只读取一次）
    print(f"正在读取输入文件: {config.INPUT_FILE}")
    stock_codes = read_stock_codes(config.INPUT_FILE)
    print(f"✅ 成功读取 {len(stock_codes)} 只股票代码\n")
    
    # 循环处理每个期限
    for idx, (deadline, deadline_label) in enumerate(DEADLINES_TO_QUERY, 1):
        print(f"\n{'#' * 80}")
        print(f"进度: [{idx}/{len(DEADLINES_TO_QUERY)}] 期限: {deadline} ({deadline_label})")
        print(f"{'#' * 80}")
        
        try:
            process_single_deadline(deadline, deadline_label, stock_codes)
        except Exception as e:
            print(f"\n❌ 错误：处理期限 {deadline} 时发生异常: {e}")
            print(f"继续处理下一个期限...\n")
            continue
    
    
    # 所有期限处理完成
    print("\n" + "=" * 80)
    print(" " * 30 + "🎉 全部处理完成！🎉")
    print("=" * 80)
    print(f"\n共处理 {len(DEADLINES_TO_QUERY)} 个期限，{len(stock_codes)} 只股票")
    print("\n输出文件位置:")
    for deadline, deadline_label in DEADLINES_TO_QUERY:
        output_path = f"output/output_{deadline}/final_result_{deadline}.xlsx"
        print(f"  - {deadline} ({deadline_label}): {output_path}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
