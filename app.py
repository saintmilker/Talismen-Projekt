import psutil
import tkinter as tk
import os
import ctypes


def set_app_icon():
    app_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico")
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    root.iconbitmap(app_icon)

class DiskSpaceGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x400")
        self.master.config(bg="black")
        self.master.title("Talismen Experience")
        set_app_icon()
        self.master.resizable(False, False)

        self.current_disk = 0

        self.disk_label = tk.Label(self.master, text="Disk C:", font=("Courier", 23, "bold"), bg="black", fg="white")
        self.disk_label.pack(pady=20)

        self.percentage_label = tk.Label(self.master, text="", font=("Courier", 45), bg="black", fg="white")
        self.percentage_label.pack(pady=20)

        self.gb_label = tk.Label(self.master, text="", font=("Courier", 23), bg="black", fg="white")
        self.gb_label.pack(pady=10)

        self.button_frame = tk.Frame(self.master, bg="black")
        self.button_frame.pack()

        disks = psutil.disk_partitions()
        self.disk_buttons = []
        for i, disk in enumerate(disks):
            disk_name = disk.device.split(":")[0]
            button_text = f"Disk {disk_name}"
            if i == self.current_disk:
                button_color = "#000080"  # Darker blue for current disk button
            else:
                button_color = "#0000FF"
            button = tk.Button(self.button_frame, text=button_text, font=("Courier", 16, "bold"), bg=button_color, fg="white", command=lambda idx=i: self.show_disk(idx))
            button.pack(side="left", padx=10)
            self.disk_buttons.append(button)

        self.show_disk(0)

    def show_disk(self, disk_num):
        self.current_disk = disk_num
        disk = psutil.disk_partitions()[disk_num]
        disk_name = disk.device.split(":")[0]
        self.disk_label.config(text=f"Disk {disk_name}:")
        usage = psutil.disk_usage(disk.mountpoint)
        total_gb = round(usage.total / (1024 ** 3), 2)
        used_gb = round(usage.used / (1024 ** 3), 2)
        free_gb = round(usage.free / (1024 ** 3), 2)
        percent_left = 100 - usage.percent
        self.percentage_label.config(text=f"{percent_left}%", fg="white")
        self.gb_label.config(text=f"{free_gb} GB left", fg="white")

        # Update button colors to highlight current disk button
        for i, button in enumerate(self.disk_buttons):
            if i == self.current_disk:
                button.config(bg="#00003f")
            else:
                button.config(bg="#0000FF")

root = tk.Tk()
gui = DiskSpaceGUI(root)
root.mainloop()