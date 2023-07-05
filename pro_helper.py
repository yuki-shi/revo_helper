#!/usr/bin/env python3

from database_manipulation import query_db, get_headers
import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-q',
                        '--query',
                        help='SQL query blablabla',
                        type=str)

    parser.add_argument('-s',
                        '--schema',
                        action='store_true',
                        help='Return table schema')

    args = parser.parse_args()

    if args.schema:
        print(get_headers())

    query_result = query_db(args.query)
    df = pd.DataFrame(query_result, columns=get_headers())
