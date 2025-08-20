import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data(filepath):
    """Load data from a CSV file into a DataFrame."""
    df = pd.read_csv(filepath)
    return df


def plot_response_time_distribution(fig, df):
    """Plot histogram of response time on a given figure."""
    fig.clf()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.hist(df['response_time'], bins=30, color='skyblue', edgecolor='black')
    ax.set_title('Response Time Distribution')
    ax.set_xlabel('Response Time (seconds)')
    ax.set_ylabel('Frequency')
    ax.grid(True)
    fig.canvas.draw()

def plot_response_time_percentiles(fig, df):
    """Plot response time percentiles without datetime conversion."""
    # Assuming 'timestamp' is already in datetime format, if not, convert it:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    percentiles = df.groupby(pd.Grouper(key='timestamp', freq='s'))['response_time'].quantile([0.5, 0.95, 0.99]).unstack()
    fig.clf()
    ax = fig.add_subplot(111)
    ax.clear()
    for percentile in percentiles.columns:
        ax.plot(percentiles.index, percentiles[percentile], label=f'{percentile*100}% Percentile')
    ax.set_title('Response Time Percentiles')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Response Time (seconds)')
    ax.legend()
    ax.grid(True)
    fig.canvas.draw()

def plot_throughput(fig, df):
    """Plot throughput without datetime conversion."""
    # Calculate throughput over smaller time intervals (requests per second)
    throughput = df.groupby(pd.Grouper(key='timestamp', freq='s')).size()

    #throughput = df.groupby('timestamp').size()
    fig.clf()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.plot(throughput.index, throughput.values, marker='o', color='orange')
    ax.set_title('Throughput Over Time')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Throughput (requests per interval)')
    ax.grid(True)
    fig.canvas.draw()

def plot_error_rate(fig, df):
    """Plot error rate without datetime conversion."""
    error_counts = df[df['status_code'] >= 400].groupby('timestamp').size()
    total_counts = df.groupby('timestamp').size()
    error_rate = error_counts / total_counts
    fig.clf()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.plot(error_rate.index, error_rate.fillna(0) * 100, marker='o', color='red')
    ax.set_title('Error Rate Over Time')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Error Rate (%)')
    ax.grid(True)
    fig.canvas.draw()

def calculate_metrics(df):
    """Calculate and return key performance metrics, ensuring datetime operations."""
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    metrics = {}
    if not pd.isnull(df['timestamp']).any():  # Ensure no NaT values which indicate conversion issues
        total_seconds = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
        if total_seconds > 0:  # Prevent division by zero
            metrics['Throughput'] = len(df) / total_seconds
        else:
            metrics['Throughput'] = 0
    else:
        metrics['Throughput'] = 0

    metrics['Average Response Time'] = df['response_time'].mean()
    metrics['Median Response Time'] = df['response_time'].median()
    metrics['95th Percentile Response Time'] = df['response_time'].quantile(0.95)
    metrics['Maximum Response Time'] = df['response_time'].max()
    metrics['Error Rate'] = df[df['status_code'] >= 400].shape[0] / df.shape[0] * 100 if df.shape[0] > 0 else 0

    return metrics


def display_metrics(fig, df):
        metrics = calculate_metrics(df)

        """Display computed metrics in the GUI's text area."""
        text_results = (
            f"Throughput: {metrics['Throughput']:.2f} requests/second\n"
            f"Average Response Time: {metrics['Average Response Time']:.2f} ms\n"
            f"Median Response Time: {metrics['Median Response Time']:.2f} ms\n"
            f"95th Percentile Response Time: {metrics['95th Percentile Response Time']:.2f} ms\n"
            f"Maximum Response Time: {metrics['Maximum Response Time']:.2f} ms\n"
            f"Error Rate: {metrics['Error Rate']:.2f}%"
        )
        fig.setText(text_results)