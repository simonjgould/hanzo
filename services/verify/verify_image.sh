#!/usr/bin/env bash

set -ex

echo "verifying image tests"

sleep 10

post_response=$(curl \
  --fail \
  --header "Content-Type: application/json" \
  --request POST \
  --data @test_body.json \
  "http://127.0.0.1:$1/polls/questions/")
echo ${post_response}

get_response=$(curl \
  --fail \
  --header "Content-Type: application/json" \
  --request GET \
  "http://127.0.0.1:$1/polls/questions/")
echo ${get_response}

if [[ "[${post_response}]" != "${get_response}" ]]; then
    echo "failed to verify service behavior"
    exit 1
fi

