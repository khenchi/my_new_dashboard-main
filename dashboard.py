import pandas as pd
import streamlit as st
import requests
from os import path as op

# let’s add a bit more descriptive text to our UI
st.write("""

# Welcome on this dashboard !

# Context
The company "Ready to distribute" wishes to set up a "credit scoring" tool to calculate the \
probability that a customer will repay his credit, then classify the request as granted or \
refused credit
The label is a binary variable, 0 (will repay the loan on time), 1 (will have difficulty repaying \
the loan)

# Objectives
 1. Create a classification model that will automatically predict the likelihood that a customer \
  can or cannot repay their loan.

 2. Build an interactive dashboard for customer relationship managers to interpret the predictions\
  made by the model, and improve the customer knowledge of customer relationship managers.

""")


def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}

    data_json = {'data': data}
    response = requests.request(
        method='POST', headers=headers, url=model_uri, json=data_json)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))

    return response.json()


def main():
    # model_uri = 'http://127.0.0.1:5000/invocations'
    # URL de l'API
    model_uri = "https://test-p7.herokuapp.com/"
    st.title('Predict the probability of getting a loan for a customer')

    ID = st.number_input('Customer ID', min_value=100000, step=1)
    df = pd.read_csv(op.join(op.dirname(op.realpath(__file__)), 'data.csv'),
                 low_memory=False)
    predict_btn = st.button('Predict')
    if predict_btn:
        data = df[df['identifiant'] == ID]
        del (data['identifiant'])
        data = data.to_json()
        pred = request_prediction(model_uri, data)[0]
        st.write(
            'The probability of giving a loan for this client is {:.2f}'.format(pred))


if __name__ == '__main__':
    main()
