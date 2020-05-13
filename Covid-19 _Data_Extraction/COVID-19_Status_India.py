#!/usr/bin/env python
# coding: utf-8

# # Automated script to extract COVID-19 related data for all the states in India

# ## Stage 1 - Data Extraction
# 
# ### Modules to be used for data extraction

# In[1]:


from urllib import request as req
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import lxml


# In[2]:


# Official website for data extraction

url = 'https://www.mohfw.gov.in/'


# ### Step 1 - Connection Establishment
#    >This step comprises of three sub steps:
#  - Opening of client and establishing connection
#  - Reading the page content
#  - Closing the client and connection

# In[3]:


# opening the client connection
client = urlopen(url) 

# reading the data from the html page and storing it
page_html = client.read()

# closing the client connection
client.close()


# ### Step 2 - Parsing of the web information

# In[4]:


# the extracted page is parsed using BeautifulSoup
page_soup = bs(page_html, 'lxml')


# ### Step 3 - Extraction of the web data (Web Scraping or Web Data extraction)
# > Based on the type and volume of data, the data extraction step plays a very crucial role.  

# In[5]:


# Extracting the name of the data source

data_source = page_soup.find("div",{"class":"logo-text"}).text


# 

# In[6]:


# Upon checking the text present in the tag, there are newline characters present in the beginning and end of text.
# the strip() is used to handle the newline characters.

data_source


# In[7]:


src = data_source.strip()


# In[8]:


src


# In[9]:


# Since the data gets updated very frequently, therefore the timestamp information becomes very handy
# the below lines can be converted to a singe line by chaining the functions

# 01. extracting the text information which contains the date and time
time_stamp = page_soup.find("div",{"class":"status-update"}).text
print("01. After text extraction: ",time_stamp)


# 02.stripping the newline characters
time_stamp = page_soup.find("div",{"class":"status-update"}).text.strip()
time_stamp
print("02. After stripping the extra chars: ",time_stamp)

# 03.After splitting the timestamp to extract the date and time string
time_stamp = page_soup.find("div",{"class":"status-update"}).text.strip().split(":",1)
time_stamp
print("03. After splitting the text, returns a list: ",time_stamp)


# In[10]:


# In the above step after executing the split(), the time_stamp variable becomes a list and contains two elements.
# time_stamp[1] contains the extraction timestamp details.
# Storing the extraction date and time information.
# Refer documentation of split() to understand further on how the list gets generated

extr_date = time_stamp[1].split(",",1)[0].strip()
print("Extraction date:",extr_date)
extr_time = time_stamp[1].split(",",1)[1].strip() #chaining the strip() to remove the spaces from the beginning
print("Extraction time:",extr_time)


# In[11]:


# Extraction of summary level data 
# Extracting the text from the list<> and strong<>

active = page_soup.find("li",{"class":"bg-blue"}).strong.text  
cured = page_soup.find("li",{"class":"bg-green"}).strong.text
deaths = page_soup.find("li",{"class":"bg-red"}).strong.text
print("Active Cases : ", active)
print("Cured  Cases : ", cured) 
print("Total  Deaths: ", deaths)


# In[12]:


# Beginning of the state-wise data extraction
# Since the data is stored in multiple rows of a table
# therefore the table was first identified and the rows were saved in a resultset 

html_table = page_soup.find("table",{"class":"table table-striped"})
tbody = html_table.findAll("tr")


# In[13]:


print(type(html_table))
print(type(tbody))


# In[14]:


# The row level state wise information was looped and the data was extracted
# The replace() was used in order to remove the newline characters and replace them with comma(,).
# Ignoring the first Header row and the bottom 5 assumptions, therefore the range() is used from 1 till (len(table body)-5)

data = []
for i in range(1,(len(tbody)-5)):
    data_row = tbody[i].text.strip().replace("\n",",")
    data.append(data_row)


# In[15]:


data[0:3]


# ## Stage 2 - Data Loading & Manipulation
# ### Modules to be used for data manipulation

# In[16]:


import pandas as pd


# In[18]:


# the extracted dataset is now loaded into Pandas dataframe

df = pd.DataFrame(data)


# In[19]:


# Viewing the data
df.head()

# Upon checking the data, looks like the extracted data has only 1 column and the data is missing the headers.
# The state wise data in the website looks something like the below:
# |------------------------------------------------------------------------------------------------|
# |'Sl No.'| 'Name of State/UT' | 'Total Confirmed Cases' | 'Cured/Discharged/Migrated' | 'Deaths' |
# | 1      | Odisha             |  377                    |  68                         |  3       |
# |------------------------------------------------------------------------------------------------|


# In[20]:


# The data is engineered using the string manipulation functions in pandas
# The string in the Column 0 is separated by using the split() and referencing the comma(,) separator

df = pd.DataFrame(df[0].str.split(",",4).tolist())


# In[21]:


df.head(3)


# In[22]:


# Updating the column names 

df.columns = ['Sl No','Name of State/ UT','Total Confirmed Cases','Cured/Discharged/Migrated','Deaths']

# deleting the Sl No. column from the data frame
df = df.drop(columns=['Sl No'])
df


# In[23]:


df.head(3)


# In[24]:


df['Date'] = extr_date
df['Time'] = extr_time
df.head(3)


# In[25]:


df.head(3)


# In[278]:


# Installing the and importing the required modules in order to save the file in excel format.

#import openpyxl as exl


# In[279]:


# Excel file with the specified name gets saved in the same working directory as the python notebook

#df.to_excel(r'India_11_05.xlsx', index = False, header=True)


# In[26]:


# exporting the data frame to csv format
df.to_csv('covid_11_05.csv', mode ='a',header=False,index= False)


# In[27]:


# loading the recently created csv into dataframe

df1 = pd.read_csv('covid_11_05.csv')
df1["Total Confirmed Cases"].max()


# In[28]:


df1


# In[29]:


df1 =df1.sort_values(by ="Total Confirmed Cases",ascending = False)


# In[30]:


df1.head(3)


# In[ ]:





# In[ ]:





# In[ ]:




