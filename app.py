#######libraries############
from bs4 import BeautifulSoup as bs
from flask import Flask,request,jsonify,render_template
import pymongo
from flask_cors import CORS,cross_origin
import requests as req
from urllib.request import urlopen as ureq
######libraries############


app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/scrap',methods=['POST'])
@cross_origin()
def index():
    if request.method =='POST':
        search=request.form['content'].replace(' ','')
        try:
            '''''
            connect=pymongo.MongoClient("mongodb://localhost:27017/")
            db=connect['first_crawler_flipkart']
            item_table=db[search].find({})
            #print(item_table.count())
            review_list = []
            if item_table.count()>0:
                return render_template('results.html',reviews=item_table)
            '''''
            review_list = []
            flipkart_url = "https://www.flipkart.com/search?q=" + search
            print(flipkart_url)
            uclient = ureq(flipkart_url)
            html_page = uclient.read()
            flipkart_html = bs(html_page, 'html.parser')
            box = flipkart_html.findAll('div', {'class': '_1AtVbE col-12-12'})
            del box[0:2]
            for i in box:
                #print(i)
                try:
                    long_short_desc = list(i.div.children)
                except:
                    print('not required tag')
                if len(long_short_desc) != 1:
                    sbox = i.findAll('div', {'class': '_4ddWXP'})
                else:
                    sbox = long_short_desc
                for j in sbox:
                    product_link = "https://www.flipkart.com" + j.a['href']
                    req = ureq(product_link)
                    product_html = bs(req.read(), 'html.parser')
                    whole_reviews = product_html.findAll('div', {'class': '_2c2kV-'})
                    for k in whole_reviews:
                        whole_com = k.findAll('div', {'class': '_16PBlm'})
                        for l in whole_com:
                            try:
                                heading = l.div.div.div.p.text
                            except:
                                heading = 'NO heading'
                            try:
                                rating = l.div.div.div.div.text
                            except:
                                rating = 'no rating'
                            try:
                                comment = l.find('div', {'class': 't-ZTKy'}).div.div.text
                            except:
                                comment='no comment'
                            try:
                                name = l.find('p',{'class':'_2sc7ZR _2V5EHH'}).text
                            except:
                                name = 'no name'
                            mydict = {"Product": search, "Name": name, "Rating": rating, "CommentHead": heading,"Comment":comment}
                            #table.insert_one(mydict)
                            review_list.append(mydict)
                            render_template('results.html', reviews=review_list)
            #print(review_list)
            return render_template('results.html',reviews=review_list)
        except Exception as e:
            print(e)
            return 'Something is wrong'
    else:
        return render_template('index.html')










if __name__=="__main__":
    app.run(debug=True)
