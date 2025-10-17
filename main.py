"""
批量期权询价工具 - 主入口
=========================

本模块演示如何通过调用内部微信小程序使用的后端 API 来自动批量查询多只股票的期权报价。
它读取包含股票代码列表的输入 Excel 文件，对每只股票执行询价，并将结果写入输出 Excel 文件。

使用方法
--------
1. 在 config.py 中配置 API 端点和认证信息
2. 准备 input.xlsx 文件，第一列包含股票代码（例如 300476.XSHE）
3. 运行此脚本：python main.py
4. 查看生成的 output.xlsx 文件

作者: Jerry-Jiayi-He
项目: option_ask_price
"""

from config import INPUT_FILE, OUTPUT_FILE
from data_processor import process_all_stocks, read_stock_codes


def main() -> None:
    """主入口点，用于读取输入、执行询价并写入输出。"""
    print("=" * 60)
    print("批量期权询价工具")
    print("=" * 60)
    
    # 读取股票代码
    print(f"\n[1/3] 正在读取输入文件: {INPUT_FILE}")
    stock_codes = read_stock_codes(INPUT_FILE)
    print(f"      成功读取 {len(stock_codes)} 只股票代码")
    
    # 批量处理所有股票
    print(f"\n[2/3] 正在执行批量询价...")
    print(f"      这可能需要一些时间，请耐心等待...")
    df_result = process_all_stocks(stock_codes)
    
    # 写入结果
    print(f"\n[3/3] 正在写入输出文件: {OUTPUT_FILE}")
    df_result.to_excel(OUTPUT_FILE)
    print(f"      成功！已将结果写入 '{OUTPUT_FILE}'")
    
    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
