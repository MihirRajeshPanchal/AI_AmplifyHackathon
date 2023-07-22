import streamlit as st
import pandas as pd
import json 
from Cloud_Backend.dynamodb import upload_dynamodb_details
import requests

st.set_page_config(
    page_title="Surf",
    page_icon="assets/logo.jpeg",
)

st.sidebar.title("Surf")
df = pd.read_csv("superstore.csv", encoding="ISO-8859-1")

# Assuming the JSON file contains a dictionary with keys corresponding to widget names
def update_sidebar_values_from_json(json_content):
    if "Order Date" in json_content:
        st.sidebar.date_input("Order Date", value=pd.to_datetime(json_content["Order Date"]))

    if "Ship Date" in json_content:
        st.sidebar.date_input("Ship Date", value=pd.to_datetime(json_content["Ship Date"]))

    if "Ship Mode" in json_content:
        st.sidebar.selectbox("Ship Mode", df["Ship Mode"].unique(), index=df["Ship Mode"].unique().tolist().index(json_content["Ship Mode"]))

    if "Segment" in json_content:
        st.sidebar.selectbox("Segment", df["Segment"].unique(), index=df["Segment"].unique().tolist().index(json_content["Segment"]))

    if "Country" in json_content:
        st.sidebar.selectbox("Country", df["Country"].unique(), index=df["Country"].unique().tolist().index(json_content["Country"]))

    if "City" in json_content:
        st.sidebar.selectbox("City", df["City"].unique(), index=df["City"].unique().tolist().index(json_content["City"]))

    if "State" in json_content:
        st.sidebar.selectbox("State", df["State"].unique(), index=df["State"].unique().tolist().index(json_content["State"]))

    if "Region" in json_content:
        st.sidebar.selectbox("Region", df["Region"].unique(), index=df["Region"].unique().tolist().index(json_content["Region"]))

    if "Category" in json_content:
        st.sidebar.selectbox("Category", df["Category"].unique(), index=df["Category"].unique().tolist().index(json_content["Category"]))

    if "Sub-Category" in json_content:
        st.sidebar.selectbox("Sub-Category", df["Sub-Category"].unique(), index=df["Sub-Category"].unique().tolist().index(json_content["Sub-Category"]))

    if "Product Name" in json_content:
        st.sidebar.selectbox("Product Name", df["Product Name"].unique(), index=df["Product Name"].unique().tolist().index(json_content["Product Name"]))

    if "Quantity" in json_content:
        st.sidebar.number_input("Quantity", min_value=0, max_value=1000, value=json_content["Quantity"])

    if "Discount" in json_content:
        st.sidebar.number_input("Discount", min_value=0, max_value=100, value=json_content["Discount"])

    if "Profit" in json_content:
        st.sidebar.number_input("Profit", min_value=0, max_value=100000, value=json_content["Profit"])

uploaded_file = st.file_uploader("Upload a JSON file", type="json")

flag = 0
if uploaded_file is not None:
    json_content = json.load(uploaded_file)
    print(json_content)
    flag = 1
    update_sidebar_values_from_json(json_content)

if flag == 0:
    order_Date = st.sidebar.date_input("Order Date", value=pd.to_datetime("today"))
    ship_date = st.sidebar.date_input("Ship Date", value=pd.to_datetime("today"))
    ship_mode = st.sidebar.selectbox("Ship Mode", df["Ship Mode"].unique())
    segment = st.sidebar.selectbox("Segment", df["Segment"].unique())
    country = st.sidebar.selectbox("Country", df["Country"].unique())
    city = st.sidebar.selectbox("City", df["City"].unique())
    state = st.sidebar.selectbox("State", df["State"].unique())
    region = st.sidebar.selectbox("Region", df["Region"].unique())
    category = st.sidebar.selectbox("Category", df["Category"].unique())
    sub_category = st.sidebar.selectbox("Sub-Category", df["Sub-Category"].unique())
    product_name = st.sidebar.selectbox("Product Name", df["Product Name"].unique())
    quantity = st.sidebar.number_input("Quantity", min_value=0, max_value=1000, value=0)
    discount = st.sidebar.number_input("Discount", min_value=0, max_value=100, value=0)
    profit = st.sidebar.number_input("Profit", min_value=0, max_value=100000, value=0)




if st.button("Predict"):
    data_to_predict = {
        "Order Date": str(order_Date),
        "Ship Date": str(ship_date),
        "Ship Mode": ship_mode,
        "Category": category,
        "Sub-Category": sub_category,
        "Product Name": product_name,
        "Quantity": quantity,
        "Profit": profit
    }

    # Convert the data to a JSON string
    json_data = json.dumps([data_to_predict])

    # Make the API request using requests library
    api_url = 'https://api.akkio.com/api'
    flow_key = 'oyw8MjvKbbub0nNTl7pP/1'
    api_key = '08bac0c7-438e-498a-a586-29931a105e95'

    payload = {
        'flow_key': flow_key,
        'api_key': api_key,
        'data': json_data
    }

    response = requests.get(api_url, params=payload)

    # Check if the API request was successful
    if response.status_code == 200:
        st.write("Prediction results:")
        prediction_results = response.json()
        sales_value = prediction_results[0]["Sales"]
        st.write("Sales Prediced: ", sales_value)
    else:
        st.write("Error making API request:", response.status_code, response.text)
    

    
st.title("Analysis")

st.title("Line Charts")
x_axis_line = st.selectbox("X-Axis", df.columns,key="x_axis_line")
y_axis_line = st.selectbox("Y-Axis", df.columns,key="y_axis_line")
st.line_chart(data=df, x=x_axis_line, y=y_axis_line, width=0, height=0, use_container_width=True)


st.title("Area Charts")
x_axis_area = st.selectbox("X-Axis", df.columns,key="x_axis_area")
y_axis_area = st.selectbox("Y-Axis", df.columns,key="y_axis_area")
st.area_chart(data=df, x=x_axis_area, y=y_axis_area, width=0, height=0, use_container_width=True)
    
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 