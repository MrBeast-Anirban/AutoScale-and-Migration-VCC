#!/bin/bash

# Variables
PROJECT_ID="vcc-assignment-3-454614"  
INSTANCE_NAME="gcp-vm-$(date +%s)"  # Unique instance name
ZONE="us-central1-a"
MACHINE_TYPE="e2-medium"
IMAGE_FAMILY="ubuntu-2004-lts"
IMAGE_PROJECT="ubuntu-os-cloud"
LOCAL_APP_DIR="app.py"
REMOTE_APP_DIR="gcloud compute scp --recurse ~/app m23csa005@$INSTANCE_NAME:~"  
TARGET_CPU_UTILIZATION=75  # Scale out when CPU > 75%

# Function to get current CPU utilization
get_cpu_utilization() {
  CPU_UTILIZATION=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
  echo $CPU_UTILIZATION
}

# Function to create a GCP VM instance
create_gcp_vm() {
  echo "Creating GCP VM instance: $INSTANCE_NAME..."
  gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --tags=http-server,https-server
}

# Function to migrate the application to the GCP VM
migrate_app() {
  echo "Migrating application to GCP VM..."
  gcloud compute scp --recurse $LOCAL_APP_DIR $INSTANCE_NAME:$REMOTE_APP_DIR \
    --project=$PROJECT_ID \
    --zone=$ZONE
  echo "Installing dependencies and starting the application..."
  gcloud compute ssh m23cse006@$VM_NAME --command="
        sudo apt update &&
        sudo apt install -y python3 python3-pip &&
        pip3 install flask &&
        cd ~/flask_app &&
        python3 app.py &"
}

# Main loop to monitor CPU utilization
while true; do
  CPU_UTILIZATION=$(get_cpu_utilization)
  echo "Current CPU Utilization: $CPU_UTILIZATION%"

  if (( $(echo "$CPU_UTILIZATION > $TARGET_CPU_UTILIZATION" | bc -l) )); then
    echo "CPU utilization is high. Scaling out..."
    create_gcp_vm
    migrate_app
    echo "Application migrated to GCP VM: $INSTANCE_NAME"
    break  # Exit the loop after migration
  else
    echo "CPU utilization is normal. No action required."
  fi

  # Wait for 10 seconds before checking again
  sleep 10
done
