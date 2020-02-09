#!/usr/bin/env bash

set -ex

sleep 3
pg_isready --host=127.0.0.1 --timeout=30 --port=$1