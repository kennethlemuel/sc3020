# SC3020-project-2

## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

- [TPC-H](https://www.tpc.org/tpch/) sample data files. Refer [here](https://tedamoh.com/en/blog/55-data-modeling/78-generating-large-example-data-with-tpc-h) for information on using the TPC-H tool dbgen.
- [PostgreSQL](https://www.postgresql.org/)

### Installation

#### Importing the TPC-H dataset into your PostgreSQL database

1. Navigate to the `/data` directory

```bash
cd data
```

2. Move your TPC-H .tbl files into the `/data` directory
3. If needed, run the `remove_trailing_delimiter.sh` script to remove trailing delimiters

```bash
./remove_trailing_delimiter.sh
```

4. Create a database with the name "TPC_H" on PostgreSQL if you have not done so.
5. Run the `init.pgsql` file to create tables and import data from the .tbl files into the PostgreSQL database. Replace `postgres` with your username if needed.

```bash
psql -U postgres -d TPC-H -a -f init.pgsql
```
