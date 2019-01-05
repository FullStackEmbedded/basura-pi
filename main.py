#!/usr/bin/python3

from logger_daemon import LoggerDaemon

if __name__ == '__main__':
    logger = LoggerDaemon()
    logger.start_logging()

