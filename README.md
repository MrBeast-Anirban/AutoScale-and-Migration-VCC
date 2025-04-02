# AutoScale-and-Migration-VCC
Implement resource monitoring using Prometheus and Configure auto-scaling and migration policies from Local Virtual Machine to Google Cloud Platform (GCP) to scale resources from Local VM to GCP when CPU utilization in Local Virtual Machine exceeds 75%.

![Alt text](vcc_assign3.png)


### About the Files in Repository :

- **cpu_load.py :** It is a stress program that increased load on CPU.
- **prometheus_metrics.py :** It is a monitor that keeps log of cpu utilization and memory utilization in Virtual Machine using Prometheus.
- **app.py :** A Flask application.
- **autoscale_cpu.sh :** It is a monitoring, scaline and migration script that monitors cpu utilization and scales to gcp when cpu utilization >75% and migrates application (flask) from local Virtual Machine to a GCP VM Instance.

  
### Prometheus is used to monitor CPU and memory utilization on the local VM.

#### Install Prometheus:
- Download and install Prometheus on the local VM.
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
tar -xvzf prometheus-2.30.3.linux-arm64.tar.gz
cd prometheus-2.30.3.linux-arm64
```


#### Install Node Exporter:
- Install Node Exporter to collect system metrics (CPU, memory, disk usage).
```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
tar -xvzf node_exporter-1.3.1.linux-arm64.tar.gz
cd node_exporter-1.3.1.linux-arm64
```


#### Configure Prometheus:

- Configure Prometheus to scrape metrics from Node Exporter.
- Edit prometheus.yml to scrape metrics from Node Exporter: scrape_configs:
```yml
job_name: 'node'
  static_configs:
    targets: ['localhost:9100']
```

A python script that queries CPU utilisation and memory Utilization on Virtual Machine and logs it. Above is the log that shows Increase in CPU utilisation when CPU_Load Program is running and drop in CPU Utilization when the CPU_Load Program is stopped.



### Autoscaling Policy and Migration Configuration 
We will use Google Cloud Platform (GCP) for auto-scaling.
Steps:
- Create a GCP Account:
- Sign up at https://cloud.google.com/.
- Set Up a GCP Project:
  - Create a new project in the GCP Console.
- Install Google Cloud SDK on the local VM:
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk 
```
Authenticate and configure the SDK:
```bash
gcloud init
```


### Simulation Peocess
```sh
./prometheus —config.file=prometheus.yml      ( // Make sure you are in _prometheus-2.30.3.linux-arm64_ directory then run the command.)
./node_exporter      ( // Make sure you are in _node_exporter-1.3.1.linux-arm64_ diectory then run the node_exporter script.)
python3 prometheus_metrics.py    
python3 app.py
python3 cpu_load.py
chmod +x autoscale_cpu.sh
./autoscale_cpu.sh
```
