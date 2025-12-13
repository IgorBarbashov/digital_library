from enum import IntEnum


class BookReadingStatus(IntEnum):
    TO_READ = 0
    READING = 1
    FINISHED = 2
    ABANDONED = 3
