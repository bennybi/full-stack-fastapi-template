#! /usr/bin/env bash

set -e
set -x

# 测试数据库， Let the DB start
python app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py
