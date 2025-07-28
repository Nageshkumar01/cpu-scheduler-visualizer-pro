import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import subprocess
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import numpy as np

color_map = {}

def generate_color(name):
    if name not in color_map:
        color_map[name] = "#%06x" % random.randint(0x444444, 0xFFFFFF)
    return color_map[name]

algorithm_names = [
    ("", "Select a Scheduling Algorithm"),
    ("FCFS", "First-Come-First-Serve: Non-preemptive, by arrival time."),
    ("RR-", "Round Robin: Time-sliced scheduling."),
    ("SPN", "Shortest Process Next: Non-preemptive, by burst time."),
    ("SRT", "Shortest Remaining Time: Preemptive SPN."),
    ("HRRN", "Highest Response Ratio Next: Based on response ratio."),
    ("FB-1", "Feedback with fixed quantum = 1."),
    ("FB-2i", "Feedback with increasing quantum 2^i."),
    ("AGING", "Aging: Priorities increase over time.")
]

def parse_output_for_gantt(output):
    lines = output.strip().split("\n")
    process_blocks = {}
    time_line = []

    in_gantt = False
    for line in lines:
        if any(alg in line for alg, _ in algorithm_names if alg):
            time_line = line.strip().split()[1:]
            in_gantt = True
        elif in_gantt and '|' in line:
            parts = line.strip().split()
            if len(parts) > 1:
                pname = parts[0]
                bars = ''.join(parts[1:]).replace('|', '')
                process_blocks[pname] = list(bars)
        elif in_gantt and '-' in line:
            continue
    return time_line, process_blocks

def parse_scheduling_metrics(output):
    """Parse scheduling metrics from output for timeline graph"""
    lines = output.strip().split("\n")
    processes = {}
    
    # Look for process completion information
    for line in lines:
        if "Process" in line and ("finished" in line or "completed" in line):
            # Try to extract process completion data
            parts = line.split()
            if len(parts) >= 4:
                process_name = parts[1]
                # Extract timing information if available
                for i, part in enumerate(parts):
                    if part.isdigit():
                        processes[process_name] = {"completion_time": int(part)}
    
    return processes

def draw_gantt_chart(time_line, process_blocks):
    canvas.delete("all")
    
    if not process_blocks:
        canvas.create_text(250, 150, text="No data to display", 
                          font=("Arial", 12), fill="#7f8c8d")
        return
    
    cell_width = 25
    cell_height = 30
    padding = 40
    
    # Draw title
    canvas.create_text(250, 15, text="Gantt Chart", 
                      font=("Arial", 12, "bold"), fill="#2c3e50")
    
    # Draw time axis
    if time_line:
        for i, time in enumerate(time_line):
            if i * cell_width + padding < 480:  # Fit within canvas width
                x = padding + i * cell_width + cell_width // 2
                canvas.create_text(x, 35, text=str(time), 
                                 font=("Arial", 8, "bold"), fill="#34495e")
                # Draw vertical grid lines
                canvas.create_line(x, 45, x, 45 + len(process_blocks) * (cell_height + 3), 
                                 fill="#bdc3c7", width=1)
    
    # Draw process blocks with enhanced styling
    for row_index, (pname, bars) in enumerate(process_blocks.items()):
        color = generate_color(pname)
        y_offset = 50 + row_index * (cell_height + 3)
        
        # Process name label with background
        canvas.create_rectangle(5, y_offset, 35, y_offset + cell_height, 
                              fill="#34495e", outline="#2c3e50")
        canvas.create_text(20, y_offset + cell_height//2, text=pname, 
                          font=("Arial", 9, "bold"), fill="white")
        
        for col_index, mark in enumerate(bars):
            if mark in '*.' or mark.strip():
                if col_index * cell_width + padding < 480:  # Fit within canvas
                    x1 = padding + col_index * cell_width
                    y1 = y_offset
                    x2 = x1 + cell_width
                    y2 = y1 + cell_height
                    
                    # Create gradient effect
                    canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=color, outline="#2c3e50", width=1)
                    # Add inner highlight
                    canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, 
                                          fill="", outline="white", width=1)
                    
                    # Process execution marker
                    canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text=mark, 
                                     fill="white", font=("Arial", 8, "bold"))

def create_timeline_graph(time_line, process_blocks):
    """Create a timeline graph using matplotlib"""
    try:
        # Clear previous plot
        for widget in timeline_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        
        if not process_blocks:
            return
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#ecf0f1')
        
        processes = list(process_blocks.keys())
        colors = [generate_color(p) for p in processes]
        
        # Create timeline bars
        for i, (process, bars) in enumerate(process_blocks.items()):
            y_pos = i
            for j, mark in enumerate(bars):
                if mark in '*.' or mark.strip():
                    rect = patches.Rectangle((j, y_pos), 1, 0.8, 
                                           linewidth=1, edgecolor='black', 
                                           facecolor=generate_color(process), alpha=0.8)
                    ax.add_patch(rect)
                    # Add process label in the center
                    ax.text(j + 0.5, y_pos + 0.4, mark, ha='center', va='center', 
                           fontweight='bold', color='white', fontsize=8)
        
        # Customize the plot
        ax.set_xlim(0, len(time_line) if time_line else 10)
        ax.set_ylim(-0.5, len(processes) - 0.5)
        ax.set_xlabel('Time Units', fontweight='bold', fontsize=9)
        ax.set_ylabel('Processes', fontweight='bold', fontsize=9)
        ax.set_title('Process Timeline', fontweight='bold', pad=15, fontsize=10)
        
        # Set y-axis labels
        ax.set_yticks(range(len(processes)))
        ax.set_yticklabels(processes)
        
        # Set x-axis labels
        if time_line:
            ax.set_xticks(range(len(time_line)))
            ax.set_xticklabels(time_line)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        ax.set_axisbelow(True)
        
        # Adjust layout for smaller space
        plt.tight_layout()
        
        # Embed the plot in tkinter
        canvas_widget = FigureCanvasTkAgg(fig, timeline_frame)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        plt.close(fig)  # Close the figure to free memory
        
    except Exception as e:
        print(f"Error creating timeline graph: {e}")

def animate_button(button):
    """Simple button animation effect"""
    original_bg = button.cget("bg")
    button.configure(bg="#0d7ec7")
    root.after(100, lambda: button.configure(bg=original_bg))

def update_description(event):
    selected_index = algo_combobox.current()
    if selected_index >= 0 and selected_index < len(algorithm_names):
        _, description = algorithm_names[selected_index]
        algo_description_var.set(description)
        
        # Special handling for aging algorithm
        if selected_index == 8:  # AGING algorithm
            algo_description_var.set("Aging: Priorities increase over time. Processes age to prevent starvation.")
        
        # Animate the description update
        algo_description.configure(fg="#27ae60")
        root.after(500, lambda: algo_description.configure(fg="#7f8c8d"))

def validate_inputs():
    """Validate user inputs before running scheduler"""
    try:
        total_time = int(time_entry.get())
        process_count = int(process_count_entry.get())
        
        if total_time <= 0 or process_count <= 0:
            raise ValueError("Values must be positive")
        
        if process_count > 50:  # Reasonable upper limit
            raise ValueError("Too many processes (max 50)")
            
        process_data = process_text.get("1.0", tk.END).strip().split("\n")
        valid_lines = [line for line in process_data if line.strip()]
        
        if len(valid_lines) != process_count:
            raise ValueError(f"Process count mismatch: expected {process_count}, got {len(valid_lines)}")
        
        for line_num, line in enumerate(valid_lines, 1):
            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Line {line_num}: Invalid format (need name,arrival,service)")
            
            name, arrival, service = parts
            if not name.strip():
                raise ValueError(f"Line {line_num}: Process name cannot be empty")
            
            try:
                arrival_time = int(arrival.strip())
                service_time = int(service.strip())
                if arrival_time < 0 or service_time <= 0:
                    raise ValueError(f"Line {line_num}: Times must be non-negative (service > 0)")
            except ValueError:
                raise ValueError(f"Line {line_num}: Arrival and service times must be integers")
        
        return True
    except ValueError as e:
        messagebox.showerror("Input Error", 
                           f"Please check your inputs:\n{str(e)}")
        return False

def run_scheduler():
    global color_map
    
    if not validate_inputs():
        return
        
    color_map = {}
    
    # Animate button
    animate_button(run_button)
    
    # Show progress
    status_var.set("Running scheduler...")
    root.update()

    operation = operation_entry.get()
    algo_index = algo_combobox.current()
    if algo_index < 1:
        messagebox.showerror("Error", "Please select a valid algorithm.")
        status_var.set("Ready")
        return
        
    algorithms = str(algo_index)
    total_time = time_entry.get()
    num_processes = process_count_entry.get()
    process_data = process_text.get("1.0", tk.END).strip().split("\n")
    
    # Filter out empty lines
    process_data = [line for line in process_data if line.strip()]

    input_data = f"{operation}\n{algorithms}\n{total_time}\n{num_processes}\n" + "\n".join(process_data)
    
    # Debug: Show input data in status
    print(f"Input data:\n{input_data}")

    try:
        result = subprocess.run(
            ["main.exe"],
            input=input_data.encode(),
            capture_output=True,
            timeout=10  # Increased timeout for aging algorithm
        )
        
        output = result.stdout.decode()
        error_output = result.stderr.decode()
        
        output_area.delete("1.0", tk.END)
        
        if result.returncode != 0:
            output_area.insert(tk.END, f"Error (Return code: {result.returncode}):\n")
            output_area.insert(tk.END, f"STDOUT:\n{output}\n")
            output_area.insert(tk.END, f"STDERR:\n{error_output}")
            status_var.set("Scheduler failed!")
        else:
            output_area.insert(tk.END, output)
            
            time_line, process_blocks = parse_output_for_gantt(output)
            draw_gantt_chart(time_line, process_blocks)
            create_timeline_graph(time_line, process_blocks)
            
            status_var.set("Scheduler completed successfully!")
        
        # Ensure the text is visible and scrollable
        output_area.see(tk.END)
        output_area.update_idletasks()
        
        root.after(3000, lambda: status_var.set("Ready"))

    except subprocess.TimeoutExpired:
        output_area.delete("1.0", tk.END)
        output_area.insert(tk.END, "Error: Scheduler timed out (took longer than 10 seconds)")
        output_area.see(tk.END)
        status_var.set("Timeout error!")
        root.after(3000, lambda: status_var.set("Ready"))
    except Exception as e:
        output_area.delete("1.0", tk.END)
        output_area.insert(tk.END, f"Error running scheduler:\n{str(e)}")
        output_area.see(tk.END)
        output_area.update_idletasks()
        status_var.set("Error occurred!")
        root.after(3000, lambda: status_var.set("Ready"))

def add_process():
    """Add a new process line"""
    current_count = int(process_count_entry.get())
    new_count = current_count + 1
    process_count_entry.delete(0, tk.END)
    process_count_entry.insert(0, str(new_count))
    
    # Add a new process line
    current_text = process_text.get("1.0", tk.END).strip()
    if current_text:
        new_process = f"\nP{new_count},0,3"
    else:
        new_process = f"P{new_count},0,3"
    
    process_text.insert(tk.END, new_process)

def remove_process():
    """Remove the last process line"""
    current_count = int(process_count_entry.get())
    if current_count > 1:
        new_count = current_count - 1
        process_count_entry.delete(0, tk.END)
        process_count_entry.insert(0, str(new_count))
        
        # Remove last line
        lines = process_text.get("1.0", tk.END).strip().split("\n")
        if lines:
            lines.pop()
            process_text.delete("1.0", tk.END)
            process_text.insert("1.0", "\n".join(lines))

def clear_all():
    """Clear all inputs and outputs"""
    process_text.delete("1.0", tk.END)
    process_text.insert(tk.END, "A,0,3\nB,2,6\nC,4,4\nD,6,5\nE,8,2")
    output_area.delete("1.0", tk.END)
    output_area.insert("1.0", "Scheduler output will appear here after running...")
    output_area.update_idletasks()
    canvas.delete("all")
    
    # Clear timeline graph
    for widget in timeline_frame.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()
    
    time_entry.delete(0, tk.END)
    time_entry.insert(0, "20")
    process_count_entry.delete(0, tk.END)
    process_count_entry.insert(0, "5")
    algo_combobox.current(0)
    update_description(None)
    status_var.set("Inputs cleared")
    root.after(2000, lambda: status_var.set("Ready"))

# Create main window with enhanced styling
root = tk.Tk()
root.title("🖥️ CPU Scheduler Visualizer Pro")
root.configure(bg="#ecf0f1")
root.geometry("1400x900")
root.resizable(True, True)

# Configure custom fonts
title_font = font.Font(family="Arial", size=16, weight="bold")
label_font = font.Font(family="Arial", size=10, weight="bold")
input_font = font.Font(family="Arial", size=10)

# Configure custom styles
style = ttk.Style()
style.theme_use('clam')
style.configure('Custom.TCombobox', fieldbackground='white', background='#3498db')

# Title section
title_frame = tk.Frame(root, bg="#2c3e50", relief="raised", bd=2)
title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
title_label = tk.Label(title_frame, text="🖥️ CPU Scheduler Visualizer Pro", 
                      font=title_font, fg="white", bg="#2c3e50", pady=10)
title_label.pack()

# Left side - Algorithm Configuration (NOW GETS MORE SPACE)
config_frame = tk.LabelFrame(root, text="⚙️ Algorithm Configuration", font=label_font, 
                           bg="#ecf0f1", fg="#2c3e50", relief="groove", bd=2)
config_frame.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=5)

# Operation input
tk.Label(config_frame, text="Operation:", bg="#ecf0f1", font=label_font, fg="#34495e").grid(row=0, column=0, sticky='w', padx=10, pady=5)
operation_entry = tk.Entry(config_frame, width=25, font=input_font, relief="groove", bd=2)
operation_entry.insert(0, "trace")
operation_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

# Algorithm selection
tk.Label(config_frame, text="Select Algorithm:", bg="#ecf0f1", font=label_font, fg="#34495e").grid(row=1, column=0, sticky='w', padx=10, pady=5)
algo_combobox = ttk.Combobox(config_frame, values=[name for name, _ in algorithm_names], 
                            state="readonly", width=23, font=input_font, style='Custom.TCombobox')
algo_combobox.current(1)
algo_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
algo_combobox.bind("<<ComboboxSelected>>", update_description)

# Algorithm description
algo_description_var = tk.StringVar()
algo_description = tk.Label(config_frame, textvariable=algo_description_var, wraplength=300, 
                           justify="left", bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 9, "italic"))
algo_description.grid(row=2, column=0, columnspan=2, sticky='w', padx=10, pady=2)
update_description(None)

# Time input
tk.Label(config_frame, text="Total Time:", bg="#ecf0f1", font=label_font, fg="#34495e").grid(row=3, column=0, sticky='w', padx=10, pady=5)
time_entry = tk.Entry(config_frame, width=25, font=input_font, relief="groove", bd=2)
time_entry.insert(0, "20")
time_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

# Configure grid weights for config frame
config_frame.grid_columnconfigure(1, weight=1)

# Middle - Scheduler Output (NOW GETS LESS SPACE)
output_frame = tk.LabelFrame(root, text="📊 Scheduler Output", font=label_font, 
                            bg="#ecf0f1", fg="#2c3e50", relief="groove", bd=2)
output_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

output_area = scrolledtext.ScrolledText(output_frame, width=50, height=18, 
                                       font=("Courier New", 9), relief="groove", bd=2,
                                       bg="#f8f9fa", selectbackground="#3498db",
                                       wrap=tk.WORD)
output_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Right side - Process Configuration
process_frame = tk.LabelFrame(root, text="📝 Process Configuration", font=label_font, 
                            bg="#ecf0f1", fg="#2c3e50", relief="groove", bd=2)
process_frame.grid(row=1, column=2, sticky="nsew", padx=(5,10), pady=5)

# Process count with add/remove buttons
tk.Label(process_frame, text="Process Count:", bg="#ecf0f1", font=label_font, fg="#34495e").grid(row=0, column=0, sticky='w', padx=10, pady=5)

process_count_frame = tk.Frame(process_frame, bg="#ecf0f1")
process_count_frame.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

process_count_entry = tk.Entry(process_count_frame, width=15, font=input_font, relief="groove", bd=2)
process_count_entry.insert(0, "5")
process_count_entry.pack(side=tk.LEFT, fill='x', expand=True)

add_btn = tk.Button(process_count_frame, text="+", command=add_process, 
                   bg="#27ae60", fg="white", font=("Arial", 9, "bold"), width=2)
add_btn.pack(side=tk.RIGHT, padx=(2,0))

remove_btn = tk.Button(process_count_frame, text="-", command=remove_process, 
                      bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), width=2)
remove_btn.pack(side=tk.RIGHT, padx=2)

# Process data input
tk.Label(process_frame, text="Processes (name,arrival,service):", bg="#ecf0f1", font=label_font, 
         fg="#34495e").grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=(10,5))
process_text = scrolledtext.ScrolledText(process_frame, width=35, height=15, font=("Courier New", 10),
                                        relief="groove", bd=2)
process_text.insert(tk.END, "A,0,3\nB,2,6\nC,4,4\nD,6,5\nE,8,2")
process_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Button section in process frame
button_frame = tk.Frame(process_frame, bg="#ecf0f1")
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

run_button = tk.Button(button_frame, text="🚀 Run Scheduler", command=run_scheduler, 
                      bg="#27ae60", fg="white", font=("Arial", 11, "bold"), 
                      relief="raised", bd=3, padx=20, pady=5,
                      activebackground="#2ecc71", cursor="hand2")
run_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="🗑️ Clear All", command=clear_all, 
                        bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), 
                        relief="raised", bd=3, padx=20, pady=5,
                        activebackground="#c0392b", cursor="hand2")
clear_button.pack(side=tk.LEFT, padx=5)

# Configure grid weights for process frame
process_frame.grid_columnconfigure(1, weight=1)
process_frame.grid_rowconfigure(2, weight=1)

# Status bar
status_var = tk.StringVar(value="Ready")
status_bar = tk.Label(root, textvariable=status_var, bg="#34495e", fg="white", 
                     font=("Arial", 9), relief="sunken", bd=1, anchor="w")
status_bar.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5)

# Create notebook for charts (Bottom section spanning all columns)
chart_notebook = ttk.Notebook(root)
chart_notebook.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

# Gantt chart tab
gantt_frame = tk.Frame(chart_notebook, bg="#ecf0f1")
chart_notebook.add(gantt_frame, text="📈 Gantt Chart")

canvas = tk.Canvas(gantt_frame, width=500, height=300, bg="#ffffff", 
                  relief="groove", bd=2, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Timeline graph tab
timeline_frame = tk.Frame(chart_notebook, bg="#ecf0f1")
chart_notebook.add(timeline_frame, text="⏱️ Timeline Graph")

# REVERSED SPACE ALLOCATION: Configure grid weights for responsive design
root.grid_columnconfigure(0, weight=4)  # Algorithm config (MORE space - 4x)  
root.grid_columnconfigure(1, weight=1)  # Output area (LESS space - 1x)
root.grid_columnconfigure(2, weight=4)  # Process config (MORE space - 4x)
root.grid_rowconfigure(1, weight=1)     # Main content area
root.grid_rowconfigure(2, weight=1)     # Charts area

# Add hover effects for buttons
def on_enter(e):
    e.widget.configure(relief="raised", bd=4)

def on_leave(e):
    e.widget.configure(relief="raised", bd=3)

run_button.bind("<Enter>", on_enter)
run_button.bind("<Leave>", on_leave)
clear_button.bind("<Enter>", on_enter)
clear_button.bind("<Leave>", on_leave)

# Center the window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

root.mainloop()