from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from threading import Thread
import webbrowser

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AppConfig:
    host: str
    port: int
    root: Path
    entrypoint: str

    @property
    def app_file(self) -> Path:
        return self.root / self.entrypoint


@dataclass
class StaticAppServer:
    config: AppConfig
    server: ThreadingHTTPServer
    _thread: Thread | None = field(default=None, init=False, repr=False)

    @property
    def url(self) -> str:
        host, port = self.server.server_address
        url_host = "127.0.0.1" if host in {"", "0.0.0.0"} else host
        return f"http://{url_host}:{port}/{self.config.entrypoint}"

    def serve_forever(self) -> None:
        self.server.serve_forever()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._thread = Thread(target=self.serve_forever, daemon=True)
        self._thread.start()

    def shutdown(self) -> None:
        self.server.shutdown()

    def close(self) -> None:
        self.server.server_close()

    def stop(self) -> None:
        if self._thread and self._thread.is_alive():
            self.shutdown()
            self._thread.join(timeout=5)

        self.close()


class QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def resolve_project_path(path_value: str) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def load_app_config() -> AppConfig:
    load_dotenv(PROJECT_ROOT / ".env")

    return AppConfig(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "0")),
        root=resolve_project_path(os.getenv("APP_ROOT", ".")),
        entrypoint=os.getenv("APP_ENTRYPOINT", "index.html").lstrip("/"),
    )


def create_app_server(config: AppConfig | None = None) -> StaticAppServer:
    app_config = config or load_app_config()

    if not app_config.app_file.is_file():
        raise FileNotFoundError(f"Configured app entrypoint does not exist: {app_config.app_file}")

    handler = partial(QuietStaticHandler, directory=str(app_config.root))
    server = ThreadingHTTPServer((app_config.host, app_config.port), handler)
    return StaticAppServer(config=app_config, server=server)


def launch_application_server(open_browser: bool = True) -> None:
    app_server = create_app_server()

    print(f"Serving {app_server.config.app_file}", flush=True)
    print(f"Open {app_server.url}", flush=True)
    print("Press Ctrl+C to stop the server.", flush=True)

    if open_browser:
        webbrowser.open(app_server.url)

    try:
        app_server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.", flush=True)
    finally:
        app_server.close()
