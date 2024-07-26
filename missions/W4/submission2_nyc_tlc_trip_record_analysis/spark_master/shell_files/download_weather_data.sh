#!/bin/bash

# Function to check if date is in the format YYYY
is_valid_date() {
    case $1 in
        ????) if echo "$1" | grep -Eq "^[0-9]{4}$"; then
                return 0
              else
                return 1
              fi ;;
        *) return 1 ;;
    esac
}

# Download function
download() {
    year=$1
    output_dir=$2
    url="https://www.ncei.noaa.gov/data/global-hourly/archive/csv/${year}.tar.gz"
    echo "Downloading $url to $output_dir"
    wget -P "$output_dir" "$url"
}

# Input parameters
start_year="2023"
end_year="2023"
output_dir="data"

# Parse command line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --start_year) start_year="$2"; shift 2;;
    --end_year) end_year="$2"; shift 2;;
    --output_dir) output_dir="$2"; shift 2;;
    *) echo "Unknown parameter passed: $1"; exit 1;;
  esac
done

# Validate input dates
if ! is_valid_date "$start_year"; then
    echo "Start year is not in the correct format (YYYY)"
    exit 1
fi

if ! is_valid_date "$end_year"; then
    echo "End year is not in the correct format (YYYY)"
    exit 1
fi

# Create output directory if it doesn't exist
if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
fi

# Loop through each year from start_year to end_year
current_year=$start_year

while [ "$current_year" -le "$end_year" ]; do
  download "$current_year" "$output_dir"
  current_year=$((current_year + 1))
done
