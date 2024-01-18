#!/bin/bash

source /app/www/vhosts/cosmenet.in.th/httpdocs-scanner-extract-feature/venv/bin/activate

pm2 del service-python-feature-extractor

pm2 start

