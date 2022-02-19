import numpy as np
import pandas as pd
import json
from app import db, Post
from datetime import datetime

f  =open('bankAccountdde24ad.json')
data = json.load(f)

for  i in range(len(data)):
    list_ = list(data[i].values())
    post = Post(id_no = i+1,account_no=list_[0],date=datetime.strptime(list_[1], '%d %b %y'),transaction_details=list_[2],value_date=datetime.strptime(list_[3], '%d %b %y'),withdrawal_amt=list_[4],deposit_amt=list_[5],balance_amt=list_[6])
    db.session.add(post)
    db.session.commit()
print(Post.query.all())