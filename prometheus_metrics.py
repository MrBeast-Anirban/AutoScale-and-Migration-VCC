import requests
import time

# Prometheus server URL
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def query_prometheus(query):
    """
    Query Prometheus using the HTTP API.
    """
    response = requests.get(PROMETHEUS_URL, params={"query": query})
    response.raise_for_status()
    return response.json()

def get_cpu_utilization():
    """
    Get CPU utilization in percentage.
    """
    query = 'rate(node_cpu_seconds_total{mode="user"}[1m]) * 100'
    result = query_prometheus(query)
    if result["data"]["result"]:
        return float(result["data"]["result"][0]["value"][1])
    else:
        return None

def get_memory_utilization():
    """
    Get memory utilization in percentage.
    """
    query = '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100'
    result = query_prometheus(query)
    if result["data"]["result"]:
        return float(result["data"]["result"][0]["value"][1])
    else:
        return None

def main():
    """
    Main function to fetch and print CPU and memory utilization.
    """
    try:
        while True:
            cpu_util = get_cpu_utilization()
            memory_util = get_memory_utilization()

            if cpu_util is not None and memory_util is not None:
                print(f"CPU Utilization: {cpu_util:.2f}%")
                print(f"Memory Utilization: {memory_util:.2f}%")
            else:
                print("Error: Unable to fetch metrics from Prometheus.")

            # Wait for 5 seconds before the next iteration
            time.sleep(5)

    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
