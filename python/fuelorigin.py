"""The small helper every script in this folder shares. Standard library only, Python 3.10+.

It makes one request and never retries. It sends your key only if FO_KEY is set, and only as the
X-API-Key header. It stops on a refusal instead of working around it:

- 403: it prints the API's reason and exits with status 3. A CSV download is redistribution and
  the API can refuse one while the JSON stays readable; no script here rebuilds a refused file
  from the JSON.
- 429: it prints how long the API asks you to wait and exits with status 4.
- A route for key holders, without FO_KEY: it prints a message and exits with status 2, without
  calling the API.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

BASE_URL = "https://api.fuelorigin.org"
ACCESS_URL = "https://fuelorigin.org/api-access"
DATASETS_URL = "https://fuelorigin.org/datasets"
USER_AGENT = "fuelorigin-api-examples"
TIMEOUT_SECONDS = 120
OUT_DIR = Path("out")

EXIT_FAILED = 1
EXIT_NO_KEY = 2
EXIT_REFUSED = 3
EXIT_TOO_MANY = 4

#: Classes of figures Fuel Origin made (calculated or estimated) rather than a publisher published.
OWN_FIGURE_CLASSES = {"CALCULATED", "INFERRED_HIGH", "INFERRED_MEDIUM", "INFERRED_LOW"}

_last_url = ""


def months_ago(months: int, today: date | None = None) -> str:
    """The first day of the month `months` months ago, as YYYY-MM-DD."""
    today = today or date.today()
    index = today.year * 12 + (today.month - 1) - months
    return date(index // 12, index % 12 + 1, 1).isoformat()


def path_part(value: str, safe: str = ":") -> str:
    """One value for the path of a URL."""
    return urllib.parse.quote(value, safe=safe)


def key() -> str | None:
    """Your key from the environment variable FO_KEY, or None."""
    return os.environ.get("FO_KEY", "").strip() or None


def require_key(route_id: str) -> None:
    """Stop here, without calling the API, when a route for key holders has no key."""
    if key() is None:
        print(
            f"{route_id}: this route answers only with an API key, and FO_KEY is not set.\n"
            f"Nothing was requested. Plans and evaluation keys: {ACCESS_URL}",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_NO_KEY)


def _query_value(value: Any) -> str:
    return ("true" if value else "false") if isinstance(value, bool) else str(value)


def _reason(body: bytes) -> str:
    """The sentence the API sent with a refusal."""
    try:
        detail = json.loads(body.decode("utf-8")).get("detail")
    except (ValueError, AttributeError):
        return body.decode("utf-8", "replace").strip()[:300] or "(the answer gave no reason)"
    if isinstance(detail, list):  # A rejected parameter: one entry per problem.
        return "; ".join(f"{'.'.join(map(str, d.get('loc', [])))}: {d.get('msg')}" for d in detail)
    return str(detail)


def _refused(error: urllib.error.HTTPError) -> SystemExit:
    body = error.read()
    if error.code == 403:
        print(
            f"The API refused this request (403):\n{_reason(body)}\n"
            f"Nothing was written. Everything as files, where each source allows it: {DATASETS_URL}",
            file=sys.stderr,
        )
        return SystemExit(EXIT_REFUSED)
    if error.code == 429:
        wait = error.headers.get("Retry-After")
        said = f"It asks you to wait {wait} seconds." if wait else "It did not say how long to wait."
        print(f"Too many requests (429). {said}\nThis script does not retry. Run it again later.", file=sys.stderr)
        return SystemExit(EXIT_TOO_MANY)
    print(f"The API answered {error.code}:\n{_reason(body)}", file=sys.stderr)
    return SystemExit(EXIT_FAILED)


def _get(path: str, params: Mapping[str, Any], accept: str) -> bytes:
    global _last_url
    query = {name: _query_value(value) for name, value in params.items() if value is not None}
    _last_url = BASE_URL + path + ("?" + urllib.parse.urlencode(query) if query else "")
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if key() is not None:
        headers["X-API-Key"] = key()
    request = urllib.request.Request(_last_url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        raise _refused(error) from None
    except OSError as error:  # No connection, a timeout.
        print(f"The request did not reach the API: {error}", file=sys.stderr)
        raise SystemExit(EXIT_FAILED) from None


def get_csv(path: str, params: Mapping[str, Any]) -> bytes:
    """The route's own CSV file, exactly as the API sends it."""
    return _get(path, {**params, "format": "csv"}, "text/csv")


def get_json(path: str, params: Mapping[str, Any]) -> dict[str, Any]:
    """The route's JSON answer."""
    return json.loads(_get(path, params, "application/json").decode("utf-8"))


def _target(route_id: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUT_DIR / f"{route_id}.csv"


def _count(rows: int) -> str:
    return f"{rows} row" if rows == 1 else f"{rows} rows"


def _more_hint(rows: int, limit: int | None) -> None:
    if limit is not None and rows >= limit:
        print(
            f"The file holds {rows} rows, the limit asked for, so there may be more. "
            f"Narrow the selection or raise --limit; everything as files: {DATASETS_URL}"
        )


def save_csv(route_id: str, body: bytes, limit: int | None = None) -> None:
    """Write the API's file byte for byte. Its # lines carry the sources and conditions: keep them."""
    target = _target(route_id)
    target.write_bytes(body)
    lines = (line for line in body.decode("utf-8").splitlines() if not line.startswith("#"))
    rows = max(sum(1 for _ in csv.reader(lines)) - 1, 0)
    print(f"{target}: {_count(rows)}")
    _more_hint(rows, limit)


def flatten(row: Mapping[str, Any], prefix: str = "") -> dict[str, Any]:
    """One level of columns: nested objects become a.b columns, lists stay as JSON text in one cell."""
    out: dict[str, Any] = {}
    for name, value in row.items():
        column = f"{prefix}{name}"
        if isinstance(value, Mapping):
            out.update(flatten(value, f"{column}."))
        elif isinstance(value, list):
            out[column] = json.dumps(value, ensure_ascii=False) if value else ""
        elif isinstance(value, bool):
            out[column] = "true" if value else "false"
        else:
            out[column] = value  # None is written as a blank cell, never as 0.
    return out


def _walk(value: Any) -> Iterator[tuple[str, Any]]:
    """Every (key, value) pair anywhere in an answer."""
    if isinstance(value, Mapping):
        for name, item in value.items():
            yield name, item
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def _texts(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        return [str(value["text"])] if value.get("text") else []
    if isinstance(value, list):
        return [text for item in value for text in _texts(item)]
    return []


def _day(stamp: Any) -> str | None:
    return str(stamp)[:10] if stamp else None


def _is_eurostat(publisher: str) -> bool:
    return publisher.strip().lower().startswith("eurostat")


def _eurostat_code(source: Mapping[str, Any]) -> str | None:
    """The code of a Eurostat dataset, from its link; Comext's link does not carry it."""
    if not _is_eurostat(source["name"]):
        return None
    if "comext" in source["name"].lower():
        return "DS-045409"
    found = re.search(r"/view/([A-Za-z0-9_]+)/", str(source["url"] or ""))
    return found.group(1) if found else None


def _cited_lines(cite: Iterable[tuple[str, str, str]], meta: Mapping[str, Any]) -> list[str]:
    """Citation lines for an answer that does not name its dataset, dated by the answer's own stamp."""
    day = _day(meta.get("last_updated")) or date.today().isoformat()
    lines = [f"Source: {publisher}, {code}, {link} (accessed {day})" for publisher, code, link in cite]
    if any(_is_eurostat(publisher) for publisher, _, _ in cite):
        lines.append("Own calculations based on Eurostat data. Eurostat is not responsible for these calculations.")
    return lines


def licence_lines(answer: Mapping[str, Any], already_cited: bool = False) -> list[str]:
    """What an answer says about its sources and conditions, as lines for the top of a file.

    Taken from the answer itself: its sources, each licence's credit, its notices and its notes.
    For figures calculated from Eurostat data it adds the wording Eurostat asks for.
    """
    meta = answer.get("meta") or {}
    lines: list[str] = []
    named: list[dict[str, Any]] = []

    def add_source(name: Any, dataset: Any, url: Any, day: Any, licence: Any = None) -> None:
        if name and not any(s["name"] == name and s["dataset"] == dataset for s in named):
            named.append({"name": str(name), "dataset": dataset, "url": url, "day": _day(day), "licence": licence})

    single = meta.get("source")
    if isinstance(single, Mapping):
        add_source(single.get("publisher"), single.get("dataset"), single.get("url"),
                   single.get("retrieved_at"), single.get("licence"))

    classes: set[str] = {str(meta["data_class"])} if meta.get("data_class") else set()
    credits_: list[str] = []
    for name, value in _walk(answer.get("data")):
        if name == "data_class" and value:
            classes.add(str(value))
        elif name == "sources" and isinstance(value, list):
            for item in value:
                if isinstance(item, Mapping) and item.get("name"):
                    add_source(item.get("name"), item.get("dataset_title"), item.get("url"), item.get("retrieved_at"))
        elif name == "source" and isinstance(value, Mapping) and value.get("publisher"):
            add_source(value.get("publisher"), value.get("dataset"), value.get("url") or value.get("dataset_url"),
                       value.get("retrieved_at") or value.get("last_retrieved_at"),
                       value.get("licence") or value.get("licence_name"))
        elif name in ("attribution", "notices", "modification_note", "not_legal_advice", "licence_requirement"):
            credits_.extend(_texts(value))

    for source in named:
        parts = [source["name"], _eurostat_code(source), source["dataset"], source["url"]]
        said = ", ".join(str(part) for part in parts if part)
        accessed = "accessed" if _is_eurostat(source["name"]) else "retrieved"
        said += f" ({accessed} {source['day']})" if source["day"] else ""
        said += f". Licence: {source['licence']}" if source["licence"] else ""
        lines.append(f"Source: {said}")
    notes = [str(note) for note in meta.get("notes") or []]
    if not named and not any(note.startswith("Sources:") for note in notes):
        lines.append(
            f"{'Other sources' if already_cited else 'Sources'}: this answer does not name them; "
            f"every source and its licence: {BASE_URL}/api/sources"
        )

    eurostat = [s for s in named if _is_eurostat(s["name"])]
    if eurostat and (classes & OWN_FIGURE_CLASSES or not classes):
        lines.append("Own calculations based on Eurostat data. Eurostat is not responsible for these calculations.")

    lines.extend(dict.fromkeys(credits_ + notes))
    text = json.dumps(answer.get("data"), ensure_ascii=False).lower()
    if "openstreetmap" in text and not any("Open Database License" in line for line in lines):
        lines.append(
            "Some coordinates are from OpenStreetMap: © OpenStreetMap contributors, available under the "
            "Open Database License (ODbL 1.0), https://www.openstreetmap.org/copyright"
        )
    return lines


def save_rows(
    route_id: str,
    rows: Iterable[Mapping[str, Any]],
    answer: Mapping[str, Any],
    own_bookkeeping: bool = False,
    cite: Iterable[tuple[str, str, str]] = (),
) -> None:
    """Write rows of a JSON answer as CSV, for a route that has no format=csv.

    Only routes whose every source allows redistribution do this (see README.md in this folder).
    The file starts with the same kind of # lines the API's own files carry: keep them.

    own_bookkeeping: the answer holds no publisher's figure, only what the API itself keeps.
    cite: (publisher, dataset code, link) for an answer that does not name its dataset.
    """
    flat = [flatten(row) for row in rows]
    columns = list(dict.fromkeys(column for row in flat for column in row))
    meta = answer.get("meta") or {}
    period = (meta.get("period") or {}).get("period")
    availability = answer.get("data_availability")
    availability = availability.get("status") if isinstance(availability, Mapping) else None
    preamble = [
        f"Fuel Origin, {route_id}",
        f"Endpoint: {_last_url}",
        f"Generated at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "Written from the API's JSON answer by fuelorigin-api-examples: this route has no format=csv, so the "
        "API's own check for files did not run on this file.",
        "Licence: Fuel Origin's own output is CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . "
        "Data from another publisher stays under that publisher's licence.",
        "Blank cell = not reported by the source. It is not zero.",
    ]
    if period:
        preamble.append(f"Period: {period}")
    if meta.get("confidence"):
        preamble.append(f"Confidence, the weakest in the answer: {meta['confidence']}")
    if meta.get("data_class"):
        preamble.append(f"Data class: {meta['data_class']}")
    if availability:
        preamble.append(f"Data availability: {availability}")
    if own_bookkeeping:
        preamble.append("Fuel Origin bookkeeping; no third-party measurements included.")
        preamble += [str(note) for note in meta.get("notes") or []]
    else:
        preamble += _cited_lines(cite, meta) + licence_lines(answer, bool(cite))

    target = _target(route_id)
    with target.open("w", encoding="utf-8", newline="") as file:
        for line in preamble:
            file.write("# " + " ".join(line.split()) + "\n")
        writer = csv.DictWriter(file, fieldnames=columns, lineterminator="\n", restval="")
        writer.writeheader()
        writer.writerows(flat)
    print(f"{target}: {_count(len(flat))}")
    if not flat:
        print("The answer held no rows for this selection. An empty list is an answer, not a zero.")
    pagination = answer.get("pagination") or {}
    if pagination.get("has_more"):
        print(
            f"The API holds {pagination.get('total')} rows for this selection; this file holds {len(flat)}. "
            f"Everything as files: {DATASETS_URL}"
        )
