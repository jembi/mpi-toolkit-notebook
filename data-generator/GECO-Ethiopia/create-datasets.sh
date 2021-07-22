#!/bin/bash

set -e
set -u

create-dataset() {
  ORDERED_FILE=$(printf "data-%05d-%05d-abcd" "$1" "$2")
  SHUFFLED_FILE=$(printf "data-%05d-%05d-dcab" "$1" "$2")
  python generate-data.py "$1" "$2" "${ORDERED_FILE}"
  sed 1,1d "$ORDERED_FILE".csv | shuf >"$SHUFFLED_FILE".csv
  HEADER=$(head -1 "${ORDERED_FILE}".csv)
  sed -i '1i '"${HEADER}" "${SHUFFLED_FILE}".csv
}

python --version

rm -f ./*.csv

create-dataset 100 50
create-dataset 200 100
create-dataset 1000 500
create-dataset 2000 1000
create-dataset 5000 2500
create-dataset 10000 5000
create-dataset 13333 6667
create-dataset 20000 10000
create-dataset 30000 15000
