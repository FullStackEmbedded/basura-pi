#!/bin/bash

FILL_STATE_LOG=log/fill-state-log.csv
REPORTED_LOG=log/reported-log.csv
BASURA_SERVER=basura-server:8000
FREQUENCY=60  # Seconds to wait before repeating report cycle

while true; do
  # Make sure Trash Can is registered with server
  echo Reporting Trash Cans to Server...
  for uuid in $(tail -n +2 $FILL_STATE_LOG | cut -d ';' -f 3 | sort -u); do
    http POST $BASURA_SERVER/trashcans/ id=$uuid
  done

  # Report all lines from Fill State Log
  # By the way, this is *not* the right way to parse text, but we hacked it this
  # way to save time
  i=0
  echo Reporting Trash Events to Server...
  while read line; do
    success=0
    if [[ $i -gt 0 ]]; then  # Skip log header
      # Serialize each line as JSON
      echo $line | \
        sed -e 's/;/", "timestamp": "/' | \
        # This hack makes sure that we can set BASURA_SERVER to point at any address
        sed -e 's/;/", "trash_can": "http:\/\/TRASH_CAN_ROOT\/trashcans\//' | \
        sed "s/TRASH_CAN_ROOT/$BASURA_SERVER/" |\
        # We need an extra slash here to access the right address
        sed -e 's/;/\/", "fill_state": /' | \
        sed -e 's/^/{"uuid": "/' | \
        sed -e 's/$/}/' | \
        http --check-status POST $BASURA_SERVER/trashstates/ && success=1
      if [[ $success -eq 1 ]]; then
        echo $line | cut -d \; -f 1 >> $REPORTED_LOG
      else
        echo FAIL: Could not register fill state with server.
      fi
    fi
    i=$((i+1))
  done < $FILL_STATE_LOG

  # Delete Fill States which have been removed from Fill State Log from the
  # Reported Log
  echo Cleaning reported log...
  for uuid in $(tail -n +2 $REPORTED_LOG); do
    delete=0
    grep $uuid $FILL_STATE_LOG && \
      echo Trash fill state still must be deleted from Fill State Log || \
      delete=1
    if [[ $delete -eq 1 ]]; then
      echo Trash fill state $uuid will be deleted from Fill State Log.
      grep -v $uuid $REPORTED_LOG > $REPORTED_LOG~ && mv $REPORTED_LOG~ $REPORTED_LOG
    fi
  done
  sleep $FREQUENCY
done
