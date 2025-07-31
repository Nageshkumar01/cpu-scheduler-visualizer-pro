# 🖥️ CPU Scheduler Visualizer Pro

A comprehensive Python GUI application for visualizing and analyzing various CPU scheduling algorithms. This tool provides an intuitive interface to simulate, trace, and visualize the execution of different scheduling policies with real-time Gantt charts and timeline graphs.

## 📋 Table of Contents
- [Features](#-features)
- [Supported Algorithms](#-supported-algorithms)
- [Installation](#-installation)
- [Usage](#-usage)
- [Input Format](#-input-format)
- [GUI Components](#-gui-components)
- [Dependencies](#-dependencies)
- [Screenshots](#-screenshots)
- [Algorithm Details](#-algorithm-details)
- [Contributing](#-contributing)

## ✨ Features

- **Interactive GUI**: Modern, user-friendly interface built with tkinter
- **Real-time Visualization**: Dynamic Gantt charts and timeline graphs
- **Multiple Algorithms**: Support for 8+ CPU scheduling algorithms
- **Input Validation**: Comprehensive error checking and validation
- **Export Capabilities**: Matplotlib-based charts for analysis
- **Process Management**: Easy add/remove processes with visual feedback
- **Responsive Design**: Adaptive layout that scales with window size
- **Color-coded Visualization**: Unique colors for each process in charts
- **Status Tracking**: Real-time status updates and progress indication

## 🔧 Supported Algorithms

| Algorithm | Code | Description |
|-----------|------|-------------|
| **FCFS** | 1 | First Come First Serve - Non-preemptive scheduling |
| **Round Robin** | 2-q | Time-sliced scheduling with quantum q |
| **SPN** | 3 | Shortest Process Next - Non-preemptive |
| **SRT** | 4 | Shortest Remaining Time - Preemptive SPN |
| **HRRN** | 5 | Highest Response Ratio Next |
| **Feedback (FB-1)** | 6 | Feedback scheduling with fixed quantum = 1 |
| **Feedback (FB-2i)** | 7 | Feedback with increasing quantum 2^i |
| **Aging** | 8-q | Priority aging with quantum q |

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- C++ compiler (g++)
- Make utility

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/nageshkumar01/cpu-scheduler-visualizer-pro.git
   cd cpu-scheduler-visualizer-pro
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the scheduler backend**
   ```bash
   make
   ```

4. **Run the application**
   ```bash
   python scheduler_gui.py
   ```

### Dependencies
```
tkinter>=8.6
matplotlib>=3.5.0
numpy>=1.21.0
```

## 🎯 Usage

### Quick Start
1. Launch the application
2. Select a scheduling algorithm from the dropdown
3. Configure total simulation time
4. Add or modify processes in the process configuration area
5. Click "🚀 Run Scheduler" to execute
6. View results in the output area and charts

### Process Input Format
Each process should be entered as: `name,arrival_time,service_time`

Example:
```
A,0,3
B,2,6
C,4,4
D,6,5
E,8,2
```

**Special Case - Aging Algorithm:**
For the Aging algorithm, use: `name,arrival_time,priority`

## 🎨 GUI Components

### Main Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    🖥️ CPU Scheduler Visualizer Pro          │
├──────────────────┬─────────────────┬──────────────────────────┤
│   ⚙️ Algorithm    │  📊 Scheduler   │    📝 Process           │
│   Configuration  │    Output       │   Configuration         │
│                  │                 │                         │
│  • Algorithm     │  • Execution    │  • Process Count        │
│    Selection     │    Trace        │  • Process List         │
│  • Parameters    │  • Statistics   │  • Add/Remove           │
│  • Time Config   │  • Error Info   │  • Run/Clear            │
└──────────────────┴─────────────────┴──────────────────────────┤
│                     📈 Visualization Charts                   │
│  ┌─────────────────┐  ┌─────────────────────────────────────┐ │
│  │  Gantt Chart    │  │      Timeline Graph                │ │
│  └─────────────────┘  └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

## 🔍 Sample Screenshots


### 🖼️ Screenshot 1
![Gantt Chart 1](https://raw.githubusercontent.com/Nageshkumar01/cpu-scheduler-visualizer-pro/main/Screenshot%20(1533).png)

### 🖼️ Screenshot 2
![Gantt Chart 2](https://raw.githubusercontent.com/Nageshkumar01/cpu-scheduler-visualizer-pro/main/Screenshot%20(1534).png)

### 🖼️ Screenshot 3
![Gantt Chart 3](https://raw.githubusercontent.com/Nageshkumar01/cpu-scheduler-visualizer-pro/main/image.png.png)


```


### Features Breakdown

- **Algorithm Configuration Panel**: Select algorithms, set parameters
- **Process Management**: Add, remove, and edit processes
- **Real-time Output**: View scheduler execution trace
- **Interactive Charts**: Gantt chart and timeline visualization
- **Status Bar**: Real-time feedback and error reporting

## 📝 Input Format Details

### Standard Format (Algorithms 1-7)
```
trace                    # Operation mode
3                       # Algorithm number
20                      # Total simulation time
5                       # Number of processes
A,0,3                   # Process: name,arrival,service
B,2,6
C,4,4
D,6,5
E,8,2
```

### Aging Algorithm Format (Algorithm 8)
```
trace                    # Operation mode
8-1                     # Aging with quantum 1
20                      # Total simulation time
3                       # Number of processes
A,0,5                   # Process: name,arrival,priority
B,2,3
C,4,1
```

## 🔍 Algorithm Details

### First Come First Serve (FCFS)
- **Type**: Non-preemptive
- **Selection**: Process arrival order
- **Best for**: Batch processing systems
- **Drawback**: Poor response time for short processes

### Round Robin (RR)
- **Type**: Preemptive
- **Selection**: Time quantum rotation
- **Parameter**: Time quantum (q)
- **Best for**: Interactive systems
- **Advantage**: Fair CPU allocation

### Shortest Process Next (SPN)
- **Type**: Non-preemptive
- **Selection**: Shortest burst time
- **Best for**: Minimizing average waiting time
- **Drawback**: Requires advance knowledge of burst times

### Shortest Remaining Time (SRT)
- **Type**: Preemptive
- **Selection**: Shortest remaining time
- **Best for**: Minimizing average turnaround time
- **Advantage**: Optimal for shortest average waiting time

### Highest Response Ratio Next (HRRN)
- **Type**: Non-preemptive
- **Selection**: Highest response ratio
- **Formula**: Response Ratio = (Wait Time + Service Time) / Service Time
- **Advantage**: Balances short processes and waiting time

### Feedback Scheduling (FB)
- **Type**: Preemptive, Multi-level
- **Selection**: Priority queues with aging
- **Variants**: 
  - FB-1: Fixed quantum = 1
  - FB-2i: Quantum = 2^i for level i
- **Advantage**: Adaptive to process behavior

### Aging
- **Type**: Preemptive with priority aging
- **Selection**: Dynamic priority adjustment
- **Mechanism**: Priorities increase over time to prevent starvation
- **Parameter**: Time quantum (q)

## 🎨 Visualization Features

### Gantt Chart
- **Color-coded processes**: Each process gets a unique color
- **Time axis**: Shows execution timeline
- **Process blocks**: Visual representation of CPU allocation
- **Interactive**: Hover effects and detailed information

### Timeline Graph
- **Matplotlib integration**: High-quality, exportable charts
- **Process scheduling**: Visual timeline of process execution
- **Grid overlay**: Easy time reference
- **Professional styling**: Publication-ready graphics

## 🛠️ Advanced Features

### Input Validation
- **Range checking**: Ensures positive values
- **Format validation**: Correct process format
- **Count verification**: Process count consistency
- **Error reporting**: Detailed error messages

### Process Management
- **Dynamic addition**: Add processes with '+' button
- **Safe removal**: Remove processes with '-' button
- **Bulk operations**: Clear all with confirmation
- **Auto-numbering**: Automatic process naming

### Visual Feedback
- **Button animations**: Hover effects and click feedback
- **Status updates**: Real-time operation status
- **Color transitions**: Smooth UI state changes
- **Progress indication**: Visual operation progress

## 🔧 Configuration Options

### Window Settings
- **Resizable interface**: Adaptive to screen size
- **Minimum dimensions**: 1400x900 pixels
- **Responsive layout**: Grid-based responsive design
- **Professional styling**: Modern color scheme and fonts

### Chart Customization
- **Color mapping**: Consistent process colors
- **Font settings**: Readable typography
- **Grid options**: Configurable grid display
- **Export formats**: Multiple output formats via matplotlib

## 🐛 Troubleshooting

### Common Issues

1. **"main.exe not found"**
   - Ensure the C++ backend is compiled: `make`
   - Check file permissions

2. **GUI not responding**
   - Check Python version (3.7+)
   - Verify tkinter installation

3. **Charts not displaying**
   - Install matplotlib: `pip install matplotlib`
   - Check backend compatibility

4. **Process input errors**
   - Verify comma-separated format
   - Ensure positive numbers for times
   - Check process count matches entries

### Performance Tips
- **Process limit**: Recommended maximum 50 processes
- **Time range**: Keep simulation time reasonable (<100 units)
- **Memory usage**: Clear charts between runs for large datasets

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/Nageshkumar01/cpu-scheduler-visualizer-pro.git
cd cpu-scheduler-visualizer-pro
pip install -r requirements-dev.txt
make test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original CPU scheduling algorithms implementation
- Python tkinter community for GUI best practices
- Matplotlib developers for excellent charting capabilities
- Contributors and testers

## 📞 Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/Nageshkumar01/cpu-scheduler-visualizer-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nageshkumar01/cpu-scheduler-visualizer-pro/discussions)
- **Email**: nageshsmp11@gmail.com

---

**Made with ❤️ for students and educators studying operating systems and CPU scheduling algorithms.**
