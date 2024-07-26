#!/bin/bash

# Function to check if date is in the format YYYY-MM
is_valid_date() {
    case $1 in
        ????-??) if echo "$1" | grep -Eq "^[0-9]{4}-(0[1-9]|1[0-2])$"; then
                    return 0
                 else
                    return 1
                 fi ;;
        *) return 1 ;;
    esac
}

# Function to split year and month
split_date() {
    year=${1%%-*}
    month=${1##*-}
}

# Download function
download() {
    data=$1
    year=$2
    month=$3
    output_dir=$4
    url="https://d37ci6vzurychx.cloudfront.net/trip-data/${data}_tripdata_${year}-$(printf "%02d" $month).parquet"
    echo "Downloading $url to $output_dir"
    wget -P "$output_dir" "$url"
}

# Input parameters
data_format="fhvhv"
start_date="2023-01"
end_date="2023-02"
output_dir="data"

# Parse command line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --data_format) data_format="$2"; shift 2;;
    --start_date) start_date="$2"; shift 2;;
    --end_date) end_date="$2"; shift 2;;
    --output_dir) output_dir="$2"; shift 2;;
    *) echo "Unknown parameter passed: $1"; exit 1;;
  esac
done

# Validate input dates
if ! is_valid_date "$start_date"; then
    echo "Start date is not in the correct format (YYYY-MM)"
    exit 1
fi

if ! is_valid_date "$end_date"; then
    echo "End date is not in the correct format (YYYY-MM)"
    exit 1
fi

# Split start and end dates
split_date "$start_date"
start_year=$year
start_month=$month

split_date "$end_date"
end_year=$year
end_month=$month

# Create output directory if it doesn't exist
if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
fi

# Loop through each month from start_date to end_date
current_year=$start_year
current_month=$start_month

while [ "$current_year" -lt "$end_year" ] || ([ "$current_year" -eq "$end_year" ] && [ "$current_month" -le "$end_month" ]); do
  download "$data_format" "$current_year" "$current_month" "$output_dir"
  if [ "$current_month" -eq 12 ]; then
    current_month=1
    current_year=$((current_year + 1))
  else
    current_month=$((current_month + 1))
  fi
done
