import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processors.strategy_advisor import StrategyAdvisorProcessor

def main():
    print("=== Generating AI Investment Strategy Prompt ===\n")
    advisor = StrategyAdvisorProcessor()
    
    # 生成供 AI 阅读的 Prompt
    ai_prompt = advisor.generate_ai_prompt()
    
    print(ai_prompt)
    
    # 也可以打印 JSON 原始数据以便调试
    # import json
    # raw_data = advisor.get_aggregated_data()
    # print("\n--- Raw Data (Debug) ---")
    # print(json.dumps(raw_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
