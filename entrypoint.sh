#!/bin/bash

if [ "$ROLE" == "head" ]; then
    ray start --head --include-dashboard=true --dashboard-host=0.0.0.0 --dashboard-port=8265
else
    ray start --address='ray-head:6379'  
fi

tail -f /dev/null