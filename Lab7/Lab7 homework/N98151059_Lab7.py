import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = np.loadtxt("Bank_Customer.csv", skiprows=1, dtype=str, delimiter=',')

# 欄位順序：
# 0 customer_id, 1 credit_score, 2 country, 3 gender, 4 age, 5 tenure,
# 6 balance, 7 products_number, 8 credit_card, 9 active_member,
# 10 estimated_salary, 11 churn

# 1. 非數值型資料轉換成數值型資料
# country：France -> 0, Germany -> 1, Spain -> 2
country = np.where(data[:, 2] == "France", 0,
                   np.where(data[:, 2] == "Germany", 1, 2))
# gender：Female -> 0, Male -> 1
gender = np.where(data[:, 3] == "Female", 0, 1)

# 2. 去除掉無意義的特徵類別
# customer_id（第 0 欄）只是客戶編號，跟是否流失無關，所以不放進特徵
x = np.column_stack((
    data[:, 1].astype(float),      # credit_score
    country,                       # country（已轉成數字）
    gender,                        # gender（已轉成數字）
    data[:, 4:11].astype(float)    # age ~ estimated_salary
)).astype(float)

# churn（第 11 欄）是要預測的答案，不做標準化
y = data[:, 11].astype(int)

# 3. 標準化特徵：每個特徵變成平均 0、標準差 1（Z-score normalization）
scaler = StandardScaler()
x = scaler.fit_transform(x)

# 前處理後的資料 = 特徵 + 答案
pre_data = np.column_stack((x, y))

np.savetxt("Bank_Customer_Preprocessed.csv", pre_data, delimiter=",", fmt="%.6f")


from sklearn.linear_model import LogisticRegression
# 決策分類器
clf = LogisticRegression()

# 4. 切割 data 為 x_train, x_test, y_train, y_test
# test_size=0.3：30% 當測試資料、70% 當訓練資料
# random_state=42：固定亂數種子，每次切出來的結果都一樣
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=42
)

# 使用訓練集來訓練我們的分類器
clf.fit(x_train, y_train)
# 測試資料集中進行預測
pred = clf.predict(x_test)

#print (pred) # 預測分類，即客戶是否流失
#print (y_test) # 分類
print (str(accuracy_score(pred, y_test)*100 ) + "% ")   # 預測精度
