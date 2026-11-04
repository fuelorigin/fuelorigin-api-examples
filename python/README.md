# One script per route

62 scripts, one for every route in the [API reference](https://fuelorigin.org/developers/reference). No route is left out. Standard library only, Python 3.10+: nothing to install.

```sh
python countries_slug_crude_origins.py
python countries_slug_crude_origins.py --slug france --from 2026-01-01
python countries_slug_crude_origins.py --help
```

Each one makes **one request**, for one sensible default selection (Germany, usually, and a recent window), and writes `out/<route id>.csv` under the folder you run it from. The scripts share [`fuelorigin.py`](fuelorigin.py). There are no loops over countries or months, no retries and no concurrency, and please keep it that way in what you build on them: the free API is for page-sized reads. For everything, use the [datasets](https://fuelorigin.org/datasets).

**Key.** Read from the environment variable `FO_KEY`, sent as the `X-API-Key` header, never an argument and never stored. A script for a route for key holders says so and stops, without calling the API, when there is no key.

**Exit status.** 0 written; 1 another failure; 2 no key on a route for key holders; 3 the API refused (403); 4 too many requests (429).

## Two kinds of script

**The API's own CSV (27 routes).** The script asks for `format=csv` and writes the file byte for byte, `#` lines included. Those lines carry the sources and the conditions: keep them. On a 403 it prints the API's reason and exits. It never falls back to the JSON.

**From the JSON (35 routes).** These routes have no `format` parameter: they answer a page-shaped object, not a list. The script picks the natural table, one row per thing, with nested objects as `a.b` columns and lists as JSON text in one cell. Some leave part of the answer out; each script's docstring says which. A route is written this way only because, on 2026-11-04, every source its answer can draw on was recorded as allowing redistribution in [`/api/sources`](https://api.fuelorigin.org/api/sources) (`redistribution_allowed`). The API's check for files does not run on such a file, and the first lines of the file say so. They also carry what the answer says about sources, credits and conditions. A source's status can change: check `/api/sources` if you reuse an old file.

Three of these answers do not name their datasets (`overview_summary.py`, `statistics_line_index.py`, `suppliers_summary.py`). Their scripts cite Eurostat's `nrg_ti_oilm` in the file's first lines, dated by the answer's own `last_updated` where it has one, and point to `/api/sources` for the rest.

## Results of the run on 2026-11-04

Every script that needs no key was run once against the live API, without a key, spaced a few seconds apart, with its default selection. Row counts are from that day and will change.

| Script | Route | CSV | Result |
|---|---|---|---|
| [`account_usage.py`](account_usage.py) | `/api/account/usage` | from JSON | not run against the live API (no key); tested against a local stub |
| [`benchmarks_code.py`](benchmarks_code.py) | `/api/benchmarks/{code}` | API's CSV | 200, 61 rows |
| [`compare.py`](compare.py) | `/api/compare` | from JSON | 200, 3 rows |
| [`corrections.py`](corrections.py) | `/api/corrections` | API's CSV | 200, 100 rows |
| [`countries.py`](countries.py) | `/api/countries` | API's CSV | 200, 241 rows |
| [`countries_slug.py`](countries_slug.py) | `/api/countries/{slug}` | from JSON | 200, 10 rows |
| [`countries_slug_crude_only.py`](countries_slug_crude_only.py) | `/api/countries/{slug}/crude-only` | from JSON | 200, 104 rows |
| [`countries_slug_crude_origins.py`](countries_slug_crude_origins.py) | `/api/countries/{slug}/crude-origins` | API's CSV | 200, 228 rows |
| [`countries_slug_fuel_chain.py`](countries_slug_fuel_chain.py) | `/api/countries/{slug}/fuel-chain` | from JSON | 200, 47 rows |
| [`countries_slug_hormuz.py`](countries_slug_hormuz.py) | `/api/countries/{slug}/hormuz` | API's CSV | 200, 11 rows |
| [`countries_slug_inventory.py`](countries_slug_inventory.py) | `/api/countries/{slug}/inventory` | API's CSV | 200, 10 rows |
| [`countries_slug_lag.py`](countries_slug_lag.py) | `/api/countries/{slug}/lag` | API's CSV | 200, 1 row |
| [`countries_slug_overview.py`](countries_slug_overview.py) | `/api/countries/{slug}/overview` | from JSON | 200, 6 rows |
| [`countries_slug_pass_through.py`](countries_slug_pass_through.py) | `/api/countries/{slug}/pass-through` | API's CSV | 200, 1 row |
| [`countries_slug_price_decomposition.py`](countries_slug_price_decomposition.py) | `/api/countries/{slug}/price-decomposition` | API's CSV | 200, 27 rows |
| [`countries_slug_prices.py`](countries_slug_prices.py) | `/api/countries/{slug}/prices` | API's CSV | 200, 27 rows |
| [`countries_slug_product_origins.py`](countries_slug_product_origins.py) | `/api/countries/{slug}/product-origins` | API's CSV | 200, 106 rows |
| [`countries_slug_refineries.py`](countries_slug_refineries.py) | `/api/countries/{slug}/refineries` | API's CSV | 200, 14 rows |
| [`countries_slug_taxes.py`](countries_slug_taxes.py) | `/api/countries/{slug}/taxes` | API's CSV | 200, 11 rows |
| [`crude_import_cost.py`](crude_import_cost.py) | `/api/crude-import-cost` | API's CSV | not run against the live API (no key); tested against a local stub |
| [`data_updates.py`](data_updates.py) | `/api/data-updates` | from JSON | 200, 21 rows |
| [`datasets.py`](datasets.py) | `/api/datasets` | from JSON | 200, 10 rows |
| [`events.py`](events.py) | `/api/events` | API's CSV | 200, 14 rows |
| [`events_slug.py`](events_slug.py) | `/api/events/{slug}` | from JSON | 200, 542 rows |
| [`events_slug_crude_only.py`](events_slug_crude_only.py) | `/api/events/{slug}/crude-only` | from JSON | 200, 18 rows |
| [`events_slug_statements.py`](events_slug_statements.py) | `/api/events/{slug}/statements` | API's CSV | 200, 28 rows |
| [`events_slug_study.py`](events_slug_study.py) | `/api/events/{slug}/study` | API's CSV | 200, 377 rows |
| [`flows_country_slug.py`](flows_country_slug.py) | `/api/flows/country/{slug}` | API's CSV | 200, 86 rows |
| [`flows_eu.py`](flows_eu.py) | `/api/flows/eu` | API's CSV | 200, 160 rows |
| [`flows_importer_slug.py`](flows_importer_slug.py) | `/api/flows/importer/{slug}` | API's CSV | 200, 8 rows |
| [`hormuz_overview.py`](hormuz_overview.py) | `/api/hormuz-overview` | from JSON | 200, 27 rows |
| [`hormuz_indirect_supply.py`](hormuz_indirect_supply.py) | `/api/hormuz/indirect-supply` | from JSON | 200, 81 rows |
| [`landing_countries_slug_oil_imports.py`](landing_countries_slug_oil_imports.py) | `/api/landing/countries/{slug}/oil-imports` | from JSON | 200, 31 rows |
| [`landing_eu_crude_sources.py`](landing_eu_crude_sources.py) | `/api/landing/eu-crude-sources` | from JSON | 200, 39 rows |
| [`landing_eu_pump_prices.py`](landing_eu_pump_prices.py) | `/api/landing/eu-pump-prices` | from JSON | 200, 54 rows |
| [`map_flows.py`](map_flows.py) | `/api/map/flows` | from JSON | 200, 156 rows |
| [`map_layers.py`](map_layers.py) | `/api/map/layers` | from JSON | 200, 485 rows |
| [`margins_proxy.py`](margins_proxy.py) | `/api/margins/proxy` | API's CSV | 200, 27 rows |
| [`network.py`](network.py) | `/api/network` | from JSON | 200, 121 rows |
| [`origins.py`](origins.py) | `/api/origins` | API's CSV | 200, 136 rows |
| [`origins_slug.py`](origins_slug.py) | `/api/origins/{slug}` | API's CSV | 200, 330 rows |
| [`overview_summary.py`](overview_summary.py) | `/api/overview-summary` | from JSON | 200, 27 rows |
| [`provenance_observation_id.py`](provenance_observation_id.py) | `/api/provenance/{observation_id}` | from JSON | 200, 1 row |
| [`refineries.py`](refineries.py) | `/api/refineries` | API's CSV | 200, 14 rows |
| [`refineries_slug.py`](refineries_slug.py) | `/api/refineries/{slug}` | from JSON | 200, 1 row |
| [`refineries_slug_profile.py`](refineries_slug_profile.py) | `/api/refineries/{slug}/profile` | from JSON | 200, 1 row |
| [`rules_changes.py`](rules_changes.py) | `/api/rules/changes` | API's CSV | not run against the live API (no key); tested against a local stub |
| [`rules_countries_iso2.py`](rules_countries_iso2.py) | `/api/rules/countries/{iso2}` | from JSON | not run against the live API (no key); tested against a local stub |
| [`rules_documents_document_key_versions.py`](rules_documents_document_key_versions.py) | `/api/rules/documents/{document_key}/versions` | from JSON | not run against the live API (no key); tested against a local stub |
| [`rules_lists_list_code.py`](rules_lists_list_code.py) | `/api/rules/lists/{list_code}` | from JSON | not run against the live API (no key); tested against a local stub |
| [`rules_refined_from_russian_crude.py`](rules_refined_from_russian_crude.py) | `/api/rules/refined-from-russian-crude` | from JSON | 200, 63 rows |
| [`sources.py`](sources.py) | `/api/sources` | API's CSV | 200, 109 rows |
| [`sources_source_id.py`](sources_source_id.py) | `/api/sources/{source_id}` | from JSON | 200, 1 row |
| [`station_prices_slug.py`](station_prices_slug.py) | `/api/station-prices/{slug}` | from JSON | 200, 95 rows |
| [`statistics_eu_crude_oil_imports_months.py`](statistics_eu_crude_oil_imports_months.py) | `/api/statistics/eu-crude-oil-imports/months` | from JSON | 200, 19 rows |
| [`statistics_eu_crude_oil_imports_months_period.py`](statistics_eu_crude_oil_imports_months_period.py) | `/api/statistics/eu-crude-oil-imports/months/{period}` | from JSON | 200, 27 rows |
| [`statistics_line_index.py`](statistics_line_index.py) | `/api/statistics/line-index` | from JSON | 200, 140 rows |
| [`statistics_slug.py`](statistics_slug.py) | `/api/statistics/{slug}` | from JSON | 200, 23 rows |
| [`stock_cover_by_product.py`](stock_cover_by_product.py) | `/api/stock-cover-by-product` | API's CSV | not run against the live API (no key); tested against a local stub |
| [`suppliers_summary.py`](suppliers_summary.py) | `/api/suppliers-summary` | from JSON | 200, 109 rows |
| [`voyages.py`](voyages.py) | `/api/voyages` | from JSON | 200, 5 rows |
| [`health.py`](health.py) | `/health` | from JSON | 200, 2 rows |

**Not run against the live API:** the 7 scripts for key holders above. Their answers were checked only for shape, against a local stub built from the published reference: writing a file, keeping the `#` lines, sending the key only as a header.

**Refusals.** A selection with nothing in it answers 403, for example `countries_slug_crude_origins.py --slug greenland`. The script prints the API's reason and stops. No public file was refused on licence on 2026-11-04.

**Not checked.** Each script's other options and the example in its docstring were not all run: only the default selection was.
