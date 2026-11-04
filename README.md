# Fuel Origin API examples

Working examples for the [Fuel Origin](https://fuelorigin.org) API: a README you can copy from, one small Python script per route, and a notebook that plots Germany's crude oil origins.

The data behind fuelorigin.org, as JSON or CSV: where the crude oil and fuel of the EU member states, Switzerland, Norway, the United Kingdom, Greenland, Türkiye, Serbia, North Macedonia, Montenegro, Albania, Moldova, Georgia and the United States come from, pump prices and taxes, oil stocks and the Strait of Hormuz, with every value traceable to the publisher's record.

- **Base URL:** `https://api.fuelorigin.org`
- Read-only: every route is `GET`.
- Every data answer has the same envelope: the rows in `data`, then `meta` (period, sources, the weakest confidence in the answer, notes), `pagination` and `data_availability`.
- Data rows carry their `data_class`, their `confidence` and a `provenance_id` that leads to the publisher's record and the file downloaded.
- Missing is `null`, never `0`. A `0` is a published zero. An empty list is an answer, and `data_availability.status` says what it means.
- Documentation: <https://fuelorigin.org/developers>. Plans and keys: <https://fuelorigin.org/api-access>.

**Want everything rather than one selection?** Use the [datasets](https://fuelorigin.org/datasets). The scripts here make one request each, on purpose.

## What is in this repository

| Path | What it is |
|---|---|
| [`python/`](python/) | One runnable script per route in the API reference. Standard library only, Python 3.10+. Each writes `out/<route id>.csv`. |
| [`notebooks/germany_crude_origins.ipynb`](notebooks/germany_crude_origins.ipynb) | Pulls Germany's crude oil origins and plots them, saved with its real outputs. |
| [`LICENSE`](LICENSE) | MIT for the code, with a note on the data. |
| [`CITATION.cff`](CITATION.cff) | How to cite the dataset the code fetches. |

## Free or with a key

The table on [/api-access](https://fuelorigin.org/api-access), as it stood on 2026-11-04:

|  | Without a key | With a key |
|---|---|---|
| History | The last 24 months | Full history |
| Rows per read | At most 1,000 rows per read on most routes, so a long history is read window by window | No cap beyond the route's own: whole histories, up to 5,000 rows per page |
| Datasets for key holders | Not answered | Average cost of crude oil imports by crude grade; days of cover by product; the EU and UK rules on fuel refined from Russian crude oil (every change, a list on any date, one country over time, every text version) |
| Rate limit | Bursts of up to 120 requests per IP address, refilled at 2 per second | A plan's key has its own, set by the plan |
| Monthly allowance | None | A number of requests per calendar month, set by the plan |
| Sources and conditions | Each answer names its source | With a plan's key, each answer lists every publisher's dataset behind it, with its licence, its conditions for commercial use and the releases the values come from |
| Caching | Answers may come from our CDN | Private: never kept at our CDN |
| Reuse of our own output under CC BY 4.0 | Yes | Yes |

Reuse, also commercial, needs credit as the [terms](https://fuelorigin.org/terms#reusing-our-content) describe.

Your key goes in the header `X-API-Key`. The examples read it from an environment variable, `FO_KEY`: `export FO_KEY=...` in a Unix shell, `$env:FO_KEY="..."` in PowerShell. Never put it in a file you share. Evaluation keys are given on request: <contact@fuelorigin.org>.

## First requests

The snippets below are the ones on [/developers](https://fuelorigin.org/developers). Every answer shown was captured from the live API on **2026-11-04**, without a key, and is cut down where it says so. Nothing in them is composed.

### curl

Germany's crude oil imports by country of production, June 2026. This route also answers without a key: with `FO_KEY` unset, curl leaves the header out.

```sh
curl -s -H "X-API-Key: $FO_KEY" \
  "https://api.fuelorigin.org/api/countries/germany/crude-origins?from=2026-06-01&to=2026-06-30&limit=2"
```

The answer, cut down: both rows the request asked for, with 11 of their 27 fields plus `provenance_id` (value cut); `meta` and `data_availability` shortened; `pagination` in full.

```json
{"data": [
  {"country_slug": "germany", "origin_country_name": "United States of America", "basis": "energy", "period": "2026-06", "quantity_tonnes": 2138248.0, "share_pct": 31.144539785, "rank_in_period": 1, "status": "PARTIAL", "data_class": "CALCULATED", "confidence": "OFFICIAL", "calculation_version": "crude_origin_v1@energy_nrg_ti_oilm", "provenance_id": "…", …},
  {"country_slug": "germany", "origin_country_name": "Kazakhstan", "basis": "energy", "period": "2026-06", "quantity_tonnes": 1116312.0, "share_pct": 16.2595842468, "rank_in_period": 2, "status": "PARTIAL", "data_class": "CALCULATED", "confidence": "OFFICIAL", "calculation_version": "crude_origin_v1@energy_nrg_ti_oilm", "provenance_id": "…", …}],
 "meta": {"period": "2026-06", …, "source": {"publisher": "Eurostat (European Commission)", "dataset_id": "nrg_ti_oilm", "url": "https://ec.europa.eu/eurostat/databrowser/view/nrg_ti_oilm/default/table?lang=en", "licence": "Commission Decision 2011/833/EU - reuse authorised with attribution", "retrieved_at": "2026-11-04T03:03:08.299756Z"},
  "confidence": "OFFICIAL", "data_class": "CALCULATED", "notes": ["Basis: energy. Rows on the other basis are excluded, not merged.", …]},
 "pagination": {"limit": 2, "offset": 0, "returned": 2, "total": 25, "has_more": true},
 "data_availability": {"status": "HELD", …}}
```

`status: PARTIAL` on an origin row says the named partners fall short of the month's published total (the rest is served on `basis=unknown`); it is the same on every partner row of that month.

### Python

With `requests`: Eurostat's average CIF cost of Germany's crude imports, all crudes. This route is for key holders.

```python
import os, requests
BASE = "https://api.fuelorigin.org"
s = requests.Session()
s.headers["X-API-Key"] = os.environ["FO_KEY"]
r = s.get(f"{BASE}/api/crude-import-cost",
          params={"country": "DE", "grade": "TOTAL",
                  "indicator": "AVGPRC_USD_BBL", "from": "2026-01-01"},
          timeout=60)
r.raise_for_status()
body = r.json()
for row in body["data"]:
    print(row["period"], row["price_usd_per_bbl"], row["source_record_id"])
```

**Not captured here: these examples were run without a key.** Without `FO_KEY` this snippet stops at `os.environ["FO_KEY"]`, before any request. Without a key the same address answers:

```
404 {"detail":"Not Found"}
```

According to /developers it prints one line per month: the period, the price in US dollars per barrel and the Eurostat cell the value comes from.

The same pattern on a route that needs no key (Germany's weekly diesel price; run on 2026-11-04):

```python
import requests

BASE = "https://api.fuelorigin.org"
s = requests.Session()
s.headers["User-Agent"] = "fuelorigin-api-examples"
r = s.get(f"{BASE}/api/countries/germany/prices",
          params={"fuel": "DIESEL", "from": "2026-10-01"},
          timeout=60)
r.raise_for_status()
body = r.json()
for row in body["data"]:
    print(row["period"], row["price_incl_tax_eur_per_litre"], row["source_record_id"])
```

Its output in full:

```
2026-09-28 2.437 history_workbook|Prices with taxes|2026-09-28|DE_|diesel
2026-10-05 2.254 history_workbook|Prices with taxes|2026-10-05|DE_|diesel
2026-10-12 2.27 history_workbook|Prices with taxes|2026-10-12|DE_|diesel
2026-10-19 2.266 history_workbook|Prices with taxes|2026-10-19|DE_|diesel
2026-10-26 2.298 history_workbook|Prices with taxes|2026-10-26|DE_|diesel
```

The prices are euros per litre, tax included, weekly, from the European Commission's Weekly Oil Bulletin.

### Excel (Power Query)

Data > Get Data > From Other Sources > Blank Query > Advanced Editor, paste, replace `YOUR-KEY`. It reads the CSV form and drops the `#` lines at the top; keep those elsewhere, they carry the citation and the conditions. The key is stored inside the workbook: do not share a workbook that contains it. /developers says this was tested in Excel for Windows on 2026-10-11.

```
let
    Raw = Web.Contents("https://api.fuelorigin.org/api/stock-cover-by-product",
        [Query = [country = "EE", product = "ROAD_DIESEL", basis = "EMERGENCY",
                  from = "2026-01-01", limit = "5000", format = "csv"],
         Headers = [#"X-API-Key" = "YOUR-KEY"]]),
    Lines = Lines.FromBinary(Raw, null, null, 65001),
    DataLines = List.Select(Lines, each not Text.StartsWith(_, "#")),
    Table = Csv.Document(Text.Combine(DataLines, "#(lf)"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Table, [PromoteAllScalars = true])
in
    Promoted
```

**Not captured here: the route is for key holders.** Without a key the same address answers:

```
404 {"detail":"Not Found"}
```

The same query on a route that needs no key. It has **not** been run in Excel; what follows it is the real file it reads.

```
let
    Raw = Web.Contents("https://api.fuelorigin.org/api/countries/germany/crude-origins",
        [Query = [from = "2026-06-01", to = "2026-06-30", limit = "3", format = "csv"]]),
    Lines = Lines.FromBinary(Raw, null, null, 65001),
    DataLines = List.Select(Lines, each not Text.StartsWith(_, "#")),
    Table = Csv.Document(Text.Combine(DataLines, "#(lf)"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Table, [PromoteAllScalars = true])
in
    Promoted
```

The file, captured with curl on 2026-11-04, cut down: all its `#` lines, the 3 rows the request asked for, 7 of 29 columns.

```
# Without an API key the API answers periods that end on or after 2024-11-01. Full history needs an API key: https://fuelorigin.org/api-access
# Fuel Origin — Crude import origins — germany (energy basis)
# Endpoint: /api/countries/germany/crude-origins
# Generated at: 2026-11-04T09:38:27.091473+00:00
# Sources: eurostat_nrg_ti_oilm
# Licence: Every contributing source permits redistribution.
# Blank cell = not reported by the source. It is not zero.
# Condition (eurostat_citation): Source: Eurostat, nrg_ti_oilm (accessed 2026-11-04).
# Condition (eurostat_own_calculation): Own calculations based on Eurostat data. Eurostat is not responsible for these calculations.
period,origin_country_name,quantity_tonnes,share_pct,status,data_class,confidence
2026-06,United States of America,2138248.000,31.1445397850,PARTIAL,CALCULATED,OFFICIAL
2026-06,Kazakhstan,1116312.000,16.2595842468,PARTIAL,CALCULATED,OFFICIAL
2026-06,Norway,734331.000,10.6958599025,PARTIAL,CALCULATED,OFFICIAL
```

## When the API says no

**403: this read is refused, and retrying will not help.** The body has a sentence saying why. Two kinds matter here:

- A CSV download is redistribution, and the licence gate can refuse one while the JSON of the same request stays readable. A publisher's licence may not allow it, or the source behind the rows may not be established; an unestablished licence counts as a no. Captured on 2026-11-04 from `/api/countries?covered_only=true&format=csv`:

  ```
  403 {"detail": "This download is not available because the run that produced these values does not record which sources contributed to them, so we cannot check whether their licences permit redistribution. This affects calculated series, whose inputs come from several publishers at once. We treat an unestablished licence as a no, not as a yes. The numbers are readable as JSON from this endpoint without the format=csv parameter, and each row carries the identifiers needed to trace it through /api/provenance."}
  ```

- A read larger than the route's cap for callers without a key. Captured on 2026-11-04 from `/api/countries/germany/crude-origins?limit=1500`:

  ```
  403 {"detail": "Without an API key this endpoint serves at most 1000 rows per request (limit). Ask for a shorter window. Larger reads need an API key (header X-API-Key)."}
  ```

The scripts here print that sentence and exit with a non-zero status. They never rebuild a refused file from the JSON. Please don't either. Each source's own page is linked from [`/api/sources`](https://api.fuelorigin.org/api/sources).

**429: too many requests.** The answer has `Retry-After` in seconds. Without a key the limit is per IP address, bursts of up to 120 requests refilled at 2 per second (the table above). A plan's key also has a monthly allowance. No 429 was met while writing this, so none is shown. The scripts print the wait and stop; they do not retry.

**404 on a route for key holders** means no key was sent, and **401** means the key is not one the API knows: `{"detail":"Unknown API key."}`, never a smaller answer that looks complete.

## Licence

The code here is MIT ([`LICENSE`](LICENSE)). That covers the code only, not the data it fetches. Fuel Origin's own output is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data from another publisher stays under that publisher's licence, named per row: each row names its source, and `sources.csv` in the [datasets](https://fuelorigin.org/datasets) gives that source's licence and conditions. The [terms](https://fuelorigin.org/terms#reusing-our-content) say how to credit it.

A CSV from the API starts with `#` lines that carry its sources and conditions. Keep them.

For figures calculated from Eurostat data the wording is exactly `Own calculations based on Eurostat data.`, with a citation of Eurostat: the dataset code, its link and the access date. The files and the notebook here carry it.

## How to cite

The dataset the code fetches, every version: DOI [10.5281/zenodo.23940619](https://doi.org/10.5281/zenodo.23940619). GitHub reads the same from [`CITATION.cff`](CITATION.cff).

> Fuel Origin: European oil supply data, https://fuelorigin.org/datasets, https://doi.org/10.5281/zenodo.23940619.

## Where else

- Datasets: <https://fuelorigin.org/datasets>
- Zenodo: <https://zenodo.org/records/23940620>
- Hugging Face: <https://huggingface.co/datasets/fuelorigin/fuel-origin-eu-oil-data>
- Kaggle: <https://www.kaggle.com/datasets/marioypr/eu-crude-oil-imports-by-origin-20152026>
- Documentation: <https://fuelorigin.org/developers>
- API and data access: <https://fuelorigin.org/api-access>
- Contact: <contact@fuelorigin.org>
