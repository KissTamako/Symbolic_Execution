from symbolic.runtime_helpers import init_symbolic_inputs, _se_input, _se_safe_eval, _se_int, _se_str, _se_float, _se_range


# === 学生代码（模块级）- input() 等调用由 PyExZ3 运行时处理 ===

#电费计算：(期末读数 - 期初读数)*单价，电单价0.85元／度，电费保留两位小数
def costCompute(iStart, iEnd):
    iConsume = iEnd - iStart
    unit_price = 0.85
    fee = iConsume * unit_price
    return round(fee, 2)

fElec1,fElec2=eval(input())
fee = costCompute(fElec1, fElec2)
print("%.2f"%fee)

