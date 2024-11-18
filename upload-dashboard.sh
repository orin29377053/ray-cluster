#!/bin/bash

GRAFANA_HOST="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASSWORD="admin"
AUTH_HEADER="Authorization: Basic $(echo -n ${GRAFANA_USER}:${GRAFANA_PASSWORD} | base64)"

curl -X POST \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  "${GRAFANA_HOST}/api/dashboards/db" \
  -d @dashboards/default_grafana_dashboard.json

curl -X POST \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  "${GRAFANA_HOST}/api/dashboards/db" \
  -d @dashboards/data_grafana_dashboard.json

curl -X POST \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  "${GRAFANA_HOST}/api/dashboards/db" \
  -d @dashboards/serve_grafana_dashboard.json

curl -X POST \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  "${GRAFANA_HOST}/api/dashboards/db" \
  -d @dashboards/serve_deployment_grafana_dashboard.json