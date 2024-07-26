## NYC TLC Trip Record Analysis using Apache Spark

### Trial and Errors

- [Notion Link](https://patrashu.notion.site/Day-19-20-1f8edc725e804486a5de78e6ef4406ee?pvs=4)

### Makefile Usage (Docker Container)

- build and run container
    ```bash
    make up
    ```

- stop and remove container
    ```bash
    make down
    ```

- remove container with base image
    ```bash
    make down_all
    ```

- remove volume
    ```bash
    make down_volume
    ```


### Download TLC Trip dataset(csv, parquet)
```bash
bash download_trip_data.sh --data_format fhvhv --start_date 2023-01 --end_date 2023-01 --output_dir data
```

### Download weather dataset
```bash
bash download_weather_data.sh --start_year 2023 --end_year 2023 --output_dir data
```