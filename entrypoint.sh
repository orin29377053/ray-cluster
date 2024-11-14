#!/bin/bash
ray start --head --include-dashboard=true --dashboard-host=0.0.0.0 --dashboard-port=8265
tail -f /dev/null
