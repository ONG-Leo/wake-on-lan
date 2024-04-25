import tkinter as tk
from tkinter import messagebox
import socket

def normalize_mac_address(mac_address):
    # 如果输入中包含了:或-分隔符，将其替换为冒号
    if ":" in mac_address:
        return mac_address
    elif "-" in mac_address:
        return mac_address.replace("-", ":")
    else:
        # 如果没有分隔符，则假设用户直接输入了MAC地址，直接返回
        return mac_address

def open_port(port):
    try:
        # 尝试在本地打开指定端口
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('localhost', port))
            print(f"端口 {port} 已成功打开！")
            return True
    except OSError as e:
        # 如果端口已被占用或者其他原因导致打开失败，打印错误信息并返回False
        print(f"无法打开端口 {port}: {e}")
        return False

def send_magic_packet(target_mac, broadcast_address):
    try:
        # 构造魔术包数据
        mac_bytes = bytes.fromhex(target_mac.replace(":", ""))
        magic_packet = b"\xFF" * 6 + mac_bytes * 16
        
        # 创建一个UDP套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 设置套接字为广播模式
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # 先用bind指令绑定端口使用
        udp_socket.bind(('', 9))
        
        # 发送魔术包到广播地址的端口9
        udp_socket.sendto(magic_packet, (broadcast_address, 9))
        
        # 关闭套接字
        udp_socket.close()
        messagebox.showinfo("成功", "魔术包已成功发送")
    except Exception as e:
        messagebox.showerror("错误", f"发送失败: {e}")

def save_input(target_mac, broadcast_address):
    with open("user_input.txt", "w") as file:
        file.write(f"MAC地址: {target_mac}\n")
        file.write(f"广播地址: {broadcast_address}\n")


import re

def load_input():
    try:
        with open("user_input.txt", "r") as file:
            lines = file.readlines()
            # 使用正则表达式来提取MAC地址
            mac_pattern = re.compile(r"MAC地址:\s*([0-9a-fA-F]{2}(?:[:][0-9a-fA-F]{2}){5})")
            # 使用正则表达式来提取广播地址
            broadcast_pattern = re.compile(r"广播地址:\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
            # 在文件中查找MAC地址和广播地址
            target_mac = ""
            broadcast_address = ""
            for line in lines:
                mac_match = mac_pattern.search(line)
                if mac_match:
                    target_mac = mac_match.group(1)
                broadcast_match = broadcast_pattern.search(line)
                if broadcast_match:
                    broadcast_address = broadcast_match.group(1)
            return target_mac, broadcast_address
    except FileNotFoundError:
        return "", ""


def send_magic_packet_gui():
    window = tk.Tk()
    window.title("网络唤醒目标计算机-发送魔术包-V01-20240425")
    
    # 功能介绍
    intro_label = tk.Label(window, text="欢迎使用发送魔术包程序！\n"
                                         "本程序用于发送网络唤醒（Wake-on-LAN）魔术包，"
                                         "以唤醒网络中的目标计算机。\n"
                                         "请确保目标MAC地址和广播地址正确无误。")
    intro_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    # MAC地址格式说明
    mac_format_label = tk.Label(window, text="MAC地址格式示例：00:11:22:33:44:55")
    mac_format_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    
    # 广播地址格式说明
    broadcast_format_label = tk.Label(window, text="广播地址格式示例：192.168.1.255")
    broadcast_format_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    
    # 作者信息
    author_label = tk.Label(window, text="作者：Leo+ChatGPT,+V 13510773588")
    author_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
    
    mac_label = tk.Label(window, text="目标MAC地址：")
    mac_label.grid(row=4, column=0)
    mac_entry = tk.Entry(window)
    mac_entry.grid(row=4, column=1)
    
    broadcast_label = tk.Label(window, text="广播地址：")
    broadcast_label.grid(row=5, column=0)
    broadcast_entry = tk.Entry(window)
    broadcast_entry.grid(row=5, column=1)
    
    # 尝试加载之前保存的用户输入
    target_mac, broadcast_address = load_input()
    mac_entry.insert(0, target_mac)
    broadcast_entry.insert(0, broadcast_address)
    
    def send_packet():
        target_mac = mac_entry.get()
        broadcast_address = broadcast_entry.get()
        send_magic_packet(target_mac, broadcast_address)
        # 保存用户输入
        save_input(target_mac, broadcast_address)
    
    send_button = tk.Button(window, text="发送", command=send_packet)
    send_button.grid(row=6, column=0, columnspan=2, pady=10)
    
    # 获取屏幕大小
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 获取窗口大小
    window_width = 500
    window_height = 300
    
    # 计算窗口位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # 设置窗口位置
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    window.mainloop()

if __name__ == "__main__":
    send_magic_packet_gui()
