# energy-import
Import electricity meter usage into graphite.

Since I have yet to find direct API access to my electricity provider's hourly usage reports, I can log in to their website and export the hourly usage data as an Excel spreadsheet. This script imports that data to Graphite.

Please excuse my (lack of) python skills...

The spreadsheet format that my electricity provider exports for hourly metered usage is:

| header (date)    | header (kWH) |
|------------------|--------------|
| 2019-09-17 12:00 | 0.666        |

The script will parse the Excel spreadsheet and import into the provided graphite server (default port 2003) into the metric `energy.household.total.watthours.count`.

Be sure to configure graphite with the correct retention policies so that aggregate values are summed accordingly.


## Installation

    pip3 install -U openpyxl

## Usage

    ./import_el.py /path/to/data.xlsx <graphite-server-ip-address>

