import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ArmstrongChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Armstrong Number Checker")
        self.root.geometry("800x600")

        self.create_widgets()
        self.setup_plots()

    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)

        # Single Check Tab
        self.tab_single = ttk.Frame(self.notebook)
        self.create_single_check_tab()

        # Range Check Tab
        self.tab_range = ttk.Frame(self.notebook)
        self.create_range_check_tab()

        # Results Tab
        self.tab_results = ttk.Frame(self.notebook)
        self.create_results_tab()

        self.notebook.add(self.tab_single, text="Single Check")
        self.notebook.add(self.tab_range, text="Range Check")
        self.notebook.add(self.tab_results, text="Results")
        self.notebook.pack(expand=True, fill="both")

    def create_single_check_tab(self):
        frame = ttk.LabelFrame(self.tab_single, text="Check Single Number")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ttk.Label(frame, text="Enter a number:").pack(pady=5)
        self.single_entry = ttk.Entry(frame)
        self.single_entry.pack(pady=5)

        ttk.Button(frame, text="Check",
                   command=self.check_single).pack(pady=10)

        self.single_result = ttk.Label(frame, text="", font=('Helvetica', 12))
        self.single_result.pack(pady=10)

        self.single_time = ttk.Label(frame, text="", font=('Helvetica', 10))
        self.single_time.pack(pady=5)

    def create_range_check_tab(self):
        frame = ttk.LabelFrame(self.tab_range, text="Check Range of Numbers")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ttk.Label(frame, text="From:").pack(pady=5)
        self.range_start = ttk.Entry(frame)
        self.range_start.pack(pady=5)

        ttk.Label(frame, text="To:").pack(pady=5)
        self.range_end = ttk.Entry(frame)
        self.range_end.pack(pady=5)

        ttk.Button(frame, text="Find Armstrong Numbers",
                   command=self.check_range).pack(pady=10)

        self.range_result = tk.Text(frame, height=10, width=50)
        self.range_result.pack(pady=10)

        self.range_time = ttk.Label(frame, text="", font=('Helvetica', 10))
        self.range_time.pack(pady=5)

        btn_frame = ttk.Frame(frame)
        ttk.Button(btn_frame, text="Export to CSV",
                   command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Results",
                   command=self.clear_results).pack(side=tk.LEFT, padx=5)
        btn_frame.pack(pady=10)

    def create_results_tab(self):
        self.results_frame = ttk.Frame(self.tab_results)
        self.results_frame.pack(fill="both", expand=True)

        # Placeholder for plots
        self.plot_frame = ttk.Frame(self.results_frame)
        self.plot_frame.pack(fill="both", expand=True)

    def setup_plots(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def is_armstrong(self, num):
        """Check if a number is Armstrong number (optimized version)"""
        original_num = num
        num_digits = len(str(num))
        sum_of_powers = 0

        while num > 0:
            digit = num % 10
            sum_of_powers += digit ** num_digits
            num = num // 10

        return sum_of_powers == original_num

    def check_single(self):
        try:
            num = int(self.single_entry.get())
            start_time = time.time()
            is_armstrong = self.is_armstrong(num)
            elapsed = (time.time() - start_time) * 1000  # in milliseconds

            if is_armstrong:
                self.single_result.config(
                    text=f"{num} is an Armstrong number!", foreground="green")
            else:
                self.single_result.config(
                    text=f"{num} is NOT an Armstrong number", foreground="red")

            self.single_time.config(text=f"Checked in {elapsed:.4f} ms")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def check_range(self):
        try:
            start = int(self.range_start.get())
            end = int(self.range_end.get())

            if start > end:
                messagebox.showerror("Error", "Start must be less than end")
                return

            self.range_result.delete(1.0, tk.END)
            armstrong_numbers = []

            start_time = time.time()
            for num in range(start, end + 1):
                if self.is_armstrong(num):
                    armstrong_numbers.append(num)
            elapsed = time.time() - start_time

            if armstrong_numbers:
                self.range_result.insert(tk.END, "Armstrong numbers found:\n")
                self.range_result.insert(
                    tk.END, ", ".join(map(str, armstrong_numbers)))

                # Update plot
                self.ax.clear()
                self.ax.bar(range(len(armstrong_numbers)), armstrong_numbers)
                self.ax.set_title("Armstrong Numbers Found")
                self.ax.set_xlabel("Index")
                self.ax.set_ylabel("Number")
                self.canvas.draw()
            else:
                self.range_result.insert(
                    tk.END, "No Armstrong numbers found in this range")

            self.range_time.config(
                text=f"Checked {end-start+1} numbers in {elapsed:.2f} seconds")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")

    def export_to_csv(self):
        try:
            numbers = self.range_result.get(
                1.0, tk.END).strip().split(":")[-1].strip()
            if not numbers or numbers == "No Armstrong numbers found in this range":
                messagebox.showwarning("Warning", "No results to export")
                return

            numbers = list(map(int, numbers.split(", ")))
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Index", "Armstrong Number"])
                    for i, num in enumerate(numbers, 1):
                        writer.writerow([i, num])
                messagebox.showinfo("Success", "Results exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def clear_results(self):
        self.range_result.delete(1.0, tk.END)
        self.range_time.config(text="")
        self.ax.clear()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ArmstrongChecker(root)
    root.mainloop()
