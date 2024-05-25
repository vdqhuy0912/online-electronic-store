import pickle

phones = pickle.load(open('phone_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(phone_name):
    phone_index = phones[phones['product_name'] == phone_name].index[0]
    distances = similarity[phone_index]
    smlPhone_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    for i in smlPhone_list:
        print(phones.iloc[i[0]].product_name)

if __name__ == '__main__':
    phone_name = 'Samsung Galaxy A05 4GB 128GB'
    recommend(phone_name)