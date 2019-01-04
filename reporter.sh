#!/bin/bash

# Read all lines from Fill State Log
i=0
while read line; do
  if [[ $i -gt 0 ]]; then  # Skip log header
    # Serialize each line as JSON
    echo $line | \
      sed -e 's/;/", "time": "/' | \
      sed -e 's/;/", "trash_can_uuid": "/' | \
      sed -e 's/;/", "fill_state": /' | \
      sed -e 's/^/{"uuid": "/' | \
      sed -e 's/$/}/'
  fi
  i=$((i+1))
done < log/fill-state-log.csv
