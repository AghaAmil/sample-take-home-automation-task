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
    """
    Represents the configuration for an application.

    This class holds the configuration details such as the host, port, root directory,
    and entrypoint for the application. It provides a property to access the complete
    path to the application's entrypoint file.

    :ivar host: The hostname or IP address where the application will run.
    :type host: str
    :ivar port: The port number on which the application listens for incoming requests.
    :type port: int
    :ivar root: The root directory of the application, where its files are located.
    :type root: Path
    :ivar entrypoint: The name of the entrypoint file for the application.
    :type entrypoint: str
    """
    host: str
    port: int
    root: Path
    entrypoint: str

    @property
    def app_file(self) -> Path:
        return self.root / self.entrypoint


@dataclass
class StaticAppServer:
    """
    Represents a static application server for serving content.

    This class is designed to represent and manage a threading-based
    HTTP server which can serve static content. It allows starting
    and stopping the server, managing its lifecycle, and getting its
    URL.

    :ivar config: The configuration settings for the server include critical server-related details.
    :type config: AppConfig
    :ivar server: The threading HTTP server instance that powers the application.
    :type server: ThreadingHTTPServer
    """
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
    """
    A specialized handler class for serving static files with suppressed logging.

    This handler overrides the `log_message` method of the parent class
    `SimpleHTTPRequestHandler` to disable logging of HTTP-related messages.
    It is useful when serving static files quietly without cluttering the
    output with log messages.
    """
    def log_message(self, format: str, *args: object) -> None:
        return


def resolve_project_path(path_value: str) -> Path:
    """
    Resolves the absolute path to a project directory.

    Converts the given path string into an absolute path. If the given path
    is relative, it will be appended to the project root directory before
    resolving to an absolute path. If the provided path contains user home
    shortcuts (e.g. '~'), these will be expanded.

    :param path_value: The input path to resolve, provided as a string.
    :type path_value: str
    :return: The absolute resolved path as a `Path` object.
    :rtype: Path
    """
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def load_app_config() -> AppConfig:
    """
    Loads the application configuration by reading environment variables
    from a `.env` file located at the project root. If an environment
    variable is not set, default values will be used. The function
    returns an `AppConfig` instance populated with the loaded
    configuration.

    :return: An `AppConfig` instance containing the application
        configuration values.
    :rtype: AppConfig
    """
    load_dotenv(PROJECT_ROOT / ".env")

    return AppConfig(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "0")),
        root=resolve_project_path(os.getenv("APP_ROOT", ".")),
        entrypoint=os.getenv("APP_ENTRYPOINT", "index.html").lstrip("/"),
    )


def create_app_server(config: AppConfig | None = None) -> StaticAppServer:
    """
    Creates and initializes a static application server instance using the provided configuration
    or a default one. This function ensures that the configured application entrypoint exists
    as a file and then sets up an HTTP server with a static handler pointing to the root directory
    specified in the configuration.

    :param config: The optional configuration object used to initialize the server. If not
        provided, the default configuration will be loaded dynamically.
    :type config: AppConfig | None
    :return: A fully initialized static application server instance ready to start serving
        requests.
    :rtype: StaticAppServer
    :raises FileNotFoundError: If the configured application entrypoint file does not exist.
    """
    app_config = config or load_app_config()

    if not app_config.app_file.is_file():
        raise FileNotFoundError(f"Configured app entrypoint does not exist: {app_config.app_file}")

    handler = partial(QuietStaticHandler, directory=str(app_config.root))
    server = ThreadingHTTPServer((app_config.host, app_config.port), handler)
    return StaticAppServer(config=app_config, server=server)


def launch_application_server(open_browser: bool = True) -> None:
    """
    Launches the application server and optionally opens it in the default web browser.

    This function initializes and starts the application server, making it accessible
    at the configured URL. It provides feedback on the console about the serving status
    and how to stop the server. If the `open_browser` parameter is set to True, the
    application URL will be opened in the default web browser.

    :param open_browser: If True, the application URL will be opened in the default web browser. Defaults to True.
    :type open_browser: bool
    :return: This function does not return a value.
    :rtype: None
    """
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
