from enum import IntEnum


class GameEnum(IntEnum):
    NAME = 0,
    DESCRIPTION = 1,
    DEVELOPER = 2,
    RAM_MIN = 3,
    CPU_MIN = 4,
    GPU_MIN = 5,
    OS_MIN = 6,
    STORAGE_MIN = 7,
    RAM_REC = 8,
    CPU_REC = 9,
    GPU_REC = 10,
    OS_REC = 11,
    STORAGE_REC = 12

    # defines ranges for each section in the response tuple of a query
    @classmethod
    def response_slice(cls, section):
        section_indexes = {
            'info': slice(cls.NAME, cls.DEVELOPER+1),
            'minimum_requirements': slice(cls.RAM_MIN, cls.STORAGE_MIN+1),
            'recommended_requirements': slice(cls.RAM_REC, cls.STORAGE_REC+1)
        }

        return section_indexes[section]

