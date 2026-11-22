"""
Module for the Tinkerforge RED Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/RED_Brick_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import check_length, check_range
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """

    ASYNC_FILE_READ = 30
    ASYNC_FILE_WRITE = 31
    FILE_EVENTS_OCCURRED = 32
    PROCESS_STATE_CHANGED = 45
    PROGRAM_SCHEDULER_STATE_CHANGED = 65
    PROGRAM_PROCESS_SPAWNED = 66


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    CREATE_SESSION = 1
    EXPIRE_SESSION = 2
    EXPIRE_SESSION_UNCHECKED = 3
    KEEP_SESSION_ALIVE = 4
    RELEASE_OBJECT = 5
    RELEASE_OBJECT_UNCHECKED = 6
    ALLOCATE_STRING = 7
    TRUNCATE_STRING = 8
    GET_STRING_LENGTH = 9
    SET_STRING_CHUNK = 10
    GET_STRING_CHUNK = 11
    ALLOCATE_LIST = 12
    GET_LIST_LENGTH = 13
    GET_LIST_ITEM = 14
    APPEND_TO_LIST = 15
    REMOVE_FROM_LIST = 16
    OPEN_FILE = 17
    CREATE_PIPE = 18
    GET_FILE_INFO = 19
    READ_FILE = 20
    READ_FILE_ASYNC = 21
    ABORT_ASYNC_FILE_READ = 22
    WRITE_FILE = 23
    WRITE_FILE_UNCHECKED = 24
    WRITE_FILE_ASYNC = 25
    SET_FILE_POSITION = 26
    GET_FILE_POSITION = 27
    SET_FILE_EVENTS = 28
    GET_FILE_EVENTS = 29
    OPEN_DIRECTORY = 33
    GET_DIRECTORY_NAME = 34
    GET_NEXT_DIRECTORY_ENTRY = 35
    REWIND_DIRECTORY = 36
    CREATE_DIRECTORY = 37
    GET_PROCESSES = 38
    SPAWN_PROCESS = 39
    KILL_PROCESS = 40
    GET_PROCESS_COMMAND = 41
    GET_PROCESS_IDENTITY = 42
    GET_PROCESS_STDIO = 43
    GET_PROCESS_STATE = 44
    GET_PROGRAMS = 46
    DEFINE_PROGRAM = 47
    PURGE_PROGRAM = 48
    GET_PROGRAM_IDENTIFIER = 49
    GET_PROGRAM_ROOT_DIRECTORY = 50
    SET_PROGRAM_COMMAND = 51
    GET_PROGRAM_COMMAND = 52
    SET_PROGRAM_STDIO_REDIRECTION = 53
    GET_PROGRAM_STDIO_REDIRECTION = 54
    SET_PROGRAM_SCHEDULE = 55
    GET_PROGRAM_SCHEDULE = 56
    GET_PROGRAM_SCHEDULER_STATE = 57
    CONTINUE_PROGRAM_SCHEDULE = 58
    START_PROGRAM = 59
    GET_LAST_SPAWNED_PROGRAM_PROCESS = 60
    GET_CUSTOM_PROGRAM_OPTION_NAMES = 61
    SET_CUSTOM_PROGRAM_OPTION_VALUE = 62
    GET_CUSTOM_PROGRAM_OPTION_VALUE = 63
    REMOVE_CUSTOM_PROGRAM_OPTION = 64


@unique
class ErrorCode(Enum):
    """
    The error code options
    """

    SUCCESS = 0
    UNKNOWN_ERROR = 1
    INVALID_OPERATION = 2
    OPERATION_ABORTED = 3
    INTERNAL_ERROR = 4
    UNKNOWN_SESSION_ID = 5
    NO_FREE_SESSION_ID = 6
    UNKNOWN_OBJECT_ID = 7
    NO_FREE_OBJECT_ID = 8
    OBJECT_IS_LOCKED = 9
    NO_MORE_DATA = 10
    WRONG_LIST_ITEM_TYPE = 11
    PROGRAM_IS_PURGED = 12
    INVALID_PARAMETER = 128
    NO_FREE_MEMORY = 129
    NO_FREE_SPACE = 130
    ACCESS_DENIED = 121
    ALREADY_EXISTS = 132
    DOES_NOT_EXIST = 133
    INTERRUPTED = 134
    IS_DIRECTORY = 135
    NOT_A_DIRECTORY = 136
    WOULD_BLOCK = 137
    OVERFLOW = 138
    BAD_FILE_DESCRIPTOR = 139
    OUT_OF_RANGE = 140
    NAME_TOO_LONG = 141
    INVALID_SEEK = 142
    NOT_SUPPORTED = 143
    TOO_MANY_OPEN_FILES = 144


@unique
class ObjectType(Enum):
    """
    The object type options
    """

    STRING = 0
    LIST = 1
    FILE = 2
    DIRECTORY = 3
    PROCESS = 4
    PROGRAM = 5


@unique
class FileFlag(Enum):
    """
    The file flag options
    """

    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = 4
    APPEND = 8
    CREATE = 16
    EXCLUSIVE = 32
    NON_BLOCKING = 64
    TRUNCATE = 128
    TEMPORARY = 256
    REPLACE = 512


@unique
class FilePermission(Enum):
    """
    The file permission options
    """

    USER_ALL = 448
    USER_READ = 256
    USER_WRITE = 128
    USER_EXECUTE = 64
    GROUP_ALL = 56
    GROUP_READ = 32
    GROUP_WRITE = 16
    GROUP_EXECUTE = 8
    OTHERS_ALL = 7
    OTHERS_READ = 4
    OTHERS_WRITE = 2
    OTHERS_EXECUTE = 1


@unique
class PipeFlag(Enum):
    """
    The pipe flag options
    """

    NON_BLOCKING_READ = 1
    NON_BLOCKING_WRITE = 2


@unique
class FileType(Enum):
    """
    The file type options
    """

    UNKNOWN = 0
    REGULAR = 1
    DIRECTORY = 2
    CHARACTER = 3
    BLOCK = 4
    FIFO = 5
    SYMLINK = 6
    SOCKET = 7
    PIPE = 8


@unique
class FileOrigin(Enum):
    """
    The file origin options
    """

    BEGINNING = 0
    CURRENT = 1
    END = 2


@unique
class FileEvent(Enum):
    """
    The file event options
    """

    READABLE = 1
    WRITABLE = 2


@unique
class DirectoryEntryType(Enum):
    """
    The directory entry type options
    """

    UNKNOWN = 0
    REGULAR = 1
    DIRECTORY = 2
    CHARACTER = 3
    BLOCK = 4
    FIFO = 5
    SYMLINK = 6
    SOCKET = 7


@unique
class DirectoryFlag(Enum):
    """
    The directory flag options
    """

    RECURSIVE = 1
    EXCLUSIVE = 2


@unique
class ProcessSignal(Enum):
    """
    The process signal options
    """

    INTERRUPT = 2
    QUIT = 3
    ABORT = 6
    KILL = 9
    USER1 = 10
    USER2 = 12
    TERMINATE = 15
    CONTINUE = 18
    STOP = 19


@unique
class ProcessState(Enum):
    """
    The process state options
    """

    UNKNOWN = 0
    RUNNING = 1
    ERROR = 2
    EXITED = 3
    KILLED = 4
    STOPPED = 5


@unique
class ProgramStdioRedirection(Enum):
    """
    The program stdio redirection options
    """

    DEV_NULL = 0
    PIPE = 1
    FILE = 2
    INDIVIDUAL_LOG = 3
    CONTINUOUS_LOG = 4
    STDOUT = 5


@unique
class ProgramStartMode(Enum):
    """
    The program start mode options
    """

    NEVER = 0
    ALWAYS = 1
    INTERVAL = 2
    CRON = 3


@unique
class ProgramSchedulerState(Enum):
    """
    The program scheduler state options
    """

    STOPPED = 0
    RUNNING = 1


class CreateSession(NamedTuple):
    error_code: ErrorCode
    session_id: int


class AllocateString(NamedTuple):
    error_code: ErrorCode
    string_id: int


class GetStringLength(NamedTuple):
    error_code: ErrorCode
    length: int


class GetStringChunk(NamedTuple):
    error_code: ErrorCode
    buffer: str


class AllocateList(NamedTuple):
    error_code: ErrorCode
    list_id: int


class GetListLength(NamedTuple):
    error_code: ErrorCode
    length: int


class GetListItem(NamedTuple):
    error_code: ErrorCode
    item_object_id: int
    type_: ObjectType


class OpenFile(NamedTuple):
    error_code: ErrorCode
    file_id: int


class CreatePipe(NamedTuple):
    error_code: ErrorCode
    file_id: int


class GetFileInfo(NamedTuple):
    error_code: ErrorCode
    type_: FileType
    name_string_id: int
    flags: FileFlag
    permissions: FilePermission
    uid: int
    gid: int
    length: int
    access_timestamp: int
    modification_timestamp: int
    status_change_timestamp: int


class ReadFile(NamedTuple):
    error_code: ErrorCode
    buffer: tuple[int, ...]
    length_read: int


class WriteFile(NamedTuple):
    error_code: ErrorCode
    length_written: int


class SetFilePosition(NamedTuple):
    error_code: ErrorCode
    position: int


class GetFilePosition(NamedTuple):
    error_code: ErrorCode
    position: int


class GetFileEvents(NamedTuple):
    error_code: ErrorCode
    events: FileEvent


class OpenDirectory(NamedTuple):
    error_code: ErrorCode
    directory_id: int


class GetDirectoryName(NamedTuple):
    error_code: ErrorCode
    name_string_id: int


class GetNextDirectoryEntry(NamedTuple):
    error_code: ErrorCode
    name_string_id: int
    type_: DirectoryEntryType


class GetProcesses(NamedTuple):
    error_code: ErrorCode
    processes_list_id: int


class SpawnProcess(NamedTuple):
    error_code: ErrorCode
    process_id: int


class GetProcessCommand(NamedTuple):
    error_code: ErrorCode
    executable_string_id: int
    arguments_list_id: int
    environment_list_id: int
    working_directory_string_id: int


class GetProcessIdentity(NamedTuple):
    error_code: ErrorCode
    pid: int
    uid: int
    gid: int


class GetProcessStdio(NamedTuple):
    error_code: ErrorCode
    stdin_file_id: int
    stdout_file_id: int
    stderr_file_id: int


class GetProcessState(NamedTuple):
    error_code: ErrorCode
    state: ProcessState
    timestamp: int
    exit_code: int


class GetPrograms(NamedTuple):
    error_code: ErrorCode
    programs_list_id: int


class DefineProgram(NamedTuple):
    error_code: ErrorCode
    program_id: int


class GetProgramIdentifier(NamedTuple):
    error_code: ErrorCode
    identifier_string_id: int


class GetProgramRootDirectory(NamedTuple):
    error_code: ErrorCode
    root_directory_string_id: int


class GetProgramCommand(NamedTuple):
    error_code: ErrorCode
    executable_string_id: int
    arguments_list_id: int
    environment_list_id: int
    working_directory_string_id: int


class GetProgramStdioRedirection(NamedTuple):
    error_code: ErrorCode
    stdin_redirection: ProgramStdioRedirection
    stdin_file_name_string_id: int
    stdout_redirection: ProgramStdioRedirection
    stdout_file_name_string_id: int
    stderr_redirection: ProgramStdioRedirection
    stderr_file_name_string_id: int


class GetProgramSchedule(NamedTuple):
    error_code: ErrorCode
    start_mode: ProgramStartMode
    continue_after_error: bool
    start_interval: int
    start_fields_string_id: int


class GetProgramSchedulerState(NamedTuple):
    error_code: ErrorCode
    state: ProgramSchedulerState
    timestamp: int
    message_string_id: int


class GetLastSpawnedProgramProcess(NamedTuple):
    error_code: ErrorCode
    process_id: int
    timestamp: int


class GetCustomProgramOptionNames(NamedTuple):
    error_code: ErrorCode
    names_list_id: int


class GetCustomProgramOptionValue(NamedTuple):
    error_code: ErrorCode
    value_string_id: int


class AsyncFileReadEvent(NamedTuple):
    file_id: int
    error_code: ErrorCode
    buffer: tuple[int, ...]
    length_read: int


class AsyncFileWriteEvent(NamedTuple):
    file_id: int
    error_code: ErrorCode
    length_written: int


class FileEventsOccurredEvent(NamedTuple):
    file_id: int
    events: FileEvent


class ProcessStateChangedEvent(NamedTuple):
    process_id: int
    state: ProcessState
    timestamp: int
    exit_code: int


class BrickRED(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Executes user programs and controls other Bricks/Bricklets standalone
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_RED
    DEVICE_DISPLAY_NAME = "RED Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ErrorCode: TypeAlias = ErrorCode
    ObjectType: TypeAlias = ObjectType
    FileFlag: TypeAlias = FileFlag
    FilePermission: TypeAlias = FilePermission
    PipeFlag: TypeAlias = PipeFlag
    FileType: TypeAlias = FileType
    FileOrigin: TypeAlias = FileOrigin
    FileEvent: TypeAlias = FileEvent
    DirectoryEntryType: TypeAlias = DirectoryEntryType
    DirectoryFlag: TypeAlias = DirectoryFlag
    ProcessSignal: TypeAlias = ProcessSignal
    ProcessState: TypeAlias = ProcessState
    ProgramStdioRedirection: TypeAlias = ProgramStdioRedirection
    ProgramStartMode: TypeAlias = ProgramStartMode
    ProgramSchedulerState: TypeAlias = ProgramSchedulerState

    CALLBACK_FORMATS = {
        CallbackID.ASYNC_FILE_READ: "H B 60B B",
        CallbackID.ASYNC_FILE_WRITE: "H B B",
        CallbackID.FILE_EVENTS_OCCURRED: "H H",
        CallbackID.PROCESS_STATE_CHANGED: "H B Q B",
        CallbackID.PROGRAM_SCHEDULER_STATE_CHANGED: "H",
        CallbackID.PROGRAM_PROCESS_SPAWNED: "H",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.ASYNC_FILE_READ,)),
        Channel(1, callbacks=(CallbackID.ASYNC_FILE_WRITE,)),
        Channel(2, callbacks=(CallbackID.FILE_EVENTS_OCCURRED,)),
        Channel(3, callbacks=(CallbackID.PROCESS_STATE_CHANGED,)),
        Channel(4, callbacks=(CallbackID.PROGRAM_SCHEDULER_STATE_CHANGED,)),
        Channel(5, callbacks=(CallbackID.PROGRAM_PROCESS_SPAWNED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def create_session(self, lifetime: int) -> CreateSession:
        """
        Create Session.
        """
        lifetime = int(lifetime)
        check_range("lifetime", lifetime, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CREATE_SESSION,
            data=pack_payload((lifetime,), "I"),
            response_expected=True,
        )
        error_code, session_id = unpack_payload(payload, "B H")
        return CreateSession(ErrorCode(error_code), session_id)

    async def expire_session(self, session_id: int) -> ErrorCode:
        """
        Expire Session.
        """
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.EXPIRE_SESSION,
            data=pack_payload((session_id,), "H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def expire_session_unchecked(self, session_id: int, response_expected: bool = True) -> None:
        """
        Expire Session Unchecked.
        """
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.EXPIRE_SESSION_UNCHECKED,
            data=pack_payload((session_id,), "H"),
            response_expected=response_expected,
        )

    async def keep_session_alive(self, session_id: int, lifetime: int) -> ErrorCode:
        """
        Keep Session Alive.
        """
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        lifetime = int(lifetime)
        check_range("lifetime", lifetime, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.KEEP_SESSION_ALIVE,
            data=pack_payload((session_id, lifetime), "H I"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def release_object(self, object_id: int, session_id: int) -> ErrorCode:
        """
        Decreases the reference count of an object by one and returns the resulting
        error code. If the reference count reaches zero the object gets destroyed.
        """
        object_id = int(object_id)
        check_range("object_id", object_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.RELEASE_OBJECT,
            data=pack_payload((object_id, session_id), "H H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def release_object_unchecked(self, object_id: int, session_id: int, response_expected: bool = True) -> None:
        """
        Release Object Unchecked.
        """
        object_id = int(object_id)
        check_range("object_id", object_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.RELEASE_OBJECT_UNCHECKED,
            data=pack_payload((object_id, session_id), "H H"),
            response_expected=response_expected,
        )

    async def allocate_string(self, length_to_reserve: int, buffer: str, session_id: int) -> AllocateString:
        """
        Allocates a new string object, reserves ``length_to_reserve`` bytes memory
        for it and sets up to the first 60 bytes. Set ``length_to_reserve`` to the
        length of the string that should be stored in the string object.

        Returns the object ID of the new string object and the resulting error code.
        """
        length_to_reserve = int(length_to_reserve)
        check_range("length_to_reserve", length_to_reserve, 0, 4294967295)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.ALLOCATE_STRING,
            data=pack_payload((length_to_reserve, str(buffer).encode("latin-1"), session_id), "I 58s H"),
            response_expected=True,
        )
        error_code, string_id = unpack_payload(payload, "B H")
        return AllocateString(ErrorCode(error_code), string_id)

    async def truncate_string(self, string_id: int, length: int) -> ErrorCode:
        """
        Truncates a string object to ``length`` bytes and returns the resulting
        error code.
        """
        string_id = int(string_id)
        check_range("string_id", string_id, 0, 65535)
        length = int(length)
        check_range("length", length, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.TRUNCATE_STRING,
            data=pack_payload((string_id, length), "H I"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_string_length(self, string_id: int) -> GetStringLength:
        """
        Returns the length of a string object and the resulting error code.
        """
        string_id = int(string_id)
        check_range("string_id", string_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_STRING_LENGTH,
            data=pack_payload((string_id,), "H"),
            response_expected=True,
        )
        error_code, length = unpack_payload(payload, "B I")
        return GetStringLength(ErrorCode(error_code), length)

    async def set_string_chunk(self, string_id: int, offset: int, buffer: str) -> ErrorCode:
        """
        Sets a chunk of up to 58 bytes in a string object beginning at ``offset``.

        Returns the resulting error code.
        """
        string_id = int(string_id)
        check_range("string_id", string_id, 0, 65535)
        offset = int(offset)
        check_range("offset", offset, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STRING_CHUNK,
            data=pack_payload((string_id, offset, str(buffer).encode("latin-1")), "H I 58s"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_string_chunk(self, string_id: int, offset: int) -> GetStringChunk:
        """
        Returns a chunk up to 63 bytes from a string object beginning at ``offset`` and
        returns the resulting error code.
        """
        string_id = int(string_id)
        check_range("string_id", string_id, 0, 65535)
        offset = int(offset)
        check_range("offset", offset, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_STRING_CHUNK,
            data=pack_payload((string_id, offset), "H I"),
            response_expected=True,
        )
        error_code, buffer = unpack_payload(payload, "B 63s")
        return GetStringChunk(ErrorCode(error_code), buffer)

    async def allocate_list(self, length_to_reserve: int, session_id: int) -> AllocateList:
        """
        Allocates a new list object and reserves memory for ``length_to_reserve``
        items. Set ``length_to_reserve`` to the number of items that should be stored
        in the list object.

        Returns the object ID of the new list object and the resulting error code.

        When a list object gets destroyed then the reference count of each object in
        the list object is decreased by one.
        """
        length_to_reserve = int(length_to_reserve)
        check_range("length_to_reserve", length_to_reserve, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.ALLOCATE_LIST,
            data=pack_payload((length_to_reserve, session_id), "H H"),
            response_expected=True,
        )
        error_code, list_id = unpack_payload(payload, "B H")
        return AllocateList(ErrorCode(error_code), list_id)

    async def get_list_length(self, list_id: int) -> GetListLength:
        """
        Returns the length of a list object in items and the resulting error code.
        """
        list_id = int(list_id)
        check_range("list_id", list_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_LIST_LENGTH,
            data=pack_payload((list_id,), "H"),
            response_expected=True,
        )
        error_code, length = unpack_payload(payload, "B H")
        return GetListLength(ErrorCode(error_code), length)

    async def get_list_item(self, list_id: int, index: int, session_id: int) -> GetListItem:
        """
        Returns the object ID and type of the object stored at ``index`` in a list
        object and returns the resulting error code.

        Possible object types are:

        * String = 0
        * List = 1
        * File = 2
        * Directory = 3
        * Process = 4
        * Program = 5
        """
        list_id = int(list_id)
        check_range("list_id", list_id, 0, 65535)
        index = int(index)
        check_range("index", index, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_LIST_ITEM,
            data=pack_payload((list_id, index, session_id), "H H H"),
            response_expected=True,
        )
        error_code, item_object_id, type_ = unpack_payload(payload, "B H B")
        return GetListItem(ErrorCode(error_code), item_object_id, ObjectType(type_))

    async def append_to_list(self, list_id: int, item_object_id: int) -> ErrorCode:
        """
        Appends an object to a list object and increases the reference count of the
        appended object by one.

        Returns the resulting error code.
        """
        list_id = int(list_id)
        check_range("list_id", list_id, 0, 65535)
        item_object_id = int(item_object_id)
        check_range("item_object_id", item_object_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.APPEND_TO_LIST,
            data=pack_payload((list_id, item_object_id), "H H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def remove_from_list(self, list_id: int, index: int) -> ErrorCode:
        """
        Removes the object stored at ``index`` from a list object and decreases the
        reference count of the removed object by one.

        Returns the resulting error code.
        """
        list_id = int(list_id)
        check_range("list_id", list_id, 0, 65535)
        index = int(index)
        check_range("index", index, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REMOVE_FROM_LIST,
            data=pack_payload((list_id, index), "H H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def open_file(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        name_string_id: int,
        flags: FileFlag | int,
        permissions: FilePermission | int,
        uid: int,
        gid: int,
        session_id: int,
    ) -> OpenFile:
        """
        Opens an existing file or creates a new file and allocates a new file object
        for it.

        FIXME: name has to be absolute

        The reference count of the name string object is increased by one. When the
        file object gets destroyed then the reference count of the name string object is
        decreased by one. Also the name string object is locked and cannot be modified
        while the file object holds a reference to it.

        The ``flags`` parameter takes a ORed combination of the following possible file
        flags (in hexadecimal notation):

        * ReadOnly = 0x0001 (O_RDONLY)
        * WriteOnly = 0x0002 (O_WRONLY)
        * ReadWrite = 0x0004 (O_RDWR)
        * Append = 0x0008 (O_APPEND)
        * Create = 0x0010 (O_CREAT)
        * Exclusive = 0x0020 (O_EXCL)
        * NonBlocking = 0x0040 (O_NONBLOCK)
        * Truncate = 0x0080 (O_TRUNC)
        * Temporary = 0x0100
        * Replace = 0x0200

        FIXME: explain *Temporary* and *Replace* flag

        The ``permissions`` parameter takes a ORed combination of the following
        possible file permissions (in octal notation) that match the common UNIX
        permission bits:

        * UserRead = 00400
        * UserWrite = 00200
        * UserExecute = 00100
        * GroupRead = 00040
        * GroupWrite = 00020
        * GroupExecute = 00010
        * OthersRead = 00004
        * OthersWrite = 00002
        * OthersExecute = 00001

        Returns the object ID of the new file object and the resulting error code.
        """
        name_string_id = int(name_string_id)
        check_range("name_string_id", name_string_id, 0, 65535)
        uid = int(uid)
        check_range("uid", uid, 0, 4294967295)
        gid = int(gid)
        check_range("gid", gid, 0, 4294967295)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.OPEN_FILE,
            data=pack_payload(
                (name_string_id, FileFlag(flags).value, FilePermission(permissions).value, uid, gid, session_id),
                "H I H I I H",
            ),
            response_expected=True,
        )
        error_code, file_id = unpack_payload(payload, "B H")
        return OpenFile(ErrorCode(error_code), file_id)

    async def create_pipe(self, flags: PipeFlag | int, length: int, session_id: int) -> CreatePipe:
        """
        Creates a new pipe and allocates a new file object for it.

        The ``flags`` parameter takes a ORed combination of the following possible
        pipe flags (in hexadecimal notation):

        * NonBlockingRead = 0x0001
        * NonBlockingWrite = 0x0002

        The length of the pipe buffer can be specified with the ``length`` parameter
        in bytes. If length is set to zero, then the default pipe buffer length is used.

        Returns the object ID of the new file object and the resulting error code.
        """
        length = int(length)
        check_range("length", length, 0, 18446744073709551615)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CREATE_PIPE,
            data=pack_payload((PipeFlag(flags).value, length, session_id), "I Q H"),
            response_expected=True,
        )
        error_code, file_id = unpack_payload(payload, "B H")
        return CreatePipe(ErrorCode(error_code), file_id)

    async def get_file_info(  # pylint: disable=too-many-locals
        self,
        file_id: int,
        session_id: int,
    ) -> GetFileInfo:
        """
        Returns various information about a file and the resulting error code.

        Possible file types are:

        * Unknown = 0
        * Regular = 1
        * Directory = 2
        * Character = 3
        * Block = 4
        * FIFO = 5
        * Symlink = 6
        * Socket = 7
        * Pipe = 8

        If the file type is *Pipe* then the returned name string object is invalid,
        because a pipe has no name. Otherwise the returned name string object was used
        to open or create the file object, as passed to :func:`open_file`.

        The returned flags were used to open or create the file object, as passed to
        :func:`open_file` or :func:`create_pipe`. See the respective function for a list
        of possible file and pipe flags.

        FIXME: everything except flags and length is invalid if file type is *Pipe*
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_FILE_INFO,
            data=pack_payload((file_id, session_id), "H H"),
            response_expected=True,
        )
        (
            error_code,
            type_,
            name_string_id,
            flags,
            permissions,
            uid,
            gid,
            length,
            access_timestamp,
            modification_timestamp,
            status_change_timestamp,
        ) = unpack_payload(payload, "B B H I H I I Q Q Q Q")
        return GetFileInfo(
            ErrorCode(error_code),
            FileType(type_),
            name_string_id,
            FileFlag(flags),
            FilePermission(permissions),
            uid,
            gid,
            length,
            access_timestamp,
            modification_timestamp,
            status_change_timestamp,
        )

    async def read_file(self, file_id: int, length_to_read: int) -> ReadFile:
        """
        Reads up to 62 bytes from a file object.

        Returns the bytes read, the actual number of bytes read and the resulting
        error code.

        If there is not data to be read, either because the file position reached
        end-of-file or because there is not data in the pipe, then zero bytes are
        returned.

        If the file object was created by :func:`open_file` without the *NonBlocking*
        flag or by :func:`create_pipe` without the *NonBlockingRead* flag then the
        error code *NotSupported* is returned.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        length_to_read = int(length_to_read)
        check_range("length_to_read", length_to_read, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_FILE,
            data=pack_payload((file_id, length_to_read), "H B"),
            response_expected=True,
        )
        error_code, buffer, length_read = unpack_payload(payload, "B 62B B")
        return ReadFile(ErrorCode(error_code), tuple(buffer), length_read)

    async def read_file_async(self, file_id: int, length_to_read: int, response_expected: bool = True) -> None:
        r"""
        Reads up to 2\ ``63``\  - 1 bytes from a file object asynchronously.

        Reports the bytes read (in 60 byte chunks), the actual number of bytes read and
        the resulting error code via the :attr:`CallbackID.ASYNC_FILE_READ` callback.

        If there is not data to be read, either because the file position reached
        end-of-file or because there is not data in the pipe, then zero bytes are
        reported.

        If the file object was created by :func:`open_file` without the *NonBlocking*
        flag or by :func:`create_pipe` without the *NonBlockingRead* flag then the error
        code *NotSupported* is reported via the :attr:`CallbackID.ASYNC_FILE_READ` callback.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        length_to_read = int(length_to_read)
        check_range("length_to_read", length_to_read, 0, 18446744073709551615)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_FILE_ASYNC,
            data=pack_payload((file_id, length_to_read), "H Q"),
            response_expected=response_expected,
        )

    async def abort_async_file_read(self, file_id: int) -> ErrorCode:
        """
        Aborts a :func:`read_file_async` operation in progress.

        Returns the resulting error code.

        On success the :attr:`CallbackID.ASYNC_FILE_READ` callback will report *OperationAborted*.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.ABORT_ASYNC_FILE_READ,
            data=pack_payload((file_id,), "H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def write_file(self, file_id: int, buffer: bytes | Sequence[int], length_to_write: int) -> WriteFile:
        """
        Writes up to 61 bytes to a file object.

        Returns the actual number of bytes written and the resulting error code.

        If the file object was created by :func:`open_file` without the *NonBlocking*
        flag or by :func:`create_pipe` without the *NonBlockingWrite* flag then the
        error code *NotSupported* is returned.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        check_length("buffer", buffer, 61)
        length_to_write = int(length_to_write)
        check_range("length_to_write", length_to_write, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FILE,
            data=pack_payload((file_id, list(map(int, buffer)), length_to_write), "H 61B B"),
            response_expected=True,
        )
        error_code, length_written = unpack_payload(payload, "B B")
        return WriteFile(ErrorCode(error_code), length_written)

    async def write_file_unchecked(
        self, file_id: int, buffer: bytes | Sequence[int], length_to_write: int, response_expected: bool = True
    ) -> None:
        """
        Writes up to 61 bytes to a file object.

        Does neither report the actual number of bytes written nor the resulting error
        code.

        If the file object was created by :func:`open_file` without the *NonBlocking*
        flag or by :func:`create_pipe` without the *NonBlockingWrite* flag then the
        write operation will fail silently.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        check_length("buffer", buffer, 61)
        length_to_write = int(length_to_write)
        check_range("length_to_write", length_to_write, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FILE_UNCHECKED,
            data=pack_payload((file_id, list(map(int, buffer)), length_to_write), "H 61B B"),
            response_expected=response_expected,
        )

    async def write_file_async(
        self, file_id: int, buffer: bytes | Sequence[int], length_to_write: int, response_expected: bool = True
    ) -> None:
        """
        Writes up to 61 bytes to a file object.

        Reports the actual number of bytes written and the resulting error code via the
        :attr:`CallbackID.ASYNC_FILE_WRITE` callback.

        If the file object was created by :func:`open_file` without the *NonBlocking*
        flag or by :func:`create_pipe` without the *NonBlockingWrite* flag then the
        error code *NotSupported* is reported via the :attr:`CallbackID.ASYNC_FILE_WRITE` callback.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        check_length("buffer", buffer, 61)
        length_to_write = int(length_to_write)
        check_range("length_to_write", length_to_write, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FILE_ASYNC,
            data=pack_payload((file_id, list(map(int, buffer)), length_to_write), "H 61B B"),
            response_expected=response_expected,
        )

    async def set_file_position(self, file_id: int, offset: int, origin: FileOrigin | int) -> SetFilePosition:
        """
        Set the current seek position of a file object relative to ``origin``.

        Possible file origins are:

        * Beginning = 0
        * Current = 1
        * End = 2

        Returns the resulting absolute seek position and error code.

        If the file object was created by :func:`create_pipe` then it has no seek
        position and the error code *InvalidSeek* is returned.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        offset = int(offset)
        check_range("offset", offset, -9223372036854775808, 9223372036854775807)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FILE_POSITION,
            data=pack_payload((file_id, offset, FileOrigin(origin).value), "H q B"),
            response_expected=True,
        )
        error_code, position = unpack_payload(payload, "B Q")
        return SetFilePosition(ErrorCode(error_code), position)

    async def get_file_position(self, file_id: int) -> GetFilePosition:
        """
        Returns the current seek position of a file object and returns the
        resulting error code.

        If the file object was created by :func:`create_pipe` then it has no seek
        position and the error code *InvalidSeek* is returned.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_FILE_POSITION,
            data=pack_payload((file_id,), "H"),
            response_expected=True,
        )
        error_code, position = unpack_payload(payload, "B Q")
        return GetFilePosition(ErrorCode(error_code), position)

    async def set_file_events(self, file_id: int, events: FileEvent | int) -> ErrorCode:
        """
        Set File Events.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FILE_EVENTS,
            data=pack_payload((file_id, FileEvent(events).value), "H H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_file_events(self, file_id: int) -> GetFileEvents:
        """
        Get File Events.
        """
        file_id = int(file_id)
        check_range("file_id", file_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_FILE_EVENTS,
            data=pack_payload((file_id,), "H"),
            response_expected=True,
        )
        error_code, events = unpack_payload(payload, "B H")
        return GetFileEvents(ErrorCode(error_code), FileEvent(events))

    async def open_directory(self, name_string_id: int, session_id: int) -> OpenDirectory:
        """
        Opens an existing directory and allocates a new directory object for it.

        FIXME: name has to be absolute

        The reference count of the name string object is increased by one. When the
        directory object is destroyed then the reference count of the name string
        object is decreased by one. Also the name string object is locked and cannot be
        modified while the directory object holds a reference to it.

        Returns the object ID of the new directory object and the resulting error code.
        """
        name_string_id = int(name_string_id)
        check_range("name_string_id", name_string_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.OPEN_DIRECTORY,
            data=pack_payload((name_string_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, directory_id = unpack_payload(payload, "B H")
        return OpenDirectory(ErrorCode(error_code), directory_id)

    async def get_directory_name(self, directory_id: int, session_id: int) -> GetDirectoryName:
        """
        Returns the name of a directory object, as passed to :func:`open_directory`, and
        the resulting error code.
        """
        directory_id = int(directory_id)
        check_range("directory_id", directory_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_DIRECTORY_NAME,
            data=pack_payload((directory_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, name_string_id = unpack_payload(payload, "B H")
        return GetDirectoryName(ErrorCode(error_code), name_string_id)

    async def get_next_directory_entry(self, directory_id: int, session_id: int) -> GetNextDirectoryEntry:
        """
        Returns the next entry in a directory object and the resulting error code.

        If there is not next entry then error code *NoMoreData* is returned. To rewind
        a directory object call :func:`rewind_directory`.

        Possible directory entry types are:

        * Unknown = 0
        * Regular = 1
        * Directory = 2
        * Character = 3
        * Block = 4
        * FIFO = 5
        * Symlink = 6
        * Socket = 7
        """
        directory_id = int(directory_id)
        check_range("directory_id", directory_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_NEXT_DIRECTORY_ENTRY,
            data=pack_payload((directory_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, name_string_id, type_ = unpack_payload(payload, "B H B")
        return GetNextDirectoryEntry(ErrorCode(error_code), name_string_id, DirectoryEntryType(type_))

    async def rewind_directory(self, directory_id: int) -> ErrorCode:
        """
        Rewinds a directory object and returns the resulting error code.
        """
        directory_id = int(directory_id)
        check_range("directory_id", directory_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REWIND_DIRECTORY,
            data=pack_payload((directory_id,), "H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def create_directory(
        self, name_string_id: int, flags: DirectoryFlag | int, permissions: FilePermission | int, uid: int, gid: int
    ) -> ErrorCode:
        """
        FIXME: name has to be absolute
        """
        name_string_id = int(name_string_id)
        check_range("name_string_id", name_string_id, 0, 65535)
        uid = int(uid)
        check_range("uid", uid, 0, 4294967295)
        gid = int(gid)
        check_range("gid", gid, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CREATE_DIRECTORY,
            data=pack_payload(
                (name_string_id, DirectoryFlag(flags).value, FilePermission(permissions).value, uid, gid), "H I H I I"
            ),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_processes(self, session_id: int) -> GetProcesses:
        """
        Get Processes.
        """
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROCESSES,
            data=pack_payload((session_id,), "H"),
            response_expected=True,
        )
        error_code, processes_list_id = unpack_payload(payload, "B H")
        return GetProcesses(ErrorCode(error_code), processes_list_id)

    async def spawn_process(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        executable_string_id: int,
        arguments_list_id: int,
        environment_list_id: int,
        working_directory_string_id: int,
        uid: int,
        gid: int,
        stdin_file_id: int,
        stdout_file_id: int,
        stderr_file_id: int,
        session_id: int,
    ) -> SpawnProcess:
        """
        Spawn Process.
        """
        executable_string_id = int(executable_string_id)
        check_range("executable_string_id", executable_string_id, 0, 65535)
        arguments_list_id = int(arguments_list_id)
        check_range("arguments_list_id", arguments_list_id, 0, 65535)
        environment_list_id = int(environment_list_id)
        check_range("environment_list_id", environment_list_id, 0, 65535)
        working_directory_string_id = int(working_directory_string_id)
        check_range("working_directory_string_id", working_directory_string_id, 0, 65535)
        uid = int(uid)
        check_range("uid", uid, 0, 4294967295)
        gid = int(gid)
        check_range("gid", gid, 0, 4294967295)
        stdin_file_id = int(stdin_file_id)
        check_range("stdin_file_id", stdin_file_id, 0, 65535)
        stdout_file_id = int(stdout_file_id)
        check_range("stdout_file_id", stdout_file_id, 0, 65535)
        stderr_file_id = int(stderr_file_id)
        check_range("stderr_file_id", stderr_file_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SPAWN_PROCESS,
            data=pack_payload(
                (
                    executable_string_id,
                    arguments_list_id,
                    environment_list_id,
                    working_directory_string_id,
                    uid,
                    gid,
                    stdin_file_id,
                    stdout_file_id,
                    stderr_file_id,
                    session_id,
                ),
                "H H H H I I H H H H",
            ),
            response_expected=True,
        )
        error_code, process_id = unpack_payload(payload, "B H")
        return SpawnProcess(ErrorCode(error_code), process_id)

    async def kill_process(self, process_id: int, signal: ProcessSignal | int) -> ErrorCode:
        """
        Sends a UNIX signal to a process object and returns the resulting error code.

        Possible UNIX signals are:

        * Interrupt = 2
        * Quit = 3
        * Abort = 6
        * Kill = 9
        * User1 = 10
        * User2 = 12
        * Terminate = 15
        * Continue =  18
        * Stop = 19
        """
        process_id = int(process_id)
        check_range("process_id", process_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.KILL_PROCESS,
            data=pack_payload((process_id, ProcessSignal(signal).value), "H B"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_process_command(self, process_id: int, session_id: int) -> GetProcessCommand:
        """
        Returns the executable, arguments, environment and working directory used to
        spawn a process object, as passed to :func:`spawn_process`, and the resulting
        error code.
        """
        process_id = int(process_id)
        check_range("process_id", process_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROCESS_COMMAND,
            data=pack_payload((process_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id = (
            unpack_payload(payload, "B H H H H")
        )
        return GetProcessCommand(
            ErrorCode(error_code),
            executable_string_id,
            arguments_list_id,
            environment_list_id,
            working_directory_string_id,
        )

    async def get_process_identity(self, process_id: int) -> GetProcessIdentity:
        """
        Returns the process ID and the user and group ID used to spawn a process object,
        as passed to :func:`spawn_process`, and the resulting error code.

        The process ID is only valid if the state is *Running* or *Stopped*, see
        :func:`get_process_state`.
        """
        process_id = int(process_id)
        check_range("process_id", process_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROCESS_IDENTITY,
            data=pack_payload((process_id,), "H"),
            response_expected=True,
        )
        error_code, pid, uid, gid = unpack_payload(payload, "B I I I")
        return GetProcessIdentity(ErrorCode(error_code), pid, uid, gid)

    async def get_process_stdio(self, process_id: int, session_id: int) -> GetProcessStdio:
        """
        Returns the stdin, stdout and stderr files used to spawn a process object, as
        passed to :func:`spawn_process`, and the resulting error code.
        """
        process_id = int(process_id)
        check_range("process_id", process_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROCESS_STDIO,
            data=pack_payload((process_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, stdin_file_id, stdout_file_id, stderr_file_id = unpack_payload(payload, "B H H H")
        return GetProcessStdio(ErrorCode(error_code), stdin_file_id, stdout_file_id, stderr_file_id)

    async def get_process_state(self, process_id: int) -> GetProcessState:
        """
        Returns the current state, timestamp and exit code of a process object, and
        the resulting error code.

        Possible process states are:

        * Unknown = 0
        * Running = 1
        * Error = 2
        * Exited = 3
        * Killed = 4
        * Stopped = 5

        The timestamp represents the UNIX time since when the process is in its current
        state.

        The exit code is only valid if the state is *Error*, *Exited*, *Killed* or
        *Stopped* and has different meanings depending on the state:

        * Error: error code for error occurred while spawning the process (see below)
        * Exited: exit status of the process
        * Killed: UNIX signal number used to kill the process
        * Stopped: UNIX signal number used to stop the process

        Possible exit/error codes in *Error* state are:

        * InternalError = 125
        * CannotExecute = 126
        * DoesNotExist = 127

        The *CannotExecute* error can be caused by the executable being opened for
        writing.
        """
        process_id = int(process_id)
        check_range("process_id", process_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROCESS_STATE,
            data=pack_payload((process_id,), "H"),
            response_expected=True,
        )
        error_code, state, timestamp, exit_code = unpack_payload(payload, "B B Q B")
        return GetProcessState(ErrorCode(error_code), ProcessState(state), timestamp, exit_code)

    async def get_programs(self, session_id: int) -> GetPrograms:
        """
        Get Programs.
        """
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAMS,
            data=pack_payload((session_id,), "H"),
            response_expected=True,
        )
        error_code, programs_list_id = unpack_payload(payload, "B H")
        return GetPrograms(ErrorCode(error_code), programs_list_id)

    async def define_program(self, identifier_string_id: int, session_id: int) -> DefineProgram:
        """
        Define Program.
        """
        identifier_string_id = int(identifier_string_id)
        check_range("identifier_string_id", identifier_string_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DEFINE_PROGRAM,
            data=pack_payload((identifier_string_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, program_id = unpack_payload(payload, "B H")
        return DefineProgram(ErrorCode(error_code), program_id)

    async def purge_program(self, program_id: int, cookie: int) -> ErrorCode:
        """
        Purge Program.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        cookie = int(cookie)
        check_range("cookie", cookie, 0, 4294967295)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.PURGE_PROGRAM,
            data=pack_payload((program_id, cookie), "H I"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_program_identifier(self, program_id: int, session_id: int) -> GetProgramIdentifier:
        """
        Get Program Identifier.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAM_IDENTIFIER,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, identifier_string_id = unpack_payload(payload, "B H")
        return GetProgramIdentifier(ErrorCode(error_code), identifier_string_id)

    async def get_program_root_directory(self, program_id: int, session_id: int) -> GetProgramRootDirectory:
        """
        FIXME: root directory is absolute: <home>/programs/<identifier>
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAM_ROOT_DIRECTORY,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, root_directory_string_id = unpack_payload(payload, "B H")
        return GetProgramRootDirectory(ErrorCode(error_code), root_directory_string_id)

    async def set_program_command(
        self,
        program_id: int,
        executable_string_id: int,
        arguments_list_id: int,
        environment_list_id: int,
        working_directory_string_id: int,
    ) -> ErrorCode:
        """
        FIXME: working directory is relative to <home>/programs/<identifier>/bin
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        executable_string_id = int(executable_string_id)
        check_range("executable_string_id", executable_string_id, 0, 65535)
        arguments_list_id = int(arguments_list_id)
        check_range("arguments_list_id", arguments_list_id, 0, 65535)
        environment_list_id = int(environment_list_id)
        check_range("environment_list_id", environment_list_id, 0, 65535)
        working_directory_string_id = int(working_directory_string_id)
        check_range("working_directory_string_id", working_directory_string_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PROGRAM_COMMAND,
            data=pack_payload(
                (program_id, executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id),
                "H H H H H",
            ),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_program_command(self, program_id: int, session_id: int) -> GetProgramCommand:
        """
        FIXME: working directory is relative to <home>/programs/<identifier>/bin
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAM_COMMAND,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id = (
            unpack_payload(payload, "B H H H H")
        )
        return GetProgramCommand(
            ErrorCode(error_code),
            executable_string_id,
            arguments_list_id,
            environment_list_id,
            working_directory_string_id,
        )

    async def set_program_stdio_redirection(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        program_id: int,
        stdin_redirection: ProgramStdioRedirection | int,
        stdin_file_name_string_id: int,
        stdout_redirection: ProgramStdioRedirection | int,
        stdout_file_name_string_id: int,
        stderr_redirection: ProgramStdioRedirection | int,
        stderr_file_name_string_id: int,
    ) -> ErrorCode:
        """
        FIXME: stdio file names are relative to <home>/programs/<identifier>/bin
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        stdin_file_name_string_id = int(stdin_file_name_string_id)
        check_range("stdin_file_name_string_id", stdin_file_name_string_id, 0, 65535)
        stdout_file_name_string_id = int(stdout_file_name_string_id)
        check_range("stdout_file_name_string_id", stdout_file_name_string_id, 0, 65535)
        stderr_file_name_string_id = int(stderr_file_name_string_id)
        check_range("stderr_file_name_string_id", stderr_file_name_string_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PROGRAM_STDIO_REDIRECTION,
            data=pack_payload(
                (
                    program_id,
                    ProgramStdioRedirection(stdin_redirection).value,
                    stdin_file_name_string_id,
                    ProgramStdioRedirection(stdout_redirection).value,
                    stdout_file_name_string_id,
                    ProgramStdioRedirection(stderr_redirection).value,
                    stderr_file_name_string_id,
                ),
                "H B H B H B H",
            ),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_program_stdio_redirection(self, program_id: int, session_id: int) -> GetProgramStdioRedirection:
        """
        FIXME: stdio file names are relative to <home>/programs/<identifier>/bin
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAM_STDIO_REDIRECTION,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        (
            error_code,
            stdin_redirection,
            stdin_file_name_string_id,
            stdout_redirection,
            stdout_file_name_string_id,
            stderr_redirection,
            stderr_file_name_string_id,
        ) = unpack_payload(payload, "B B H B H B H")
        return GetProgramStdioRedirection(
            ErrorCode(error_code),
            ProgramStdioRedirection(stdin_redirection),
            stdin_file_name_string_id,
            ProgramStdioRedirection(stdout_redirection),
            stdout_file_name_string_id,
            ProgramStdioRedirection(stderr_redirection),
            stderr_file_name_string_id,
        )

    async def set_program_schedule(
        self,
        program_id: int,
        start_mode: ProgramStartMode | int,
        continue_after_error: bool,
        start_interval: int,
        start_fields_string_id: int,
    ) -> ErrorCode:
        """
        Set Program Schedule.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        start_interval = int(start_interval)
        check_range("start_interval", start_interval, 0, 4294967295)
        start_fields_string_id = int(start_fields_string_id)
        check_range("start_fields_string_id", start_fields_string_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PROGRAM_SCHEDULE,
            data=pack_payload(
                (
                    program_id,
                    ProgramStartMode(start_mode).value,
                    bool(continue_after_error),
                    start_interval,
                    start_fields_string_id,
                ),
                "H B ! I H",
            ),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_program_schedule(self, program_id: int, session_id: int) -> GetProgramSchedule:
        """
        Get Program Schedule.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAM_SCHEDULE,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, start_mode, continue_after_error, start_interval, start_fields_string_id = unpack_payload(
            payload, "B B ! I H"
        )
        return GetProgramSchedule(
            ErrorCode(error_code),
            ProgramStartMode(start_mode),
            continue_after_error,
            start_interval,
            start_fields_string_id,
        )

    async def get_program_scheduler_state(self, program_id: int, session_id: int) -> GetProgramSchedulerState:
        """
        FIXME: message is currently valid in error-occurred state only
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROGRAM_SCHEDULER_STATE,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, state, timestamp, message_string_id = unpack_payload(payload, "B B Q H")
        return GetProgramSchedulerState(
            ErrorCode(error_code), ProgramSchedulerState(state), timestamp, message_string_id
        )

    async def continue_program_schedule(self, program_id: int) -> ErrorCode:
        """
        Continue Program Schedule.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CONTINUE_PROGRAM_SCHEDULE,
            data=pack_payload((program_id,), "H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def start_program(self, program_id: int) -> ErrorCode:
        """
        Start Program.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.START_PROGRAM,
            data=pack_payload((program_id,), "H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_last_spawned_program_process(self, program_id: int, session_id: int) -> GetLastSpawnedProgramProcess:
        """
        Get Last Spawned Program Process.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_LAST_SPAWNED_PROGRAM_PROCESS,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, process_id, timestamp = unpack_payload(payload, "B H Q")
        return GetLastSpawnedProgramProcess(ErrorCode(error_code), process_id, timestamp)

    async def get_custom_program_option_names(self, program_id: int, session_id: int) -> GetCustomProgramOptionNames:
        """
        Get Custom Program Option Names.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CUSTOM_PROGRAM_OPTION_NAMES,
            data=pack_payload((program_id, session_id), "H H"),
            response_expected=True,
        )
        error_code, names_list_id = unpack_payload(payload, "B H")
        return GetCustomProgramOptionNames(ErrorCode(error_code), names_list_id)

    async def set_custom_program_option_value(
        self, program_id: int, name_string_id: int, value_string_id: int
    ) -> ErrorCode:
        """
        Set Custom Program Option Value.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        name_string_id = int(name_string_id)
        check_range("name_string_id", name_string_id, 0, 65535)
        value_string_id = int(value_string_id)
        check_range("value_string_id", value_string_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CUSTOM_PROGRAM_OPTION_VALUE,
            data=pack_payload((program_id, name_string_id, value_string_id), "H H H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    async def get_custom_program_option_value(
        self, program_id: int, name_string_id: int, session_id: int
    ) -> GetCustomProgramOptionValue:
        """
        Get Custom Program Option Value.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        name_string_id = int(name_string_id)
        check_range("name_string_id", name_string_id, 0, 65535)
        session_id = int(session_id)
        check_range("session_id", session_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CUSTOM_PROGRAM_OPTION_VALUE,
            data=pack_payload((program_id, name_string_id, session_id), "H H H"),
            response_expected=True,
        )
        error_code, value_string_id = unpack_payload(payload, "B H")
        return GetCustomProgramOptionValue(ErrorCode(error_code), value_string_id)

    async def remove_custom_program_option(self, program_id: int, name_string_id: int) -> ErrorCode:
        """
        Remove Custom Program Option.
        """
        program_id = int(program_id)
        check_range("program_id", program_id, 0, 65535)
        name_string_id = int(name_string_id)
        check_range("name_string_id", name_string_id, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REMOVE_CUSTOM_PROGRAM_OPTION,
            data=pack_payload((program_id, name_string_id), "H H"),
            response_expected=True,
        )
        return ErrorCode(unpack_payload(payload, "B"))

    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.ASYNC_FILE_READ:
            file_id, error_code, buffer, length_read = value
            return 0, AsyncFileReadEvent(file_id, ErrorCode(error_code), tuple(buffer), length_read)
        if callback_id is CallbackID.ASYNC_FILE_WRITE:
            file_id, error_code, length_written = value
            return 1, AsyncFileWriteEvent(file_id, ErrorCode(error_code), length_written)
        if callback_id is CallbackID.FILE_EVENTS_OCCURRED:
            file_id, events = value
            return 2, FileEventsOccurredEvent(file_id, FileEvent(events))
        if callback_id is CallbackID.PROCESS_STATE_CHANGED:
            process_id, state, timestamp, exit_code = value
            return 3, ProcessStateChangedEvent(process_id, ProcessState(state), timestamp, exit_code)
        if callback_id is CallbackID.PROGRAM_SCHEDULER_STATE_CHANGED:
            return 4, value
        return 5, value
