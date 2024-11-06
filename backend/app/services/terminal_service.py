# app/services/terminal_service.py
import asyncio
import logging
import pty
import os
import fcntl
import termios
import struct
from typing import Dict, Optional
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class TerminalSession:
    def __init__(self, websocket: WebSocket, terminal_id: str, user_id: int):
        self.websocket = websocket
        self.terminal_id = terminal_id
        self.user_id = user_id
        self.master_fd = None
        self.slave_fd = None
        self.process = None

    async def start(self):
        """Initialize terminal session"""
        try:
            # Create pseudo-terminal
            self.master_fd, self.slave_fd = pty.openpty()
            
            # Set terminal size
            term_size = struct.pack('HHHH', 24, 80, 0, 0)
            fcntl.ioctl(self.slave_fd, termios.TIOCSWINSZ, term_size)

            # Start shell process
            env = os.environ.copy()
            env["TERM"] = "xterm-256color"
            
            self.process = await asyncio.create_subprocess_shell(
                "bash",
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                env=env,
                start_new_session=True
            )
            
            logger.info(f"Started terminal session {self.terminal_id} for user {self.user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to start terminal session: {e}")
            return False

    async def read_output(self):
        """Read terminal output"""
        while True:
            try:
                output = os.read(self.master_fd, 1024).decode()
                if output:
                    await self.websocket.send_json({
                        "type": "output",
                        "content": output
                    })
            except Exception as e:
                logger.error(f"Error reading terminal output: {e}")
                break

    async def write_input(self, data: str):
        """Write input to terminal"""
        try:
            os.write(self.master_fd, data.encode())
        except Exception as e:
            logger.error(f"Error writing to terminal: {e}")

    async def resize(self, rows: int, cols: int):
        """Resize terminal window"""
        try:
            term_size = struct.pack('HHHH', rows, cols, 0, 0)
            fcntl.ioctl(self.slave_fd, termios.TIOCSWINSZ, term_size)
        except Exception as e:
            logger.error(f"Error resizing terminal: {e}")

    async def close(self):
        """Close terminal session"""
        try:
            if self.process:
                self.process.terminate()
                await self.process.wait()
            if self.master_fd:
                os.close(self.master_fd)
            if self.slave_fd:
                os.close(self.slave_fd)
            logger.info(f"Closed terminal session {self.terminal_id}")
        except Exception as e:
            logger.error(f"Error closing terminal session: {e}")

class TerminalManager:
    def __init__(self):
        self.sessions: Dict[str, TerminalSession] = {}

    async def create_session(self, websocket: WebSocket, terminal_id: str, user_id: int) -> Optional[TerminalSession]:
        """Create new terminal session"""
        session = TerminalSession(websocket, terminal_id, user_id)
        if await session.start():
            self.sessions[terminal_id] = session
            return session
        return None

    async def close_session(self, terminal_id: str):
        """Close terminal session"""
        if terminal_id in self.sessions:
            await self.sessions[terminal_id].close()
            del self.sessions[terminal_id]