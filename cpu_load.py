import math
import time
import multiprocessing

def cpu_intensive_task():
    """
    A function that performs CPU-intensive calculations.
    """
    while True:
        # Perform a computationally intensive task (e.g., calculate square roots)
        for _ in range(10_000_000):
            math.sqrt(123456789)
        time.sleep(0.1)  # Small sleep to avoid 100% CPU usage on all cores

def main():
    """
    Main function to create multiple processes for CPU load.
    """
    print("Starting CPU load application...")
    print(f"Using {multiprocessing.cpu_count()} CPU cores.")

    # Create a process for each CPU core
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=cpu_intensive_task)
        process.start()
        processes.append(process)

    try:
        # Keep the main program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping CPU load application...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()
        print("Application stopped.")

if __name__ == "__main__":
    main()
