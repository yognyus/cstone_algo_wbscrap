from re import M
from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
kurs_all = soup.find_all("tr")

print(len(kurs_all))

tgl=[kurs.find("td").text for kurs in kurs_all]
exch=[kurs.a.text.replace(",","") for kurs in kurs_all]

#change into dataframe
kurs_data = pd.DataFrame(
    {
        "Date" : tgl,
        "ExRate" : exch
    }
)
#print(kurs_data)
#insert data wrangling here

kurs_data['Date']=kurs_data['Date'].astype('datetime64')
kurs_data['ExRate']=kurs_data['ExRate'].astype('float64')
kurs_data=kurs_data.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{kurs_data["ExRate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = kurs_data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)