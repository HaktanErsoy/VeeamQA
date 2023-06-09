import os
import shutil
import time
import sys


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        with open(self.log_file, "a") as log:
            log.write(f"{message}\n")

    def log_operation(self, operation, path):
        message = f"{operation}: {path}"
        self.log(message)
        print(message)


def do_sync(source_folder, copy_folder, sync_interval, log_file):
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(copy_folder, exist_ok=True)

    logger = Logger(log_file)

    while True:
        source_set = set(os.listdir(source_folder))
        copy_set = set(os.listdir(copy_folder))

        added_items = source_set - copy_set
        for file in added_items:
            src = os.path.join(source_folder, file)
            dst = os.path.join(copy_folder, file)
            shutil.copyfile(src, dst)
            operation = "Created" if len(source_set) > len(copy_set) else "Copied"
            logger.log_operation(operation, f"{src} -> {dst}")

        deleted_items = copy_set - source_set
        for file in deleted_items:
            path = os.path.join(copy_folder, file)
            os.remove(path)
            logger.log_operation("Removed", path)

        time.sleep(int(sync_interval))


def do_sync_once(source_folder, copy_folder, sync_interval, log_file):
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(copy_folder, exist_ok=True)

    logger = Logger(log_file)

    source_set = set(os.listdir(source_folder))
    copy_set = set(os.listdir(copy_folder))

    added_items = source_set - copy_set
    for file in added_items:
        src = os.path.join(source_folder, file)
        dst = os.path.join(copy_folder, file)
        shutil.copyfile(src, dst)
        operation = "Created" if len(source_set) > len(copy_set) else "Copied"
        logger.log_operation(operation, f"{src} -> {dst}")

    deleted_items = copy_set - source_set
    for file in deleted_items:
        path = os.path.join(copy_folder, file)
        os.remove(path)
        logger.log_operation("Removed", path)

    time.sleep(int(sync_interval))


if __name__ == "__main__":
    source_folder = sys.argv[1]
    copy_folder = sys.argv[2]
    sync_interval = sys.argv[3]
    log_file = sys.argv[4]

    do_sync(source_folder, copy_folder, sync_interval, log_file)
