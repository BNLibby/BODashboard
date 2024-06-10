
# Imports
from ercotapi import ERCOTAPI
from ercotapi import USERNAME
from ercotapi import PASSWORD
from ercotapi import API_KEY
from pandas import DataFrame
from streamlit import cache_data, header, subheader, table, button, download_button
import datetime as dt

# Variable To Access API
API_CONNECTION = ERCOTAPI(USERNAME, PASSWORD, API_KEY)

# Reset API Connection Every Hour
def set_api_access():
    API_CONNECTION.set_api_connection()
    return None

# Get DAM SPP
def get_dam_spp():
    set_api_access()
    data = API_CONNECTION.get_json_dict(API_CONNECTION.get_dam_spp(deliveryDateFrom=str(dt.date.today()), deliveryDateTo=str(dt.date.today()), settlementPoint="HB_WEST"))["data"]
    data = DataFrame(data=data, columns=["Date", "Hour", "Settlement Point", "SPP", "Repeat Flag"])
    data["Hour"] = [int(x[:-3]) for x in data["Hour"]]
    data.drop("Repeat Flag", inplace=True, axis=1)
    return data

@cache_data
def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

spp_df = get_dam_spp()

header("West Hub DAM SPP Downloader")
subheader("Currently Showing Data For: " + str(spp_df["Date"].iloc[0]))
table(spp_df)
button("Refresh Data", on_click=get_dam_spp)
download_button(
  label="Download data as CSV",
  data=convert_df_to_csv(spp_df),
  file_name="HB_WEST_SPP_" + str(spp_df["Date"].iloc[0]) + ".csv",
  mime='text/csv',
)