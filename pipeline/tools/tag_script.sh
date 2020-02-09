#!/usr/bin/env bash

set -ex

git_username=$1
git_password=$2

git config --local credential.helper "!f() { echo username=\\$git_username; echo password=\\$git_password; }; f"
git push --tags