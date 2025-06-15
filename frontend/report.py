import tkinter as tk
from utils import show_info

class ReportUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.report_data = []
        self.master = master
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="报表与财务分析", font=("微软雅黑", 14)).pack(pady=10)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="收入汇总", command=self.show_income, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="成本明细", command=self.show_cost, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="利润分析", command=self.show_profit, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清空", command=self.clear_text, width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="导出报表", command=self.export_report, width=12).pack(side=tk.LEFT, padx=5)
        self.text = tk.Text(self, height=20, width=80)
        self.text.pack(pady=10)

    def show_income(self):
        # 简单统计所有订单收入
        orders = getattr(self.master.master, 'order_list', []) if hasattr(self.master, 'master') else []
        total_income = 0
        for order in orders:
            for meal in order.get('meals', []):
                total_income += meal.get('qty', 0) * meal.get('price', 0)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"总收入：{total_income}\n")

    def show_cost(self):
        # 简单统计所有原料和容器成本
        ingredients = getattr(self.master.master, 'ingredient_list', []) if hasattr(self.master, 'master') else []
        containers = getattr(self.master.master, 'container_list', []) if hasattr(self.master, 'master') else []
        total_cost = sum(i.get('stock', 0) * i.get('price', 0) for i in ingredients)
        total_cost += sum(c.get('stock', 0) * c.get('unit_cost', 0) for c in containers)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"总成本：{total_cost}\n")

    def show_profit(self):
        # 利润 = 收入 - 成本
        self.show_income()
        income = self.text.get(1.0, tk.END).strip().replace('总收入：', '')
        self.show_cost()
        cost = self.text.get(1.0, tk.END).strip().replace('总成本：', '')
        try:
            profit = float(income) - float(cost)
        except:
            profit = 0
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"利润：{profit}\n")

    def clear_text(self):
        self.text.delete(1.0, tk.END)

    def export_report(self):
        content = self.text.get(1.0, tk.END)
        with open('report.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        show_info("导出报表", "报表已导出为 report.txt")

    # Getter/Setter
    def get_report_data(self):
        return self.report_data
    def set_report_data(self, value):
        self.report_data = value
