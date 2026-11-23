import json
import os
from datetime import datetime

import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

FONT = "font.ttf"


def ar(text):
    return get_display(arabic_reshaper.reshape(str(text)))


class ArInput(TextInput):
    def __init__(self, hint, **kwargs):
        super().__init__(
            hint_text=ar(hint),
            font_name=FONT,
            halign="right",
            multiline=False,
            **kwargs,
        )


class ExpenseApp(App):
    def build(self):
        self.title = ar("مدير المصاريف")
        self.data_file = os.path.join(self.user_data_dir, "data.json")
        self.data = self.load_data()

        root = BoxLayout(orientation="vertical", padding=10, spacing=8)

        salary_row = BoxLayout(size_hint_y=None, height=50, spacing=5)
        self.salary_input = ArInput("المرتب الشهري", input_filter="float")
        salary_btn = Button(text=ar("حفظ المرتب"), font_name=FONT, size_hint_x=0.4)
        salary_btn.bind(on_press=self.save_salary)
        salary_row.add_widget(self.salary_input)
        salary_row.add_widget(salary_btn)
        root.add_widget(salary_row)

        self.name_input = ArInput("وصف المصروف", size_hint_y=None, height=50)
        self.amount_input = ArInput("المبلغ", input_filter="float", size_hint_y=None, height=50)
        add_btn = Button(text=ar("إضافة مصروف"), font_name=FONT, size_hint_y=None, height=50)
        add_btn.bind(on_press=self.add_expense)
        root.add_widget(self.name_input)
        root.add_widget(self.amount_input)
        root.add_widget(add_btn)

        self.summary_label = Label(font_name=FONT, size_hint_y=None, height=90, halign="center")
        root.add_widget(self.summary_label)

        self.list_layout = GridLayout(cols=1, spacing=4, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.list_layout)
        root.add_widget(scroll)

        self.refresh()
        return root

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"salary": 0.0, "expenses": []}

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def save_salary(self, instance):
        if self.salary_input.text:
            self.data["salary"] = float(self.salary_input.text)
            self.save_data()
            self.refresh()

    def add_expense(self, instance):
        if self.name_input.text and self.amount_input.text:
            self.data["expenses"].append({
                "name": self.name_input.text,
                "amount": float(self.amount_input.text),
                "date": datetime.now().strftime("%Y-%m-%d"),
            })
            self.name_input.text = ""
            self.amount_input.text = ""
            self.save_data()
            self.refresh()

    def delete_expense(self, index):
        del self.data["expenses"][index]
        self.save_data()
        self.refresh()

    def refresh(self):
        month = datetime.now().strftime("%Y-%m")
        today = datetime.now().strftime("%Y-%m-%d")
        month_expenses = [e for e in self.data["expenses"] if e["date"].startswith(month)]
        today_total = sum(e["amount"] for e in self.data["expenses"] if e["date"] == today)
        month_total = sum(e["amount"] for e in month_expenses)
        remaining = self.data["salary"] - month_total

        self.summary_label.text = ar(
            f"المرتب: {self.data['salary']:.2f}\n"
            f"مصاريف اليوم: {today_total:.2f}  |  مصاريف الشهر: {month_total:.2f}\n"
            f"المتبقي: {remaining:.2f}"
        )

        self.list_layout.clear_widgets()
        for i, e in enumerate(self.data["expenses"]):
            row = BoxLayout(size_hint_y=None, height=40, spacing=5)
            row.add_widget(Label(
                text=ar(f"{e['date']}  {e['name']}  {e['amount']:.2f}"),
                font_name=FONT,
            ))
            del_btn = Button(text=ar("حذف"), font_name=FONT, size_hint_x=0.25)
            del_btn.bind(on_press=lambda inst, idx=i: self.delete_expense(idx))
            row.add_widget(del_btn)
            self.list_layout.add_widget(row)


if __name__ == "__main__":
    ExpenseApp().run()
