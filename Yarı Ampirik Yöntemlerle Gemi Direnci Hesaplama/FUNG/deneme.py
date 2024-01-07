# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:07:26 2023

@author: uygur
"""

# import numpy as np
# import matplotlib.pyplot as plt

# # Manuel olarak tanımlanan VL, DL ve CR1 array'leri
# VL_values = np.array([0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3])
# DL_values = np.array([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250])
# CR1_array = np.loadtxt("cr1.txt").reshape(len(VL_values), len(DL_values))  # Dosya adını ve yolu güncelleyin

# # Scatter plot çizimi
# plt.scatter(np.repeat(VL_values, len(DL_values)), np.tile(DL_values, len(VL_values)), c=CR1_array.flatten(), cmap='viridis', s=50, vmin=-1, vmax=10)
# cbar = plt.colorbar()
# cbar.set_label('CR1 Değerleri')
# plt.xlabel('VL (x ekseni)')
# plt.ylabel('DL (y ekseni)')
# plt.title('VL, DL ve CR1 Scatter Plot')
# plt.show()

############################################################################################################################################################################################

# import numpy as np
# from scipy.interpolate import griddata

# # Manuel olarak tanımlanan VL, DL ve CR1 array'leri
# VL_values = np.array([0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3])
# DL_values = np.array([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250])
# CR1_array = np.loadtxt('cr1.txt')  # Dosya adını ve yolu güncelleyin

# # Kullanıcıdan DL ve VL değerlerini al
# user_DL = float(input("DL değerini girin: "))
# user_VL = float(input("VL değerini girin: "))

# # Her bir koordinatın bir satırda olduğu bir dizi oluştur
# points = np.array(np.meshgrid(VL_values, DL_values)).T.reshape(-1, 2)

# # Kullanıcıdan alınan DL ve VL değerlerini bir dizi haline getir
# user_point = np.array([[user_VL, user_DL]])

# # Griddata ile interpolasyon yapma
# user_CR1 = griddata(points, CR1_array.flatten(), user_point, method='linear')

# print(f"DL={user_DL}, VL={user_VL} için interpolasyon sonucu CR1={user_CR1[0]:.5f}")

############################################################################################################################################################################################
############################################################################################################################################################################################

"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Verileri tanımla
data = np.loadtxt('cr1.txt')

# Kullanıcıdan dereceyi al
degree = int(input("Enter the degree of the polynomial: "))

# Verileri numpy dizilerine çevir
x_values = data[:, 0].reshape(-1, 1)
y_values = data[:, 1]

# Polynomial özelliklerini oluştur
poly_features = PolynomialFeatures(degree=degree)
x_poly = poly_features.fit_transform(x_values)

# Lineer regresyon modelini oluştur
model = LinearRegression()
model.fit(x_poly, y_values)

# Katsayıları ve intercept'i al
coefficients = model.coef_
intercept = model.intercept_

# x cinsinden denklemi yazdır
equation = f"y = {intercept:.4f}"
for i in range(1, degree + 1):
    equation += f" + {coefficients[i]:.4f}x^{i}"

print(f"\nPolynomial Equation: {equation}")

# Kullanıcının x değerini al
user_x = float(input("\nEnter the value of x to find the corresponding y: "))

# Girilen x değeri için y'yi hesapla
user_x_poly = poly_features.transform(np.array([[user_x]]))
user_y_pred = model.predict(user_x_poly)[0]

print(f"\nFor x = {user_x}, y = {user_y_pred:.4f}")

# R^2 değerini hesapla
y_pred = model.predict(x_poly)
r2 = r2_score(y_values, y_pred)
print(f"R^2 Score: {r2:.4f}")

# Grafik çizimi
plt.scatter(x_values, y_values, color='blue', label='Actual Data')
plt.plot(x_values, y_pred, color='red', label=f'Polynomial Fit (Degree {degree})\n{equation}\nR^2 = {r2:.4f}')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.legend()
plt.title('Polynomial Regression')
plt.show()
"""

############################################################################################################################################################################################
############################################################################################################################################################################################
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Verileri yükleme
data = np.loadtxt("CR1.2.txt", skiprows=1, usecols=range(7))

# Sütun sayısını belirleme
num_columns = data.shape[1]

# Kullanıcıdan eğri derecesini alın
degree = int(input("Eğri Derecesini Girin: "))

# DL (x) ve y değerlerini ayırma
DL = data[:, 0]
y_values = data[:, 1:]

# Tahmin edilen değerleri tutacak array'leri oluştur
predictions_array = []

# Her bir y değeri için ayrı ayrı işlemler yapma
for i in range(num_columns - 1):
    y = y_values[:, i]

    # NaN veya sıfır olmayan değerlere sahip satırları seçme
    valid_indices = ~np.isnan(y) & (y != 0)
    valid_DL = DL[valid_indices]
    valid_y = y[valid_indices]

    if len(valid_DL) > 0:  # Eğer geçerli DL değerleri varsa işlem yap
        # Polynomial Regression modeli oluşturma
        model = np.polyfit(valid_DL, valid_y, degree)
        polynomial = np.poly1d(model)

        # R^2 değerini hesaplama
        y_pred = polynomial(valid_DL)
        r2 = r2_score(valid_y, y_pred)

        # Grafik çizimi
        plt.scatter(valid_DL, valid_y, label=f"1.{i}")
        plt.plot(valid_DL, polynomial(valid_DL), label=f"1.{i} - R^2: {r2:.4f}")

        plt.xlabel("DL")
        plt.ylabel("Y Değerleri")
        plt.legend()
        plt.show()
    else:
        print(f"1.{i} - Geçerli DL değeri yok, dolayısıyla işlem yapılamıyor.")

# Kullanıcının girdiği x değerini alın
x_value = float(input("DL Değerini Girin: "))

# Kullanıcının girdiği x değeri DL arrayinde herhangi bir elemana eşitse, y değerini kullanıcının girdiği DL değerine karşılık gelen y_values'deki y değeri yap
if x_value in DL:
    index = np.where(DL == x_value)[0][0]
    for i in range(num_columns - 1):
        if not np.isnan(y_values[index, i]) and y_values[index, i] != 0:
            print(f"1.{i} - Kullanıcının girdiği x değerine karşılık gelen y değeri: {y_values[index, i]:.4f}")
        else:
            print(f"1.{i} - Kullanıcının girdiği x değerine karşılık gelen y değeri yok.")
            predictions_array.append(y_values)
else:
    # Kullanıcının girdiği x değeri DL arrayinde herhangi bir elemana eşit değilse, o zaman denklemden y değerini bul
    for i in range(num_columns - 1):
        y = y_values[:, i]

        # NaN veya sıfır olmayan değerlere sahip satırları seçme
        valid_indices = ~np.isnan(y) & (y != 0)
        valid_DL = DL[valid_indices]

        if len(valid_DL) > 0:  # Eğer geçerli DL değerleri varsa işlem yap
            model = np.polyfit(valid_DL, y[valid_indices], degree)
            polynomial = np.poly1d(model)
            prediction = polynomial(x_value)
            predictions_array.append(prediction)

            print(f"1.{i} - Tahmin Edilen Y Değeri: {prediction:.4f}")
        else:
            print(f"1.{i} - Geçerli DL değeri yok veya y değeri yok, dolayısıyla işlem yapılamıyor.")
predictions_array = np.array(predictions_array)
print("Her bir sütun için tahmin edilen değerler:", predictions_array)
"""


"""
import numpy as np
from sklearn.metrics import r2_score

######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR1 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array = []

# Kullanıcının girdiği x değerini alın
x_value = float(input("DL Değerini Girin: "))

# Her bir dosya için işlemleri gerçekleştirme
for file_number in range(25, 28):
    # Dosya adını oluşturma
    file_name = f"CR{file_number}.txt"
    
    try:
        # Verileri yükleme
        data = np.loadtxt(file_name, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns = data.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree = int(input(f"{file_name} için Eğri Derecesini Girin: "))

        # DL (x) ve y değerlerini ayırma
        DL = data[:, 0]
        y_values = data[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns - 1):
            y = y_values[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices = ~np.isnan(y) & (y != 0)
            valid_DL = DL[valid_indices]
            valid_y = y[valid_indices]

            if len(valid_DL) > 0:  # Eğer geçerli DL değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model = np.polyfit(valid_DL, valid_y, degree)
                polynomial = np.poly1d(model)

                # R^2 değerini hesaplama
                y_pred = polynomial(valid_DL)
                r2 = r2_score(valid_y, y_pred)

                # Tahmin değerini predictions_array'e ekle
                if x_value in DL:
                    index = np.where(DL == x_value)[0][0]
                    if not np.isnan(y_values[index, i]) and y_values[index, i] != 0:
                        predictions_array.append(y_values[index, i])
                    else:
                        predictions_array.append(None)
                else:
                    prediction = polynomial(x_value)
                    predictions_array.append(prediction)
            else:
                print(f"1.{i} - Geçerli DL değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array = np.array(predictions_array)
        print(f"{file_name} için Her bir sütun için tahmin edilen değerler:", predictions_array)
        all_predictions_array.extend(predictions_array)

    except Exception as e:
        print(f"{file_name} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array = np.array(all_predictions_array)
print("Tüm dosyalar için her bir sütun için tahmin edilen değerler:", all_predictions_array)

"""

"""

"""
# import numpy as np
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import PolynomialFeatures

# # Veri setini tanımla
# data = np.array([[ 6.00000000e-01,  1.27080836e-02, -2.01923119e-01,
#          2.89528930e+00, -1.94067948e+00, -6.20850701e-03,
#          1.79815275e+00,  7.67634413e-02,  5.19366344e-02,
#          2.63882719e-01, -2.46457869e-01],
#        [ 7.00000000e-01, -1.53971961e-01,  1.25419546e+00,
#          5.42158780e-01, -7.31745264e-01,  4.92486920e-01,
#          2.12784741e+00,  8.41102322e-02,  6.94070263e-02,
#          3.77283889e-01, -7.12961462e-01],
#        [ 8.00000000e-01, -1.88717257e-01,  1.21674942e+00,
#         -1.28410809e-01,  1.14398852e-01,  6.29063508e-01,
#          2.13830203e+00,  8.81880615e-02,  8.80773416e-02,
#          1.40737450e-01, -7.96993665e-01],
#        [ 9.00000000e-01, -1.19025483e-01,  1.60153559e+00,
#         -4.37585554e-01,  6.05008541e-01,  7.74240790e-01,
#          1.55221929e+00,  8.03692209e-02,  8.19048910e-02,
#         -1.11617072e-01, -1.39440884e+00],
#        [ 1.00000000e+00, -1.55188603e-02,  1.92407322e+00,
#         -1.84338782e+00,  2.55194147e+00,  8.81276293e-01,
#          1.74237279e+00,  6.72372622e-02, -2.59892654e-02,
#         -8.64849521e-02, -2.13790650e+00],
#        [ 1.10000000e+00,  2.29701661e-01,  2.65345904e+00,
#         -2.39526356e+00,  2.50286374e+00,  1.05149988e+00,
#          1.66420241e+00, -2.20422878e-02, -3.17317960e-02,
#          1.53901006e-01, -2.48949633e+00],
#        [ 1.20000000e+00,  7.58052256e-01,  2.69127243e+00,
#         -3.41286800e+00,  3.93276187e+00,  9.62627369e-01,
#          1.67143492e+00, -8.22926272e-02,  2.36920228e-02,
#          2.78383139e-01, -3.05832374e+00],
#        [ 1.30000000e+00,  1.34814843e+00,  2.48618910e+00,
#         -8.44509406e+00,  9.57673118e+00,  7.23449034e-01,
#          1.26345390e+00, -2.17204733e-01,  8.88487088e-02,
#         -8.84525598e-03, -3.16014626e+00],
#        [ 1.40000000e+00,  2.14474094e+00,  2.30850217e+00,
#         -1.06401875e+01,  1.26355482e+01,  4.64944030e-01,
#          6.90095359e-01, -3.11563350e-01,  5.20371706e-02,
#         -5.69047917e-01, -3.68268507e+00],
#        [ 1.50000000e+00,  3.53910438e+00,  1.69246615e+00,
#         -1.22694543e+01,  1.46564168e+01,  7.39133464e-02,
#          2.57733232e-01, -3.33815496e-01,  9.29124130e-02,
#         -2.13113741e-01, -3.90463257e+00],
#        [ 1.60000000e+00,  4.42149574e+00,  1.23004497e+00,
#         -1.17412891e+01,  1.44267642e+01, -3.76378239e-02,
#         -9.30825704e-02, -3.85284489e-01,  7.59332177e-02,
#         -5.44213872e-01, -4.20641376e+00],
#        [ 1.70000000e+00,  4.88185961e+00,  9.68606868e-01,
#         -1.15256488e+01,  1.42818875e+01, -6.87912944e-02,
#         -2.02410304e-01, -4.04309052e-01,  9.95269247e-02,
#         -3.18135217e-01, -4.32737525e+00],
#        [ 1.80000000e+00,  5.03609948e+00,  7.98747253e-01,
#         -8.35360458e+00,  1.08841740e+01, -5.68741749e-02,
#         -4.65696517e-01, -3.36982204e-01,  1.48432431e-01,
#          0.00000000e+00, -4.25215176e+00],
#        [ 1.90000000e+00,  5.30602739e+00,  1.59797833e+00,
#         -4.65600675e+00,  7.04744799e+00, -1.07418060e+00,
#          2.85389310e-01, -5.62048601e-01,  7.11436908e-02,
#          0.00000000e+00, -4.13716921e+00],
#        [ 2.00000000e+00,  4.62758969e+00,  7.73348435e-01,
#         -6.14833122e+00,  7.95980893e+00, -2.40940641e-01,
#         -5.53918739e-02, -5.00805966e-01,  1.33087868e-01,
#          0.00000000e+00, -3.06463656e+00],
#        [ 2.10000000e+00,  4.10013293e+00,  1.02578868e+00,
#         -7.06182120e+00,  9.47621145e+00, -2.25854545e-01,
#         -1.34894929e-01, -4.15154663e-01,  3.82135718e-02,
#          0.00000000e+00, -3.69266213e+00],
#        [ 2.20000000e+00,  4.50451822e+00,  1.33684173e+00,
#         -8.89510241e+00,  1.01600991e+01, -7.05881712e-01,
#         -4.90409008e-01, -4.62024514e-01,  1.14192579e-01,
#          0.00000000e+00, -2.89876895e+00],
#        [ 2.30000000e+00,  4.10971760e+00,  1.44768152e+00,
#         -9.96349004e+00,  1.25456278e+01, -5.58888475e-01,
#         -1.10194440e+00, -5.30971734e-01,  9.04029814e-02,
#          0.00000000e+00, -4.16119546e+00]])

# my_VL = np.array([0.6044884 , 0.63859465, 0.67359843, 0.70635838, 0.7395671 ,
#        0.77277581, 0.805087  , 0.84053955, 0.8732995 , 0.90695698,
#        0.90830328, 0.94106323, 0.97427194, 1.00748066, 1.00837819,
#        1.04068938, 1.04158691, 1.07479563, 1.10890188, 1.14255936,
#        1.17621684, 1.20942556, 1.20987433, 1.24398058, 1.27763806,
#        1.28526709, 1.29424242, 1.30994924, 1.31129554, 1.3278999 ,
#        1.34450426, 1.37816174, 1.41092169, 1.44413041, 1.44592548,
#        1.47958296, 1.51234291, 1.51279168])

# # Veriyi düzenle ve x, y değerlerini ayır
# x_values = data[:, 0]
# y_values = data[:, 1:]

# # Derecesini kullanıcıdan al
# degree = 10

# # Tahmin yapacak x değerlerini belirle
# predict_x = my_VL.reshape(-1, 1)

# # Tahminleri saklamak için bir dizi oluştur
# result = np.zeros((len(my_VL), y_values.shape[1] + 1))

# # İlk sütuna all_VL değerlerini ekle
# result[:, 0] = my_VL

# # Her bir y değeri için regresyon modelini oluştur ve tahmin yap
# for i in range(y_values.shape[1]):
#     y = y_values[:, i]
    
#     # Sıfır olan değerleri kontrol et
#     zero_indices = np.where(y == 0)[0]
    
#     # Sıfır olmayan değerleri kullanarak regresyon yap
#     non_zero_x = x_values[y != 0]
#     non_zero_y = y[y != 0]
    
#     poly_features = PolynomialFeatures(degree=degree)
#     x_poly = poly_features.fit_transform(non_zero_x.reshape(-1, 1))
#     predict_x_poly = poly_features.transform(predict_x)
    
#     model = LinearRegression()
#     model.fit(x_poly, non_zero_y)
    
#     predictions = model.predict(predict_x_poly)
    
#     # Sonuçları result dizisine ekle
#     result[:, i + 1] = predictions
"""
import numpy as np
import matplotlib.pyplot as plt

Fung_R_t = np.array([3.354E+05, 3.871E+05, 4.623E+05, 5.248E+05, 5.731E+05,
    6.098E+05, 6.409E+05, 6.771E+05, 7.165E+05, 7.649E+05,
    7.670E+05, 8.223E+05, 8.863E+05, 9.588E+05, 9.609E+05,
    1.041E+06, 1.043E+06, 1.136E+06, 1.243E+06, 1.356E+06,
    1.472E+06, 1.580E+06, 1.581E+06, 1.677E+06, 1.748E+06,
    1.761E+06, 1.775E+06, 1.795E+06, 1.797E+06, 1.814E+06,
    1.830E+06, 1.864E+06, 1.920E+06, 2.019E+06, 2.026E+06,
    2.176E+06, 2.344E+06, 2.346E+06])

speeds = np.array([6.711, 7.090, 7.479, 7.842, 8.211, 8.580, 8.938, 9.332, 9.696, 10.069,
    10.084, 10.448, 10.817, 11.185, 11.195, 11.554, 11.564, 11.933, 12.311,
    12.685, 13.059, 13.427, 13.432, 13.811, 14.185, 14.270, 14.369, 14.544,
    14.558, 14.743, 14.927, 15.301, 15.665, 16.033, 16.053, 16.427, 16.791,
    16.796])

froudes = np.array([0.180, 0.190, 0.200, 0.210, 0.220, 0.230, 0.240, 0.250, 0.260, 0.270,
    0.270, 0.280, 0.290, 0.300, 0.300, 0.310, 0.310, 0.320, 0.330, 0.340,
    0.350, 0.360, 0.360, 0.370, 0.380, 0.382, 0.385, 0.390, 0.390, 0.395,
    0.400, 0.410, 0.420, 0.430, 0.430, 0.440, 0.450, 0.450])

p_e = Fung_R_t * speeds


#EXPERIMENTAL RESULTS

real_froudes = np.array([0, 0.0498028958929961, 0.0499364157211275,
                    0.0592828036903225, 0.0700979097689624, 0.0700979097689624,
                    0.0746375839254285, 0.0798448572225514, 0.0898588443324032,
                    0.100006351270386, 0.109886818552107, 0.119900805661958,
                    0.12003432549009, 0.129781272943679, 0.139661740225399,
                    0.139795260053531, 0.150076286819645, 0.159823234273234,
                    0.160090273929497, 0.169837221383086, 0.179851208492938,
                    0.189998715430921, 0.200413262025167, 0.210160209478756,
                    0.220040676760476, 0.229921144042197, 0.239534571667654,
                    0.250082638090031, 0.25982958554362, 0.269843572653472,
                    0.270244132137866, 0.279991079591455, 0.289871546873176,
                    0.299752014154896, 0.300019053811159, 0.309632481436617,
                    0.309899521092879, 0.3197799883746, 0.329927495312583,
                    0.339941482422435, 0.349955469532286, 0.359835936814007,
                    0.359969456642138, 0.370116963580121, 0.380130950689973,
                    0.382400787768206, 0.385071184330833, 0.389744378315431,
                    0.390144937799825, 0.395085171440685, 0.400025405081545,
                    0.410039392191397, 0.419786339644986, 0.429666806926706,
                    0.430200886239232, 0.440214873349084, 0.449961820802673,
                    0.450095340630804])
real_speeds = real_froudes * np.sqrt(9.807*142)

real_r_t = np.array([0,16284.4782670025,16849.1550114651,22360.216699293,
                     27990.0843330943,27686.6898226365,32660.9432323375,
                     34077.1597832842,42701.2414167816,54211.8035430807,
                     62146.8631191253,78593.6950890453,75632.9591552314,
                     90663.0205901599,106173.442460792,106540.550063252,
                     126577.690136775,151334.444673086,150987.693406851,
                     168272.479562627,187743.512816745,213127.237207354,
                     233524.829365639,258250.775808028,288291.899018752,
                     317242.672986704,354322.46813325,388603.394808196,
                     423066.015909901,456762.678057169,452982.248897946,
                     518338.484982712,580641.568480829,638067.788844854,
                     636077.094338037,707911.171752567,704546.414129663,
                     759644.860608329,829695.061346214,900492.437270422,
                     979755.726393382,1083449.38686172,1083110.07062413,
                     1217341.73089021,1374335.69988256,1441676.72855747,
                     1484740.03069751,1568311.61844585,1582727.00359761,
                     1678253.26999036,1788110.18299234,2004793.74660511,
                     2227945.86438187,2471197.07196123,2470323.06762615,
                     2644444.79443997,2923361.78650161,2907661.3201144])

real_p_e = real_r_t * real_speeds

# Plotting
plt.figure(figsize=(10, 6))

# Plotting p_e
plt.plot(froudes, p_e, label='Effective Power (W)', color='magenta', marker = 'o')
plt.plot(real_froudes, real_p_e, label='Experimental Effective Power (W)' , color = 'blue', marker = '*')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Effective Power [W]')
plt.title('Effective Power vs Froudes Number (Fung Method)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()
"""

"""
import numpy as np
import matplotlib.pyplot as plt

speeds = np.array([0.000, 0.579, 1.157, 1.736, 2.315, 2.894, 3.472, 4.051, 4.630, 5.208,
    5.787, 6.366, 6.944, 7.523, 8.102, 8.681, 9.259, 9.838, 10.417, 10.995,
    11.574, 12.153, 12.731, 13.310, 13.889, 14.468, 15.046, 15.625, 16.204, 16.782])

froudes = speeds/np.sqrt(9.807*142)

holtrop_rt = np.array([0.000, 1.818E+03, 6.710E+03, 1.437E+04, 2.461E+04, 3.728E+04,
    5.224E+04, 6.937E+04, 8.862E+04, 1.100E+05, 1.338E+05, 1.602E+05,
    1.898E+05, 2.231E+05, 2.610E+05, 3.037E+05, 3.532E+05, 4.117E+05,
    4.754E+05, 5.379E+05, 6.042E+05, 6.799E+05, 7.732E+05, 8.929E+05,
    1.046E+06, 1.237E+06, 1.464E+06, 1.697E+06, 1.932E+06, 2.169E+06])


compton_rt = np.array([0.000E+00, 0.000E+00, 0.000E+00, 0.000E+00, 0.000E+00, 0.000E+00,
    0.000E+00, 7.516E+04, 9.677E+04, 1.209E+05, 1.477E+05, 1.777E+05,
    2.105E+05, 2.465E+05, 2.909E+05, 3.398E+05, 3.935E+05, 4.745E+05,
    5.695E+05, 6.764E+05, 7.861E+05, 9.013E+05, 1.027E+06, 1.194E+06,
    1.418E+06, 1.668E+06, 1.967E+06, 2.397E+06, 2.874E+06, 3.401E+06])

fung_rt = np.array([0.000E+00, 0.000E+00, 0.000E+00, 0.000E+00, 0.000E+00, 0.000E+00,
    0.000E+00, 0.000E+00, 0.000E+00, 1.044E+05, 1.304E+05, 1.607E+05,
    1.957E+05, 2.374E+05, 2.824E+05, 3.323E+05, 3.946E+05, 4.723E+05,
    5.619E+05, 6.555E+05, 7.492E+05, 8.498E+05, 9.715E+05, 1.130E+06,
    1.337E+06, 1.599E+06, 1.917E+06, 2.279E+06, 2.667E+06, 3.062E+06])

holtrop_pe = holtrop_rt * speeds
compton_pe = compton_rt * speeds
fung_pe = fung_rt * speeds

#######################################################################################################

real_froudes = np.array([0, 0.0498028958929961, 0.0499364157211275,
                    0.0592828036903225, 0.0700979097689624, 0.0700979097689624,
                    0.0746375839254285, 0.0798448572225514, 0.0898588443324032,
                    0.100006351270386, 0.109886818552107, 0.119900805661958,
                    0.12003432549009, 0.129781272943679, 0.139661740225399,
                    0.139795260053531, 0.150076286819645, 0.159823234273234,
                    0.160090273929497, 0.169837221383086, 0.179851208492938,
                    0.189998715430921, 0.200413262025167, 0.210160209478756,
                    0.220040676760476, 0.229921144042197, 0.239534571667654,
                    0.250082638090031, 0.25982958554362, 0.269843572653472,
                    0.270244132137866, 0.279991079591455, 0.289871546873176,
                    0.299752014154896, 0.300019053811159, 0.309632481436617,
                    0.309899521092879, 0.3197799883746, 0.329927495312583,
                    0.339941482422435, 0.349955469532286, 0.359835936814007,
                    0.359969456642138, 0.370116963580121, 0.380130950689973,
                    0.382400787768206, 0.385071184330833, 0.389744378315431,
                    0.390144937799825, 0.395085171440685, 0.400025405081545,
                    0.410039392191397, 0.419786339644986, 0.429666806926706,
                    0.430200886239232, 0.440214873349084, 0.449961820802673,
                    0.450095340630804])
real_speeds = real_froudes * np.sqrt(9.807*142)

real_r_t = np.array([0,16284.4782670025,16849.1550114651,22360.216699293,
                     27990.0843330943,27686.6898226365,32660.9432323375,
                     34077.1597832842,42701.2414167816,54211.8035430807,
                     62146.8631191253,78593.6950890453,75632.9591552314,
                     90663.0205901599,106173.442460792,106540.550063252,
                     126577.690136775,151334.444673086,150987.693406851,
                     168272.479562627,187743.512816745,213127.237207354,
                     233524.829365639,258250.775808028,288291.899018752,
                     317242.672986704,354322.46813325,388603.394808196,
                     423066.015909901,456762.678057169,452982.248897946,
                     518338.484982712,580641.568480829,638067.788844854,
                     636077.094338037,707911.171752567,704546.414129663,
                     759644.860608329,829695.061346214,900492.437270422,
                     979755.726393382,1083449.38686172,1083110.07062413,
                     1217341.73089021,1374335.69988256,1441676.72855747,
                     1484740.03069751,1568311.61844585,1582727.00359761,
                     1678253.26999036,1788110.18299234,2004793.74660511,
                     2227945.86438187,2471197.07196123,2470323.06762615,
                     2644444.79443997,2923361.78650161,2907661.3201144])

real_p_e = real_r_t * real_speeds

#######################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

# Plotting r_t
plt.plot(froudes, holtrop_rt, label='Holtrop Total Resistance', color='magenta', marker = '*')
plt.plot(froudes[7:], compton_rt[7:], label='Compton Total Resistance', color='red', marker = 'x')
plt.plot(froudes[9:], fung_rt[9:], label='Fung Total Resistance', color='orange', marker = 'o')
plt.plot(real_froudes, real_r_t, label='Experimental Total Resistance' , color = 'blue', marker = '.')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Total Resistance [N]')
plt.title('Maxsurf Total Resistance vs Froudes Number')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

# Plotting r_t
plt.plot(froudes, holtrop_pe, label='Holtrop Effective Power', color='magenta', marker = '*')
plt.plot(froudes[7:], compton_pe[7:], label='Compton Effective Power', color='red', marker = 'x')
plt.plot(froudes[9:], fung_pe[9:], label='Fung Effective Power', color='orange', marker = 'o')
plt.plot(real_froudes, real_p_e, label='Experimental Effective Power' , color = 'blue', marker = '.')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Effective Power [W]')
plt.title('Maxsurf Effective Power vs Froudes Number')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()
"""


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


# froudes = np.array([0.0498028958929961, 0.0499364157211275,
#                     0.0592828036903225, 0.0700979097689624, 0.0700979097689624,
#                     0.0746375839254285, 0.0798448572225514, 0.0898588443324032,
#                     0.100006351270386, 0.109886818552107, 0.119900805661958,
#                     0.12003432549009, 0.129781272943679, 0.139661740225399,
#                     0.139795260053531, 0.150076286819645, 0.159823234273234,
#                     0.160090273929497, 0.169837221383086, 0.179851208492938,
#                     0.189998715430921, 0.200413262025167, 0.210160209478756,
#                     0.220040676760476, 0.229921144042197, 0.239534571667654,
#                     0.250082638090031, 0.25982958554362, 0.269843572653472,
#                     0.270244132137866, 0.279991079591455, 0.289871546873176,
#                     0.299752014154896, 0.300019053811159, 0.309632481436617,
#                     0.309899521092879, 0.3197799883746, 0.329927495312583,
#                     0.339941482422435, 0.349955469532286, 0.359835936814007,
#                     0.359969456642138, 0.370116963580121, 0.380130950689973,
#                     0.382400787768206, 0.385071184330833, 0.389744378315431,
#                     0.390144937799825, 0.395085171440685, 0.400025405081545,
#                     0.410039392191397, 0.419786339644986, 0.429666806926706,
#                     0.430200886239232, 0.440214873349084, 0.449961820802673,
#                     0.450095340630804])


# real_cw = np.array([
#     1.718E-04, 2.636E-04, 1.317E-04, -1.300E-04, -1.594E-04, -3.030E-05,
#     -2.540E-04, -2.420E-04, -1.438E-04, -2.425E-04, -6.117E-05, -1.642E-04,
#     -7.462E-05, -2.124E-05, -1.693E-05, 8.690E-05, 2.528E-04, 2.376E-04,
#     2.302E-04, 2.355E-04, 3.015E-04, 2.769E-04, 3.087E-04, 3.753E-04,
#     4.125E-04, 5.092E-04, 5.420E-04, 5.802E-04, 5.961E-04, 5.632E-04,
#     7.698E-04, 9.234E-04, 1.026E-03, 1.009E-03, 1.171E-03, 1.149E-03,
#     1.203E-03, 1.306E-03, 1.397E-03, 1.506E-03, 1.690E-03, 1.686E-03,
#     1.946E-03, 2.252E-03, 2.419E-03, 2.495E-03, 2.647E-03, 2.682E-03,
#     2.854E-03, 3.059E-03, 3.424E-03, 3.774E-03, 4.135E-03, 4.117E-03,
#     4.267E-03, 4.651E-03, 4.610E-03
# ])


# real_cfs = np.array([
#     1.862E-03, 1.862E-03, 1.819E-03, 1.778E-03, 1.778E-03, 1.763E-03,
#     1.748E-03, 1.720E-03, 1.697E-03, 1.676E-03, 1.657E-03, 1.657E-03,
#     1.640E-03, 1.625E-03, 1.625E-03, 1.610E-03, 1.597E-03, 1.597E-03,
#     1.585E-03, 1.574E-03, 1.563E-03, 1.552E-03, 1.543E-03, 1.534E-03,
#     1.526E-03, 1.518E-03, 1.510E-03, 1.503E-03, 1.496E-03, 1.496E-03,
#     1.489E-03, 1.483E-03, 1.477E-03, 1.477E-03, 1.471E-03, 1.471E-03,
#     1.466E-03, 1.460E-03, 1.455E-03, 1.450E-03, 1.445E-03, 1.445E-03,
#     1.440E-03, 1.435E-03, 1.434E-03, 1.433E-03, 1.431E-03, 1.431E-03,
#     1.429E-03, 1.426E-03, 1.422E-03, 1.418E-03, 1.414E-03, 1.414E-03,
#     1.410E-03, 1.407E-03, 1.407E-03
# ])


# real_ct = np.array([
#     3.119E-03, 3.210E-03, 3.023E-03, 2.706E-03, 2.677E-03, 2.785E-03,
#     2.539E-03, 2.512E-03, 2.575E-03, 2.445E-03, 2.597E-03, 2.494E-03,
#     2.557E-03, 2.586E-03, 2.590E-03, 2.670E-03, 2.815E-03, 2.799E-03,
#     2.772E-03, 2.758E-03, 2.805E-03, 2.762E-03, 2.778E-03, 2.829E-03,
#     2.851E-03, 2.934E-03, 2.952E-03, 2.977E-03, 2.980E-03, 2.947E-03,
#     3.141E-03, 3.283E-03, 3.374E-03, 3.357E-03, 3.508E-03, 3.485E-03,
#     3.529E-03, 3.621E-03, 3.702E-03, 3.801E-03, 3.975E-03, 3.971E-03,
#     4.222E-03, 4.519E-03, 4.684E-03, 4.757E-03, 4.905E-03, 4.940E-03,
#     5.108E-03, 5.309E-03, 5.665E-03, 6.007E-03, 6.359E-03, 6.341E-03,
#     6.483E-03, 6.860E-03, 6.819E-03
# ])

# real_r_t = np.array([16284.4782670025,16849.1550114651,22360.216699293,
#                      27990.0843330943,27686.6898226365,32660.9432323375,
#                      34077.1597832842,42701.2414167816,54211.8035430807,
#                      62146.8631191253,78593.6950890453,75632.9591552314,
#                      90663.0205901599,106173.442460792,106540.550063252,
#                      126577.690136775,151334.444673086,150987.693406851,
#                      168272.479562627,187743.512816745,213127.237207354,
#                      233524.829365639,258250.775808028,288291.899018752,
#                      317242.672986704,354322.46813325,388603.394808196,
#                      423066.015909901,456762.678057169,452982.248897946,
#                      518338.484982712,580641.568480829,638067.788844854,
#                      636077.094338037,707911.171752567,704546.414129663,
#                      759644.860608329,829695.061346214,900492.437270422,
#                      979755.726393382,1083449.38686172,1083110.07062413,
#                      1217341.73089021,1374335.69988256,1441676.72855747,
#                      1484740.03069751,1568311.61844585,1582727.00359761,
#                      1678253.26999036,1788110.18299234,2004793.74660511,
#                      2227945.86438187,2471197.07196123,2470323.06762615,
#                      2644444.79443997,2923361.78650161,2907661.3201144])




# # Plotting
# plt.figure(figsize=(10, 6))

# # Plotting r_t
# plt.plot(froudes, real_cw, label='Wave Resistance Coefficient', color='blue', marker = '*')
# plt.plot(froudes, real_ct, label='Total Resistance Coefficient', color='red', marker = 'x')
# plt.plot(froudes, real_cfs, label='Friction Resistance Coefficient', color='green', marker = 'o')

# # Adding labels and title
# plt.xlabel('Froudes Number')
# plt.ylabel('Resistance Coefficients ')
# plt.title('Total, Viscous and Wave Resistance Coefficients as a function of Froude number ')
# plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
# plt.legend()

# # Show the plot
# plt.show()


# # Plotting
# plt.figure(figsize=(10, 6))

# # Plotting r_t
# plt.plot(froudes, real_r_t, label='Total Resistance [N]', color='red', marker = 'o')

# # Adding labels and title
# plt.xlabel('Froudes Number')
# plt.ylabel('Resitance Forces [N] ')
# plt.title('Resitance Forces vs Froude number ')
# plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
# plt.legend()

# # Show the plot
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import r2_score

# X = np.array([
#     0.002, 0.002, 0.003, 0.006, 0.006, 0.008, 0.011, 0.018, 0.029, 0.042,
#     0.061, 0.061, 0.085, 0.116, 0.116, 0.156, 0.203, 0.205, 0.262, 0.333,
#     0.419, 0.523, 0.638, 0.773, 0.929, 1.102, 1.319, 1.547, 1.812, 1.823,
#     2.113, 2.442, 2.808, 2.819, 3.215, 3.227, 3.678, 4.189, 4.746, 5.356,
#     6.015, 6.024, 6.764, 7.560, 7.750, 7.978, 8.389, 8.425, 8.879, 9.350,
#     10.365, 11.430, 12.593, 12.659, 13.932, 15.262, 15.281
# ])

# Y = np.array([
#     1.234, 1.257, 1.225, 1.156, 1.148, 1.183, 1.121, 1.123, 1.150, 1.120,
#     1.173, 1.142, 1.169, 1.185, 1.186, 1.218, 1.270, 1.265, 1.264, 1.266,
#     1.288, 1.281, 1.292, 1.315, 1.328, 1.361, 1.374, 1.388, 1.395, 1.383,
#     1.456, 1.510, 1.548, 1.542, 1.601, 1.593, 1.614, 1.653, 1.687, 1.729,
#     1.797, 1.796, 1.892, 2.006, 2.068, 2.096, 2.153, 2.166, 2.231, 2.308,
#     2.446, 2.580, 2.719, 2.713, 2.774, 2.923, 2.907
# ])

# # Kullanıcıdan polinom derecesini alalım
# derece = int(input("Kullanmak istediğiniz polinomun derecesini belirtin: "))

# # En küçük kareler yöntemiyle polinom katsayılarını hesaplayalım
# katsayilar = np.polyfit(X, Y, derece)

# # X değerlerine karşılık gelen Y değerlerini hesaplayalım
# Y_tahmin = np.polyval(katsayilar, X)

# # R^2 skorunu hesaplayalım
# r2_skoru = r2_score(Y, Y_tahmin)

# # Grafik çizelim
# plt.figure(figsize=(10, 6))
# plt.scatter(X, Y, color='blue')
# plt.plot(X, Y_tahmin, label=f'{derece}. derece Polinom Eğrisi', color='red')

# # R^2 skorunu ve polinom denklemini grafikte yazdıralım
# denklem = np.poly1d(katsayilar)
# denklem_str = f'Denklem: {denklem}\nR^2 Skoru: {r2_skoru:.4f}'
# plt.text(0.5, 2, denklem_str, fontsize=10, ha='left')

# plt.legend()
# plt.xlabel('X = Fr^4/Cf')
# plt.ylabel('Y = Ct/Cf')
# plt.title("Prohaska's Graphic")
# plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
# plt.legend(loc='lower right')
# plt.show()



























