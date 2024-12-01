import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import json
conn = create_engine('mysql+pymysql://root:123456@localhost:3306/hourses_data?charset=utf8&autocommit=true')
transfer = LabelEncoder()

def getJSONFirst(item):
    try:
        return int(json.loads(item)[-1])
    except:
        return 0

def getData():
    df = pd.read_sql('select * from hourse_info',con=conn,index_col='id')
    X = df[['city','rooms_desc','area_range','hourseType','sale_status','price']]
    X['hourseType'] = X['hourseType'].replace('住宅',0) \
                                 .replace('别墅', 1)\
                                .replace('商业类', 2)\
                                .replace('商业', 3)\
                                .replace('酒店式公寓', 4)\
                                .replace('底商', 5)\
                                .replace('写字楼', 6)\
                                .replace('车库', 7)
    X['city'] = transfer.fit_transform(X['city'].values)
    X['rooms_desc'] = X['rooms_desc'].apply(getJSONFirst)
    X['area_range'] = X['area_range'].apply(getJSONFirst)
    X['price'] = X['price'].astype('int')
    return X

def model_train(data):
    # 数据集 测试集划分
    x_train,x_test,y_train,y_test =  train_test_split(data[['city','rooms_desc','area_range','hourseType','sale_status']],data['price'],test_size=0.25,random_state=1)
    # 创建一个线性回归对象
    linear2 = LinearRegression()

    # 多元线性回归 模型训练
    linear2.fit(x_train,y_train)

    return linear2

def pred(model,*args):
    city = transfer.transform([args[0]])[0]
    rooms_desc = args[1]
    area_range = args[2]
    hourseType = ['住宅','别墅','商业类','酒店式公寓','底商','写字楼','车库'].index(args[3])
    sale_status = args[4]

    predPrice = model.predict([
        [city,rooms_desc,area_range,hourseType,sale_status]
    ])
    return round(predPrice[0],1)



if __name__ == '__main__':
    model = model_train(getData())
    pred(model,'北京',5,150,'别墅',3)