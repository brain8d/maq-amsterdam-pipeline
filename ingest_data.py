from sqlalchemy import create_engine
import pandas as pd 
import argparse

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    #url = params.url
    data = params.data

    # Create engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Convert to pandas and check data 
    df = pd.read_csv(data)
    drops= ["air_pressure", "RH", "wind_speed", "wind_dir"]
    df = df.drop(columns = drops)

    # drop first row that contains extra  names
    df = df.iloc[1:,]

    # Set up correct dtypes
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.astype({'Qs_in_Avg': 'float'})
    df = df.astype({'T1_Avg': 'float'})

    # # Creating just the table in postgres
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--data', required=True, help="file path")
    #parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)