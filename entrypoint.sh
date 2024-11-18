#!/bin/bash

# download the dataset
python download_dataset.py

# run ray
if [ "$ROLE" == "head" ]; then
    # Start Ray head node with Prometheus metrics enabled
    ray start --head \
        --include-dashboard=true \
        --dashboard-host=0.0.0.0 \
        --dashboard-port=8265 \
        --metrics-export-port=8080 \
        --metrics-export-interval-ms=10000
else
    # Start Ray worker node with Prometheus metrics enabled
    ray start \
        --address='ray-head:6379' \
        --metrics-export-port=8080 \
        --metrics-export-interval-ms=10000
fi

# Start a basic Python HTTP server to expose metrics endpoint if needed
if [ "$PROMETHEUS_METRICS" == "true" ]; then
    python -m http.server 8080 &
fi

# Keep container running
tail -f /dev/null