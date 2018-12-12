import uuid
import time
import datetime
import csv
import json
from warnings import warn
from settings import SCHEDULE_INTERVAL, TRASH_CAN_INFORMATION_FILENAME, LOG_FILENAME, LOG_DIR
from fse2017_robot.drivers.ultrasonic_ranger import UltrasonicRanger


class LoggerDaemon:

    def __init__(self):
        self.log_dir = LOG_DIR
        self.log_filename = LOG_FILENAME
        self.trash_can_information_filename = TRASH_CAN_INFORMATION_FILENAME
        self.schedule_interval = SCHEDULE_INTERVAL

        # Retrieve depth and uuid of trash can
        with open(self.trash_can_information_filename) as data:
            d = json.load(data)
        self.depth = int(d['depth'])
        self.trash_can_uuid = d['uuid']


    def start_logging(self):
        """
        Perform logging.
        :return:
        """
        print("Started logger daemon for trash can " + self.trash_can_uuid)
        print("log is stored to " + self.log_dir + self.log_filename)

        # Schedule logging events
        print("Writing to log every " + str(self.schedule_interval) + " seconds.")
        while True:
            x = self.get_fill_state()
            self.write_to_log(x)
            time.sleep(self.schedule_interval)


    def get_fill_state(self):
        """
        Use Ultrasonic ranger to retrieve fill state.
        :return: Fill state in percent, between 0 and 1. 0 = empty, 1 = full.
        """
        distance = UltrasonicRanger().average_distance
        fill_state = float(self.depth - distance) / self.depth

        if fill_state < 0:
            return 0
        else:
            return fill_state


    def write_to_log(self, fill_state: float):
        """
        Write an entry  to the fill state log file of the trash can.
        :param fill_state:  Numerical representation of the trash bin fill state.
        :return:
        """
        with open(self.log_dir + self.log_filename, 'a') as file:
            wr = csv.writer(file, delimiter=';', lineterminator='\n')
            wr.writerow([str(uuid.uuid4()), str(datetime.datetime.utcnow()), str(self.trash_can_uuid), fill_state])


    def delete_from_log(self, uuid: str):
        """
        Delete an entry from the fill state log file of the trash can.
        :param uuid: 36 digit
        :return:
        """
        output_lines = []
        found_uuid = False

        log_file = open(self.log_dir + self.log_filename, 'r')
        for line in log_file:
            if str(uuid) in line:
                found_uuid = True
            else:
                output_lines.append(line)
        log_file.close()

        if found_uuid is False:
            warn("No log entry with given UUID found.")
        else:
            with open(self.log_dir + self.log_filename, 'w') as log_file:
                log_file.writelines(output_lines)
            print("Successfully deleted log entry with UUID " + uuid + ".")

