#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import requests as r
import pandas as pd
import time


# In[50]:


headers = {'Authorization': st.secrets["token"] , 'Accept': 'application/json', 'Content-Type': 'application/json'}



# In[2]:


st.title("Banabikurye'de Daha Fazla Kazanç Elde Etmek İster Misiniz?")
st.subheader("Vereceğiniz bilgileri size daha uygun gönderiler sağlayabilmek için kullanacağız.")


phone = st.text_input("Telefon numaranız:")

def external_id(phone):
    while True:
        try:
            phone = phone.replace(" ", "")
            phone = phone.replace("-", "")
            phone = phone.replace("(", "")
            phone = phone.replace(")", "")
            phone = phone.replace("+", "")
            if len(phone) == 11:
                phone = phone[1:11]
            else:
                phone = phone  
            query = {
            "query" : {
                "field" : "phone",
                "operator" : "=",
                "value" : phone
            } } 
            url = "https://api.intercom.io/contacts/search"
            result = r.post(url, headers=headers, json=query)
            result = result.json()
            return(result["data"][0]["id"])
        except IndexError:
            return("not exist")

if not phone:
    st.subheader("Lütfen sisteme kayıtlı telefon numaranızı girip formu doldurunuz.")
elif external_id(phone) == "not exist":
    st.subheader("Lütfen sistemde kayıtlı olan telefon numaranızı giriniz.")
else:
    with st.form(key='my_form'):
        schedule = st.radio("Banabikurye'de çalışmak için haftada ne kadar zaman ayırabilirsiniz?", ('Haftada 20 saatten az çalışabilirim', 'Haftada 20 ila 30 saat arası çalışabilirim', 'Haftada 30 saatten fazla çalışabilirim'))
        work_type = st.radio("Halihazırda çalışmakta olduğunuz tam ya da yarı zamanlı bir işiniz var mı?", ('Tam zamanlı işim var', 'Yarı zamanlı işim var', 'Hayır, yok'))
        has_company = st.radio('Kazancınıza karşılık fatura kesebileceğiniz bir şirketiniz var mı?', ('Evet', 'Hayır'))
        st.text("Aşağıdaki ifadelerden size uygun olanları seçiniz. Birden fazla seçim yapabilirsiniz.")
        opt_1 = st.checkbox('Profesyonel olarak kuryelik yapıyorum, tecrübeliyim.')
        opt_2 = st.checkbox('Geçici süreyle kuryelik yapmayı planlıyorum.')
        opt_3 = st.checkbox('Ana gelir kaynağım kuryelik.')
        opt_4 = st.checkbox('Trendyol, Banabi, Getir gibi farklı şirketlerde de kuryelik yapıyorum.')
        opt_5 = st.checkbox("Banabikurye'den elde edeceğim kazanç asıl gelir kaynağım olacak.")
        opt_6 = st.checkbox("Banabikurye'yi ek gelir elde etmek için kullanmayı planlıyorum.")
        submit_button = st.form_submit_button(label='Gönder')


    if submit_button:
        st.subheader("Vermiş olduğunuz cevaplar için teşekkür ederiz.")
        
    courier_id = external_id(phone)
    
    
    opts = {}
    opts["opt_1"] = opt_1
    opts["opt_2"] = opt_2
    opts["opt_3"] = opt_3
    opts["opt_4"] = opt_4
    opts["opt_5"] = opt_5
    opts["opt_6"] = opt_6


    options = []
    for key, value in opts.items():
             if value == True:
                options.append(key)
        
    update_1 = {"type": "contact",
            "id": courier_id,
            "custom_attributes" : {
                               "options": ' '.join(x for x in options)
            }}


    # In[12]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_1)





    update_2 = {"type": "contact",
     "id": courier_id,
      "custom_attributes" : {
                           "schedule": schedule
    }}


    # In[ ]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_2)




    # In[22]:


    update_3 = {"type": "contact",
     "id": courier_id,
      "custom_attributes" : {
                           "has_company": has_company
    }}


    # In[ ]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_3)
    
    update_3 = {"type": "contact",
     "id": courier_id,
      "custom_attributes" : {
                           "work_type": work_type
    }}


    # In[ ]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_3)

