#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e


# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Step 3: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput


echo "Build process completed successfully!"