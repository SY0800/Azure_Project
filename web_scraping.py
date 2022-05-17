# -*- coding: utf-8 -*-
"""Web scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vlhdEIRqLnximpGRDmEu7HcD-pxPuCpG
"""

from flask import Flask, redirect, render_template, url_for, request
app = Flask(__name__)

# import module
import requests
from bs4 import BeautifulSoup

#pip install azure-ai-textanalytics==5.1.0
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential



#!pip install



HEADERS = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

# user define function
# Scrape the data
def getdata(url):
	r = requests.get(url, headers=HEADERS)
	return r.text


def html_code(url):

	# pass the url
	# into getdata function
	htmldata = getdata(url)
	soup = BeautifulSoup(htmldata, 'html.parser')

	# display html code
	return (soup)


#url = "https://www.amazon.in/Vivinks-Womens-Sleeves-T-Shirt-XX-Large/dp/B09W5SNZ1F/ref=sr_1_1_sspa?pf_rd_i=283155&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=05b91ec0-2ed2-4cf5-a33a-23a7d8762cf1&pf_rd_r=35b4cd2c-f088-4d84-9397-bfbd0c4ca14a&pf_rd_s=center-1&pf_rd_t=101&qid=1652425406&refinements=p_36%3A-39900%2Cp_72%3A1318476031%2Cp_85%3A10440599031&rnid=10440598031&rps=1&s=apparel&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNjJDWVlEQVlaT1JLJmVuY3J5cHRlZElkPUEwODQ4NzUwMVQ1N1ZTVFY4SUwzUCZlbmNyeXB0ZWRBZElkPUEwMzA3NDA2MzJZTENYTVZNMVlIUCZ3aWRnZXROYW1lPXNwX2F0Zl9icm93c2UmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl"
#url = "https://www.amazon.in/Aahwan-Black-Ribbed-Womens-173-Black-M/dp/B09QL59JGR/ref=sr_1_2?pf_rd_i=283155&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=05b91ec0-2ed2-4cf5-a33a-23a7d8762cf1&pf_rd_r=35b4cd2c-f088-4d84-9397-bfbd0c4ca14a&pf_rd_s=center-1&pf_rd_t=101&qid=1652425406&refinements=p_36%3A-39900%2Cp_72%3A1318476031%2Cp_85%3A10440599031&rnid=10440598031&rps=1&s=apparel&sr=1-2"
#soup = html_code(url)
#print(soup)

def cus_rev(soup):
	# find the Html tag
	# with find()
	# and convert into string
	data_str = ""


	for item in soup.find_all("span", attrs={'data-hook':'review-body'}):
		data_str = data_str + item.get_text()

	result = data_str.split("\n")
	return (result)


#rev_data = cus_rev(soup)
#rev_result = []
#for i in rev_data:
#	if i is "":
#		pass
#	else:
#		rev_result.append(i)
#rev_result

#rev_result=rev_result[0:3]
#rev_result


key = "b1dd6471771640019c164689d6bded4e"
endpoint = "https://sentiment-detect.cognitiveservices.azure.com/"



# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

#client = authenticate_client()

# Example function for detecting sentiment in text
def sentiment_analysis_example(client, rev_result):
    result=[]
    documents = rev_result
    response = client.analyze_sentiment(documents=documents)[0]
    result.append("Document Sentiment: {}<br>".format(response.sentiment))
    result.append("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} <br>".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        result.append("<br>Sentence: {}<br>".format(sentence.text))
        result.append("Sentence {} sentiment: {}<br>".format(idx+1, sentence.sentiment))
        result.append("Sentence score:<br>Positive={0:.2f}<br>Neutral={1:.2f}<br>Negative={2:.2f}<br>".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))
    return result
          
#sentiment_analysis_example(client)

def driver_code(link):
    soup=html_code(link)
    
    rev_data = cus_rev(soup)
    rev_result = []
    for i in rev_data:
        if i is "":
            pass
        else:
            rev_result.append(i)

    rev_result=rev_result[0:3]
    client = authenticate_client()

    return sentiment_analysis_example(client, rev_result)

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        #print(ele)
        str1 += ele  
    
    # return string  
    return str1

# @app.route('/success/<name>')
# def success(name):
#     print(name)
#     return driver_code("%s") % name
#     #return driver_code(name)

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
       user = request.form['nm']
       result=driver_code(user)
       return listToString(result)
    else:
        user = request.form['nm']
        result=driver_code(user)
        return listToString(result)

if __name__ == '__main__':
    app.run(debug = True)


