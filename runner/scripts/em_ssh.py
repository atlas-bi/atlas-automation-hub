"""SSH connection handler."""
import sys
from pathlib import Path
from typing import Optional

import paramiko
from flask import current_app as app

from runner.model import ConnectionSsh, Task
from runner.scripts.em_messages import RunnerException, RunnerLog

sys.path.append(str(Path(__file__).parents[2]) + "/scripts")

from crypto import em_decrypt


def connect(connection: ConnectionSsh) -> paramiko.SSHClient:
    """Connect to SSH server."""
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(
        hostname=str(connection.address),
        port=(connection.port or 22),
        username=connection.username,
        password=em_decrypt(connection.password, app.config["PASS_KEY"]),
        timeout=5000,
        allow_agent=False,
        look_for_keys=False,
    )

    return session


class Ssh:
    """SSH Connection Handler Class."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        task: Task,
        run_id: Optional[str],
        connection: ConnectionSsh,
        command: str,
    ):
        """Set up class parameters."""
        self.connection = connection
        self.task = task
        self.run_id = run_id
        self.command = command
        self.session = self.__connect()

    def __connect(self) -> paramiko.SSHClient:
        try:
            return connect(self.connection)
        except BaseException as e:
            raise RunnerException(
                self.task, self.run_id, 19, f"Failed to connect.\n{e}"
            )

    def __close(self) -> None:
        try:
            self.session.close()

        except BaseException as e:
            raise RunnerException(
                self.task, self.run_id, 19, f"Failed to disconnect.\n{e}"
            )

    def run(self) -> None:
        """Run an SSH Command.

        First, this will make a connection then run the command

        :returns: Output from command.
        """
        self.__connect()

        try:
            # pylint: disable=W0612
            stdin, stdout, stderr = self.session.exec_command(  # noqa: S601
                self.command, timeout=5000
            )

            stderr_data = b""
            stdout_data = b""

            while not stdout.channel.exit_status_ready():
                stdout_data += stdout.channel.recv(1024)

            for line in iter(stdout.readline, ""):
                stdout_data += bytes(line, "utf8")

            for line in iter(stderr.readline, ""):
                stderr_data += bytes(line, "utf8")

            out = stdout_data.decode("utf-8") or "None"
            err = stderr_data.decode("utf-8") or "None"

            if stdout.channel.recv_exit_status() != 0 or stderr_data != b"":
                raise ValueError(
                    f"Command stdout: {out}\nCommand stderr: {err}",
                )

            RunnerLog(
                self.task,
                self.run_id,
                19,
                f"Command output:\n{out}",
            )

        except BaseException as e:
            raise RunnerException(
                self.task, self.run_id, 19, f"Failed to run command.\n{e}"
            )

        self.__close()
