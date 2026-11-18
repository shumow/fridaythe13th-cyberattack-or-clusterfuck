# Brief for Codex: a local copy of the GDELT news index

Written 18 November 2026 for a Codex session. It is self-contained: you do not need the rest of this repository to do it.

## What this is for

We are measuring how much U.S. news coverage of technology outages there was, day by day, from 17 August to 17 November 2026. The plan was to ask GDELT's search API (`api.gdeltproject.org/api/v2/doc/doc`). That API has refused every request with HTTP 429, from two different addresses, on the first request each time.

So we want the underlying records on our own disk instead. GDELT publishes its article-level index as bulk files every 15 minutes. Your job is to build a container that downloads those files for our date range, reduces them to a small queryable table, and leaves that table where another agent (Claude Code, running on the same Mac) can read it.

**You are building the data set, not doing the analysis.** Do not count, chart or summarise outage or cyberattack stories. The counting rules are pre-registered elsewhere and must be applied by someone who has not already looked. Sanity checks on row counts and on a neutral word are fine and are listed below.

## Hard rules

1. **Do not call the search API.** Nothing under `api.gdeltproject.org`. Bulk files only, from `data.gdeltproject.org`.
2. **Size first, download second.** Before downloading any data file, work out the total compressed size from the master file list and print it. If it is over **15 GB**, stop and report the figure instead of downloading. The owner expects roughly 10 GB and wants to know if that is wrong.
3. **Be a polite client.** At most 4 downloads at once, a descriptive `User-Agent` with no personal details, retry with backoff on failures, and never re-download a file that is already verified on disk.
4. **Every fact marked "verify" below is from memory.** Check it against GDELT's own documentation or the files themselves before relying on it, and list in your report anything that turned out different.
5. **Do not commit data to git.** Code and the report are committed; the data directory is ignored.

## Source data

GDELT 2.0 Global Knowledge Graph (GKG), English feed.

- Master file list: `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt`. One line per file: size in bytes, MD5, URL. (verify)
- Use only the lines whose URL ends in `.gkg.csv.zip`. File names are UTC timestamps, `YYYYMMDDHHMMSS.gkg.csv.zip`, one per 15 minutes. (verify)
- Do **not** use `masterfilelist-translation.txt`. That is the machine-translated feed; we want English-language sources only.
- Each file is one tab-separated table, no header, 27 columns, in the GKG 2.1 layout. (verify against the GKG 2.1 codebook, "GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf")

Columns we need, by position in the 2.1 layout (verify each):

| # | Codebook name | What we keep it as |
| --- | --- | --- |
| 1 | `GKGRECORDID` | `record_id` |
| 2 | `V2.1DATE` | `seen_utc` (timestamp) and `day_utc` (date) |
| 3 | `V2SOURCECOLLECTIONIDENTIFIER` | `source_collection` (1 means web) |
| 4 | `V2SOURCECOMMONNAME` | `domain` |
| 5 | `V2DOCUMENTIDENTIFIER` | `url` |
| 8 | `V1THEMES` | `themes` (semicolon-separated string, kept as is) |
| 27 | `V2EXTRASXML` | `title`, taken from the `<PAGE_TITLE>` element |

Everything else in the row is dropped. The files are not clean: expect bad UTF-8, stray tabs and the occasional short row. Do not crash on them. Count what you skip, per file.

### Source country

The search API's `sourcecountry:US` filter is based on where an outlet is published, not on what the article is about. GDELT has published a lookup from domain to country for this.

- Believed location: a file named like `MASTER-GDELTDOMAINSBYCOUNTRY-MAY2018.TXT` under `http://data.gdeltproject.org/blog/2018-news-outlets-by-country-may2018-update/`. (verify; find the newest version GDELT offers and say which you used)
- Join it to `domain` to fill `source_country`. Leave it null where the domain is not in the lookup. **Keep those rows**; do not drop them.

## Date range

- **Stage 1 (required):** every GKG file from `20260817000000` up to the newest one available when you run. Record that newest timestamp in the report. This is 93 days plus whatever has accrued, about 8,900 files.
- **Stage 2 (do not start without being asked):** selected earlier weeks back to November 2024. Design the downloader so that a later run can add any date range without redoing Stage 1, but do not fetch anything before 17 August 2026 in this session.

## What to build

A small project in its own directory, `gdelt-local/`, with:

- A `Dockerfile` and `compose.yaml`. Python and DuckDB are suggested; use what you like, but keep it boring.
- One host directory mounted as the data volume, `gdelt-local/data/`, ignored by git.
- Three commands, runnable as `docker compose run --rm gdelt <command>`:

| Command | What it does |
| --- | --- |
| `plan --from 20260817 [--to YYYYMMDD]` | Reads the master file list, prints file count and total compressed bytes for the range, downloads nothing. |
| `fetch --from 20260817 [--to YYYYMMDD]` | Downloads, verifies MD5 against the master list, extracts the columns above, writes Parquet, appends to the manifest. Resumable: safe to stop and rerun. |
| `check` | Prints the validation numbers listed under "Checks". |

Raw zips may be deleted once a file is verified and extracted, to stay inside the disk budget. The manifest is what proves they were fetched.

## Output contract

This is the part the other agent depends on. Please match it exactly.

```
gdelt-local/data/
  articles/day_utc=YYYY-MM-DD/part-*.parquet
  daily_totals.parquet
  manifest.csv
  domains_by_country.csv
  REPORT.md
```

**`articles`**: one row per GKG record in the English feed, all countries, nothing filtered out.

| Column | Type | Notes |
| --- | --- | --- |
| `record_id` | string | |
| `seen_utc` | timestamp | from `V2.1DATE`, UTC |
| `day_utc` | date | partition key |
| `source_collection` | int | |
| `domain` | string | lower-cased |
| `source_country` | string, nullable | from the lookup; say in the report which code system it uses |
| `url` | string | |
| `title` | string, nullable | from `<PAGE_TITLE>`, HTML entities decoded, whitespace collapsed, otherwise untouched |
| `themes` | string, nullable | as in the file |
| `src_file` | string | the 15-minute file it came from |

**`daily_totals`**: one row per UTC day, computed from the same rows: `day_utc`, `records_all`, `records_us`, `records_with_title`, `records_us_with_title`, `files_expected`, `files_present`. These are the denominators, so they must count every row before any later filtering.

**`manifest.csv`**: one row per source file: URL, bytes, MD5 expected, MD5 seen, time fetched (UTC), rows read, rows skipped as malformed, status. Include the files that failed or were missing from the master list, with a status that says so.

## Checks

`check` should print, and `REPORT.md` should record:

1. Files expected against files present, per day. List every missing 15-minute slot. A day should have 96.
2. Rows per day, all and U.S. Flag any day under half or over double the median.
3. Share of rows with a non-empty title, per day. If `<PAGE_TITLE>` is missing from most rows, stop and say so: the whole approach depends on it.
4. Share of rows whose domain is in the country lookup, and the twenty most frequent domains that are not.
5. Duplicate `url` values: how many rows, how many distinct URLs.
6. One neutral smoke test of the table: the daily count of titles containing the word `weather`, case-insensitive. This is only to show the table can be queried; do not run any other content query.
7. Total size of `data/` on disk, and the total compressed bytes downloaded.

## What to report back

Write `gdelt-local/data/REPORT.md` and also print it at the end. It should say:

- the newest file timestamp fetched, and the UTC time the run finished;
- total files, bytes downloaded, rows kept, size on disk;
- every "verify" item above: confirmed, or what was actually true;
- every gap: missing files, days with odd counts, malformed rows;
- the exact commands to rerun or extend the range;
- how another process on the same Mac reads the table, as one working example. For instance, from the host with DuckDB: `SELECT day_utc, count(*) FROM read_parquet('gdelt-local/data/articles/*/*.parquet', hive_partitioning=true) GROUP BY 1 ORDER BY 1;`

## Things we already know are limits

You do not need to fix these. Say so if you find they are worse than described.

- The bulk files carry a title, a URL and machine-assigned themes for each article, **not the article text**. The search API matched full text. Anything counted from this table is a headline-and-metadata measure and will be reported as a different instrument.
- A wire story carried by two hundred local sites is two hundred rows.
- The country lookup may be years old, so newer outlets will have no country.
- Whether the bulk feed and the search API cover exactly the same articles is not known.
