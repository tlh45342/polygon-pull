import datetime
import os
import pandas
from polygon.rest.client import RESTClient

def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


def pull_day(Symbol, from_):

    POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')

    enddate = datetime.datetime.fromisoformat(from_)
    enddate += datetime.timedelta(days=1)
    enddate = str(enddate)[0:10]
  
    with RESTClient(POLYGON_API_KEY) as client:

        resp = client.stocks_equities_aggregates(Symbol, 1, "minute", from_, enddate, unadjusted=False)

        #print(f"Minute aggregates for {resp.ticker} between {from_} and {enddate}.")

        out = {}
        df = pandas.DataFrame(out, columns = ['Datetime', 'Open', 'High', 'Low','Close','Adj Close','Volume'])  

        for result in resp.results:
            #dt = ts_to_datetime(result["t"])
            #print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
            date = {"Datetime": result['t']}
            open = {"Open": result['o']}
            high = {"High": result['h']}
            low = {"Low": result['l']}
            close = {"Close": result['c']}
            volume = {"Volume": result['v']}
            bar = {**date, **open, **high, **low, **close, **volume}
            df = df.append(bar,ignore_index=True)

    return(df)

# ----------------------------
  
daystr  = "2021-09-10"
df = pull_day("LC", daystr)
fname = r"M:\data\out.csv"
print("Writing: ", fname)
df.to_csv (fname, index = False, header=True)