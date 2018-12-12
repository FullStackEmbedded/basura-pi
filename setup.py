import os.path
import uuid
import json
import csv
from settings import LOG_FILENAME, LOG_DIR, TRASH_CAN_INFORMATION_FILENAME
from fse2017_robot.drivers.ultrasonic_ranger import UltrasonicRanger


# Create a new log file, if not exists
if not os.path.isfile(LOG_DIR + LOG_FILENAME):
    os.makedirs(LOG_DIR)
    with open(LOG_DIR + LOG_FILENAME, 'w') as file:
        wr = csv.writer(file,  delimiter=';', lineterminator='\n')
        wr.writerow(["uuid", "time", "trash_can_uuid", "fill_state"])

# Create UUID for trash can
trash_can_uuid = uuid.uuid4()

# Calibrate logger for a trash can interactively.
print("Starting interactive calibration of your logger.")
print("Please empty trash can completely. Mount the ultrasonic ranger at the top, facing down.")
input("Press Enter when you are done.")

# Read trash can depth
depth = UltrasonicRanger().average_distance

if depth is not None:
    print("Measured depth: " + str(depth) + " cm.")
    print("Calibration completed.")

# Write to json file
with open(TRASH_CAN_INFORMATION_FILENAME, 'w') as writer:
    writer.write(json.dumps({"uuid": str(trash_can_uuid), "depth": depth}))
    writer.close()

print("UUID and depth were stored in " + TRASH_CAN_INFORMATION_FILENAME)

