#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JSON 查看工具
支持折叠和扩展功能的 JSON 数据查看器
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os

class JSONViewer:
    """
    JSON 查看器主类
    提供 JSON 数据的可视化查看，支持折叠、扩展、打开文件等功能
    """
    
    def __init__(self, root):
        """
        初始化 JSON 查看器
        
        参数:
            root: Tkinter 根窗口对象
        """
        self.root = root
        self.root.title("JSON 查看器")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 设置中文字体
        self.font = ("SimHei", 10)
        
        # 创建菜单
        self.create_menu()
        
        # 创建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建 JSON 树形视图
        self.create_tree_view()
        
        # 创建状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 当前打开的文件路径
        self.current_file = None
        
        # JSON 数据缓存
        self.json_data = None
    
    def create_menu(self):
        """
        创建菜单栏，包含文件、编辑、帮助等菜单
        """
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="打开文件", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="保存文件", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="展开全部", command=self.expand_all, accelerator="Ctrl+E")
        edit_menu.add_command(label="折叠全部", command=self.collapse_all, accelerator="Ctrl+C")
        menubar.add_cascade(label="编辑", menu=edit_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # 绑定快捷键
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        self.root.bind("<Control-e>", lambda event: self.expand_all())
        self.root.bind("<Control-c>", lambda event: self.collapse_all())
    
    def create_tree_view(self):
        """
        创建 JSON 树形视图和右侧值显示区域
        """
        # 创建分割窗格
        self.paned_window = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧树形视图框架
        tree_frame = tk.Frame(self.paned_window)
        self.paned_window.add(tree_frame, width=300)
        
        # 创建 Treeview 组件
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        tree_scrollbar_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar_x = tk.Scrollbar(self.paned_window, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        # 配置滚动条
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
        
        # 右侧值显示区域
        value_frame = tk.Frame(self.paned_window)
        self.paned_window.add(value_frame, width=400)
        
        # 创建值显示文本框
        tk.Label(value_frame, text="值:", font=self.font).pack(anchor=tk.W, padx=5, pady=5)
        self.value_text = scrolledtext.ScrolledText(value_frame, font=self.font, wrap=tk.WORD)
        self.value_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.value_text.config(state=tk.DISABLED)
        
        # 绑定树形视图事件
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # 添加水平滚动条到底部
        tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_file(self):
        """
        打开 JSON 文件并解析显示
        """
        file_path = filedialog.askopenfilename(
            title="打开 JSON 文件",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.json_data = json.load(file)
                
                self.current_file = file_path
                self.root.title(f"JSON 查看器 - {os.path.basename(file_path)}")
                self.status_var.set(f"已打开文件: {os.path.basename(file_path)}")
                
                # 清空树形视图并重新填充
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                self._populate_tree("", "JSON", self.json_data)
                
            except json.JSONDecodeError as e:
                messagebox.showerror("JSON 解析错误", f"无法解析 JSON 文件:\n{str(e)}")
                self.status_var.set("JSON 解析错误")
            except Exception as e:
                messagebox.showerror("错误", f"打开文件时出错:\n{str(e)}")
                self.status_var.set("打开文件错误")
    
    def save_file(self):
        """
        保存当前 JSON 数据到文件
        """
        if not self.json_data:
            messagebox.showinfo("提示", "没有可保存的数据")
            return
        
        if self.current_file:
            file_path = self.current_file
        else:
            file_path = filedialog.asksaveasfilename(
                title="保存 JSON 文件",
                defaultextension=".json",
                filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
            )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.json_data, file, ensure_ascii=False, indent=2)
                
                self.current_file = file_path
                self.root.title(f"JSON 查看器 - {os.path.basename(file_path)}")
                self.status_var.set(f"已保存文件: {os.path.basename(file_path)}")
                messagebox.showinfo("成功", "文件保存成功")
                
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时出错:\n{str(e)}")
                self.status_var.set("保存文件错误")
    
    def _populate_tree(self, parent, key, value):
        """
        递归填充树形视图
        
        参数:
            parent: 父节点 ID
            key: 当前键名
            value: 当前值
        """
        # 生成节点标签
        if isinstance(key, str):
            node_text = key
        else:
            node_text = str(key)
        
        # 根据值类型添加图标标识
        if isinstance(value, dict):
            node_text += ": {}".format("{...}")
            node = self.tree.insert(parent, "end", text=node_text, open=False)
            for k, v in value.items():
                self._populate_tree(node, k, v)
        elif isinstance(value, list):
            node_text += ": []".format("[...]" if value else "[]")
            node = self.tree.insert(parent, "end", text=node_text, open=False)
            for i, item in enumerate(value):
                self._populate_tree(node, f"[{i}]", item)
        else:
            # 基本类型：字符串、数字、布尔值、None
            value_str = self._format_value(value)
            node_text += f": {value_str}"
            node = self.tree.insert(parent, "end", text=node_text)
            # 存储原始值用于显示
            self.tree.item(node, values=(value_str,))
    
    def _format_value(self, value):
        """
        格式化值的显示
        
        参数:
            value: 要格式化的值
            
        返回:
            str: 格式化后的字符串
        """
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            # 限制字符串长度，过长时截断
            max_length = 50
            if len(value) > max_length:
                return f'"{value[:max_length]}..."'
            return f'"{value}"'
        else:
            return str(value)
    
    def on_tree_select(self, event):
        """
        当树形视图中选择项改变时触发
        
        参数:
            event: 事件对象
        """
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            # 获取完整路径和值
            path = self._get_full_path(item)
            value = self._get_value_by_path(path)
            
            # 在右侧显示完整值
            self.value_text.config(state=tk.NORMAL)
            self.value_text.delete(1.0, tk.END)
            
            if isinstance(value, (dict, list)):
                # 如果是复杂类型，格式化显示
                formatted_value = json.dumps(value, ensure_ascii=False, indent=2)
                self.value_text.insert(tk.END, formatted_value)
            else:
                # 基本类型直接显示
                self.value_text.insert(tk.END, str(value))
            
            self.value_text.config(state=tk.DISABLED)
    
    def _get_full_path(self, item):
        """
        获取节点的完整路径
        
        参数:
            item: 节点 ID
            
        返回:
            list: 路径列表
        """
        path = []
        while item:
            parent = self.tree.parent(item)
            if parent:
                # 提取键名（去掉显示格式）
                text = self.tree.item(item, "text")
                if ":" in text:
                    key = text.split(":", 1)[0].strip()
                else:
                    key = text.strip()
                
                # 处理数组索引
                if key.startswith("[") and key.endswith("]"):
                    try:
                        index = int(key[1:-1])
                        path.insert(0, index)
                    except ValueError:
                        path.insert(0, key)
                else:
                    path.insert(0, key)
            item = parent
        return path
    
    def _get_value_by_path(self, path):
        """
        根据路径获取 JSON 值
        
        参数:
            path: 路径列表
            
        返回:
            对应的值
        """
        if not self.json_data:
            return None
        
        value = self.json_data
        try:
            for key in path:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                elif isinstance(value, list) and isinstance(key, int) and 0 <= key < len(value):
                    value = value[key]
                else:
                    return None
            return value
        except:
            return None
    
    def expand_all(self):
        """
        展开所有节点
        """
        def expand_children(node):
            children = self.tree.get_children(node)
            for child in children:
                self.tree.item(child, open=True)
                expand_children(child)
        
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            expand_children(item)
        
        self.status_var.set("已展开所有节点")
    
    def collapse_all(self):
        """
        折叠所有节点
        """
        def collapse_children(node):
            children = self.tree.get_children(node)
            for child in children:
                self.tree.item(child, open=False)
                collapse_children(child)
        
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            collapse_children(item)
        
        self.status_var.set("已折叠所有节点")
    
    def show_about(self):
        """
        显示关于对话框
        """
        about_text = """
        JSON 查看器 v1.0
        
        一个简单易用的 JSON 文件查看工具，
        支持折叠/扩展、语法高亮等功能。
        
        © 2023 JSON Viewer
        """
        messagebox.showinfo("关于", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    # 设置窗口图标（可选）
    # root.iconbitmap("icon.ico")
    print("JSON 查看器启动中...")
    app = JSONViewer(root)
    root.mainloop()