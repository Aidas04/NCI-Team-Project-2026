#!/bin/sh
set -e

#   Edited by:
#   Ionut Ciobanu
#

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
