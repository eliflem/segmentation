#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import streamlit as st
import requests as r
import pandas as pd
import datetime
import os
import streamlit as st
import base64


# In[ ]:


st.title("Pipedrive - Times in Stage")


# In[3]:


filter_id = st.text_input("Please enter filter id:")
token = st.text_input("Please enter your token:")
from datetime import date
today = date.today()
d1 = today.strftime("%B %d")
print("Thank you! Please do not close this window, it'll be closed automatically. When this window is closed, your csv file will be saved as "+d1)


# In[8]:


filters=r.get("https://api.pipedrive.com/v1/deals?filter_id="+filter_id+"&status=all_not_deleted&start=-1&limit=1000&api_token="+token)
filter_deals = filters.json()

created = {}
ids = []
for deal in filter_deals["data"]:
    deal_ids = deal["id"]
    ids.append(deal_ids)
    created[deal_ids] = deal["add_time"] #dealcreated

deals_ids = [str(i) for i in ids] #deal ids


# In[ ]:


links = []
for deal in deals_ids:
    links.append("https://api.pipedrive.com/v1/deals/"+deal+"?api_token="+token)

result = []
for link in links:
    resp = r.get(link)
    result.append(resp.json())

stages={}
for i in result:
    id = i["data"]["id"]
    stages[id] = i["data"]["stay_in_pipeline_stages"]["times_in_stages"]
    owner = 'owner'
    stages[owner] = [i["data"]["owner_name"]]
    created = 'created time'
    stages[created] = [i["data"]["add_time"]]


# In[ ]:


st.write(stages)


# In[ ]:


#path = os.path.dirname(os.path.realpath("__file__"))
df = pd.DataFrame(list(stages.items()), columns = ["Deal ID", "Time in stage"])
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown('### **⬇️ Download output CSV File **')
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ".csv")'
st.markdown(href, unsafe_allow_html=True)


# In[ ]:


#csv = df.to_csv("results.csv", index=False)
#f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'


# In[9]:


#path = os.path.dirname(os.path.realpath("__file__"))
#df = pd.DataFrame(list(final.items()), columns = ["Deal ID", "Difference(min)"])
#df.to_csv(path+"\\"+d1+".csv", index=False)

