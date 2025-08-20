# Web Server Benchmarking Tool

This project is a **benchmarking tool** developed in Python to evaluate the **throughput (rata de ieșire)** and **response time (timp de răspuns)** of a web server under different load conditions.  
It provides detailed insights into server performance, helping identify bottlenecks and areas for optimization.

---

## 📌 Features
- Measure **response time** and **throughput** for HTTP requests.  
- Multiple **test scenarios**:
  - Constant Load Test
  - Ramp-Up Test
  - Spike Test
  - Stress Test
- **Asynchronous request handling** with `asyncio` for high concurrency.  
- **Data collection & visualization**:
  - Saves results in CSV format.
  - Generates histograms, percentiles, throughput, and error rate plots.  
- **Graphical User Interface (GUI)** using `PyQt5` for easy configuration and visualization.  
- Flexible configuration via **config.json** or command-line arguments.

---

## 🛠️ Technologies & Libraries
- **Python 3.8+**
- [`requests`](https://docs.python-requests.org/) – HTTP requests  
- [`asyncio`](https://docs.python.org/3/library/asyncio.html) – asynchronous requests  
- [`matplotlib`](https://matplotlib.org/) – data visualization  
- [`numpy`](https://numpy.org/) – numerical computations  
- [`pandas`](https://pandas.pydata.org/) – data analysis  
- [`statistics`](https://docs.python.org/3/library/statistics.html) – statistical calculations  
- [`argparse`](https://docs.python.org/3/library/argparse.html) – CLI argument parsing  
- [`PyQt5`](https://riverbankcomputing.com/software/pyqt/) – graphical interface  
- [`json`](https://docs.python.org/3/library/json.html) – configuration management  

---

## 📂 Project Structure
├── main.py # Entry point – runs the benchmark


├── benchmark.py # Core logic for sending requests


├── config_handler.py # Load/save configurations


├── test_scenarios.py # Load, ramp-up, spike, and stress tests


├── data_plotting.py # Data analysis & plotting


├── config.json # Configuration file


├── response_data.csv # Output with server responses


└── data_analysis.ipynb # Jupyter notebook with data visualization


---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the tool
```bash
python main.py --url https://example.com --num_requests 100
```

## or use the GUI
```bash
python main.py
```

The GUI allows you to:

- Enter the server URL
- Choose number of requests
- Select test type (constant, ramp-up, spike, stress)
- Visualize results interactively
