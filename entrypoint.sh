#   Edited by:
#   Ionut Ciobanu
#

#!/bin/sh
set -e

python manage.py migrate --noinput
exec "$@"
