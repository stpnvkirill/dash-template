import logging
from pathlib import Path
import time
import uuid

from flask import g, has_request_context, request
from flask_login import current_user
from pythonjsonlogger.json import JsonFormatter

from .base import BaseMiddlaware


class AutoContextFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if has_request_context():
            log_record.update(
                {
                    "request": {
                        "request_id": getattr(g, "request_id", None),
                        "ip": getattr(g, "ip_address", None),
                        "ua": str(getattr(g, "user_agent", "")) or None,
                        "method": request.method if request else None,
                        "path": request.path if request else None,
                    }
                }
            )
            if (
                current_user.is_authenticated
                and hasattr(current_user, "session")
                and current_user.session
            ):
                log_record.update(
                    {
                        "user": {
                            "user_id": current_user.id,
                            "session_id": current_user.session.id,
                        }
                    }
                )
            if request.path == "/_dash-update-component":
                log_record.update(
                    {
                        "callback": {
                            "triggered_id": request.json.get("parsedChangedPropsIds"),
                            "output": request.json.get("output"),
                        }
                    }
                )

        if record.exc_info:
            _exc_type, exc_value, _exc_tb = record.exc_info
            log_record["error"] = get_error_source(exc_value)

        if "exc_info" in log_record:
            del log_record["exc_info"]


root_logger = logging.getLogger()
root_logger.handlers.clear()

handler = logging.StreamHandler()
formatter = AutoContextFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={
        "asctime": "timestamp",
        "levelname": "level",
        "name": "logger",
        "message": "message",
    },
)
handler.setFormatter(formatter)
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

logging.getLogger("werkzeug").setLevel(logging.WARNING)


class LoggingMiddleware(BaseMiddlaware):
    def before(self):
        g.start_time = time.time()
        g.request_id = str(uuid.uuid7())

    def after(self, response):
        exclude_paths = [
            "/assets/",
            "/favicon.ico",
            "/_reload-hash",
            "/_dash-component-suites/",
            "/_dash-dependencies",
        ]
        if any(path in request.path for path in exclude_paths):
            return response
        duration_ms = round(
            (time.time() - getattr(g, "start_time", time.time())) * 1000, 2
        )

        extra = {
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "response_size": sum(map(len, response.iter_encoded())),
        }

        logging.info(
            "Request completed",
            extra=extra,
        )

        return response


def strip_filename(name: str):
    return "/app/" + name.rsplit("/app/", maxsplit=1)[-1]


def get_error_source(error: Exception):
    """
    Get the line of code where the error occurred
    """
    try:
        exc_traceback = error.__traceback__

        if exc_traceback is None:
            return None

        tb = exc_traceback
        while tb is not None:
            frame = tb.tb_frame
            filename = frame.f_code.co_filename
            if (
                "site-packages" not in filename
                and "lib/python" not in filename
                and "<" not in filename
                and "logs.py" not in filename
            ):
                line_no = tb.tb_lineno
                try:
                    with Path(filename).open(encoding="utf-8") as f:
                        lines = f.readlines()
                        if line_no - 1 < len(lines):
                            source_line = lines[line_no - 1].strip()
                            return {
                                "error": str(error),
                                "filename": f"{strip_filename(filename)}:{line_no}",
                                "source": source_line,
                            }
                except Exception:
                    pass
                return {
                    "error": str(error),
                    "filename": f"{strip_filename(filename)}:{line_no}",
                    "source": "Couldn't read the line",
                }

            tb = tb.tb_next

        return None  # noqa: TRY300

    except Exception:
        return None
