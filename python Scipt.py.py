from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

import uvicorn
app = FastAPI()

print("HERE!! started FAST API")


countries_info = pd.read_csv('/Users/mohammed5.asif/Downloads/Customer-Rating-System-Datasets/countries_info.csv')
cust_acc_info = pd.read_csv('/Users/mohammed5.asif/Downloads/Customer-Rating-System-Datasets/customer_account_info.csv')
cust_info = pd.read_csv('/Users/mohammed5.asif/Downloads/Customer-Rating-System-Datasets/customer_info.csv')
cust_tran = pd.read_csv('/Users/mohammed5.asif/Downloads/Customer-Rating-System-Datasets/customer_transactions.csv')

high_risk = set(countries_info["ENTITY_KEY"])


def get_risk_rating(Customer_information):
    account_key = Customer_information.account_key
    cust_tran.rename({' Transaction_Date': 'Transaction_Date'}, axis=1, inplace=True)
    cust_tran_data = cust_tran[cust_tran[" Account_Key"] == account_key].copy()
    cust_tran['Transaction_Date']= pd.to_datetime(cust_tran['Transaction_Date'])
    monthly_transactions = cust_tran['Transaction_Date'].groupby([ cust_tran.Transaction_Date.dt.month]).agg('count')

    risk_codes = []
    high_risk_country_count = 0
    
    # h1
    for country in cust_tran_data[" Transaction_Origin/Destination"]:
        print(country)
        if country in high_risk:
            high_risk_country_count += 1 
    # m1, l1
    
    total_tran = len(cust_tran_data)
    
    #h2
    sum_of_inn_tran = sum(cust_tran_data[cust_tran_data[' Transaction Type'] == 'INN'][' Transaction_Amount(in $)'])
    #h3
    sum_of_out_tran = sum(cust_tran_data[cust_tran_data[' Transaction Type'] == 'OUT'][' Transaction_Amount(in $)'])
    #h4
    date_val_counts = cust_tran_data['Transaction_Date'].value_counts()
    max_tran_per_day = max(date_val_counts.values) 
    
    


        
    
    if(high_risk_country_count > 10):
        risk_codes.append("H1")
        risk_rating = "High"
    elif (sum_of_inn_tran > 1000):
        risk_codes.append("H2")
        risk_rating = "High"
    elif(sum_of_out_tran > 800):
        risk_codes.append("H3")
        risk_rating = "High"
    elif(max_tran_per_day > 20):
        risk_codes.append("H4")
        risk_rating = "High"
        
    elif(total_tran > 10):
        risk_codes.append("M1")
        risk_rating = "Medium"
    elif (sum_of_inn_tran > 600 and sum_of_inn_tran < 1000):
        risk_codes.append("M2")
        risk_rating = "Medium"
    elif(sum_of_out_tran > 500 and sum_of_out_tran < 800):
        risk_codes.append("M3")
        risk_rating = "Medium"
    elif(max_tran_per_day > 10 and max_tran_per_day < 20):
        risk_codes.append("M4")
        risk_rating = "Medium"
        
    elif(total_tran < 10):
        risk_codes.append("L1")
        risk_rating = "Low"
    elif (sum_of_inn_tran < 600):
        risk_codes.append("L2")
        risk_rating = "Low"
    elif(sum_of_out_tran < 500):
        risk_codes.append("L3")
        risk_rating = "Low"
    elif(max_tran_per_day < 10):
        risk_codes.append("L4")
        risk_rating = "Low"
    else:
        risk_codes.append("")
        risk_rating = "Low"
        
    
    return risk_codes, risk_rating


class Customer_information(BaseModel):
    account_key: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/Customer_information/")
def print_cust_info(Customer_information:Customer_information):
    print(Customer_information)
    risk_codes, risk_rating = get_risk_rating(Customer_information)
    
    result = {
        "risk_code":risk_codes,
        "risk_rating":risk_rating,
        "response":200
    }
    return result

uvicorn.run(app, host="127.0.0.1", port=5003, log_level="info")