#!/usr/bin/env bash

# fail fast
set -e

WIREMOCK_IMAGE="wiremock/wiremock:3.10.0-1@sha256:052f7d05b585d5cc956ecf2f1543b1a721858ec83baf0d11b507a113e3b023ee"
CONTAINER_NAME="probro_wiremock"
WIREMOCK_PORT="8080"
EXPOSED_PORT="8181"
HOST="127.0.0.1"

MOCK_URL="http://${HOST}:${EXPOSED_PORT}"

WIREMOCK_CONFIG_ROOT="$(dirname "$0")/mocks/wiremock/config"

function create_mock {
  echo -e "[i] Pull image $WIREMOCK_IMAGE"
  podman pull "$WIREMOCK_IMAGE"

  echo -e "[i] Fire up container"
  podman run --restart unless-stopped \
    --tty=false \
    --name $CONTAINER_NAME \
    -p ${EXPOSED_PORT}:${WIREMOCK_PORT} \
    -e WIREMOCK_OPTIONS="--enable-stub-cors --max-request-journal-entries 1000 $WIREMOCK_VERBOSE" \
    --detach \
    "$WIREMOCK_IMAGE"

  PODMAN_RUN=$?
  if [ $PODMAN_RUN -ne 0 ]; then
    echo -e "[!] Failed to run container (error code: $PODMAN_RUN)"
    exit 1
  fi
}

function remove_mock {
  if podman ps -a | grep ${CONTAINER_NAME}; then
    echo -e "[i] Remove existing container"
    podman stop ${CONTAINER_NAME} &>/dev/null
    podman rm ${CONTAINER_NAME} &>/dev/null
  fi
}

function wait_for_mock {
  while :; do
    if curl -v --max-time 1 http://${HOST}:${EXPOSED_PORT}/foo &>/dev/null; then
      break
    fi
    sleep 1
  done
}

function flush_mock {
  echo "[i] Flush mock config and settings"
  curl -s -X DELETE "${MOCK_URL}"/__admin/mappings &>/dev/null
  curl -s -X DELETE "${MOCK_URL}"/__admin/settings &>/dev/null
}

function configure_mock {
  echo "[i] Configure mock mappings"
  find "$WIREMOCK_CONFIG_ROOT"/mappings -name "*.json" \
    -exec curl -s -X POST -H "Content-Type: application/json; charset=utf-8" "${MOCK_URL}"/__admin/mappings -d "@{}" \; &>/dev/null

  echo "[i] Configure mock settings"
  curl -s -X POST "${MOCK_URL}"/__admin/settings -d @"$WIREMOCK_CONFIG_ROOT"/settings.json &>/dev/null
}

function verify_mock_configuration {
  APPLIED_MAPPING_COUNT=$(curl -s "${MOCK_URL}"/__admin/mappings | jq -r ".mappings | length")
  MAPPING_FILE_COUNT=$(find "$WIREMOCK_CONFIG_ROOT"/mappings -name "*.json" | wc -l)
  if [ "$APPLIED_MAPPING_COUNT" -ne "$MAPPING_FILE_COUNT" ]; then
    echo -e "[!] Not all wiremock mappings applied. Files: $MAPPING_FILE_COUNT, Applied: $APPLIED_MAPPING_COUNT"
    exit 1
  fi
  echo -e "[i] Number of verified wiremock mappings: $APPLIED_MAPPING_COUNT"
}

echo -e "[i] Start $CONTAINER_NAME setup"

remove_mock
create_mock
wait_for_mock

flush_mock
configure_mock
verify_mock_configuration

echo -e "[i] Done"
