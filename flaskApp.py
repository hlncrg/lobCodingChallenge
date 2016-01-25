from flask import Flask
from flask import request, render_template, redirect, url_for, redirect
import lob 
import urllib2
import json
lob.api_key = 'test_0dc8d51e0acffcb1880e0f19c79b2f5b0cc'
#import libraries and set lob key

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')#home page
def index():
    return render_template('index.html')

@app.route('/sendLetter', methods = ['POST'])
def sendLetter():#after pushing submit, go into this function
    fileHTML = open("example0.html", "r").read()#letter template
    senderName=request.form['name']#get info from submission form
    senderAddressState=request.form['state']
    senderAddressZip=request.form['zip']
    senderAddressCity=request.form['city']
    senderAddressLine1=request.form['address']
    letterContent=request.form['letter']
    if letterContent=='' or senderAddressZip=='' or senderAddressCity=='' or senderAddressLine1=='' or senderName=='':
        return '<html style="padding-top: .5in; margin: .5in;">Something went wrong.  Hit back and try again</html>'
    #if form is empty return an error    

    requestString='https://www.googleapis.com/civicinfo/v2/representatives?address='+senderAddressState+'&levels=administrativeArea1&roles=headOfGovernment&key=AIzaSyB7Ei3b6IIMhv1udluKomljDwBcJeZSIgQ'
    response=json.load(urllib2.urlopen(requestString))
    #call google api to find governor of state given

    #create the letter on lob
    letter=None
    try:
        letter=lob.Letter.create(
          description = 'Demo Letter',
          to_address = {
              'name': response['officials'][0]['name'],
              'address_line1': response['officials'][0]['address'][0]['line1'],
              'address_city': response['officials'][0]['address'][0]['city'].title(),
              'address_state': response['officials'][0]['address'][0]['state'],
              'address_zip': response['officials'][0]['address'][0]['zip'],
              'address_country': 'US'

          },
          from_address = {
              'name': senderName,
              'address_line1': senderAddressLine1,
              'address_city': senderAddressCity,
              'address_state': senderAddressState,
              'address_zip': senderAddressZip,
              'address_country': 'US'     
          },
          file = fileHTML,
          data = {
            'letterContent': letterContent
          },
          color = True
        )
    #if a value for the url does not exist, give a warning
    except:
        return '<html style="padding-top: .5in; margin: .5in;">Something went wrong.  Hit back and try again</html>'
    #redirect to the letter produced
    return redirect(letter['url'])

if __name__ == '__main__':
    app.run()
