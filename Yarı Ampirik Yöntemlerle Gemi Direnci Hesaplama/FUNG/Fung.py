# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 21:52:29 2023

@author: uygur
"""


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

length_bp = (float(input('Enter Lbp: ')))*3.2808399  # Length between perpendicular
length_wl = (float(input('Enter LwL: ')))*3.2808399   # Waterline length
beam = (float(input('Enter B: ')))*3.2808399  # Beam
beam_tw = (float(input('Enter B at 20th station: ')))*3.2808399
depth = (float(input('Enter D: ')))*3.2808399   # Depth
depth_tw = (float(input('Enter depth at 20: ')))
t_a = (float(input('Enter Ta: ')))*3.2808399   # Aft Draught
t_f = (float(input('Enter Tf: ')))*3.2808399  # Forward Draught
t = (t_a + t_f) / 2  # Midship Draught
g = 9.807  # Gravity [km/s^2]
rho = 1025  # Density [kg/m^3]
s = (float(input('Enter Wetted Surface Area, S: ')))*(3.2808399**2)  # Wetted Surface Area
disp_v = float(input('Enter the displacement volume: ')) #Displacement Volume
a_m = float(input('Enter the midship section area: '))*(3.2808399**2) #Midship Section Area
a_tw =float(input('Enter the section area at 20th station: '))*(3.2808399**2)
a_w = float(input('Enter the waterplane section area: '))*(3.2808399**2) #Waterplane Area
abt = float(input('Enter Transverse Area of Bulb: '))*(3.2808399**2)
l_CB = float(input('Enter Longitudinal Center of Buoyancy: '))*3.2808399

#######################################################################################################
#DISPLACEMENT 
disp = (disp_v * (rho/1025)) #Displacement [t]

#######################################################################################################
#FORM COEFFICENTS
c_b = disp_v / ((length_wl/3.2808399) * (beam/3.2808399) * (t/3.2808399)) #Block Coefficient
c_p = disp_v / ((length_wl/3.2808399) * (a_m/3.2808399**2)) #Prismatic Coefficient
c_wp = (a_w/3.2808399**2) / ((length_wl/3.2808399)*(beam/3.2808399)) #WaterPlane Area Coefficient
c_m = (a_m/3.2808399**2) / ((beam/3.2808399) * (t/3.2808399)) #MidshipSection Coefficient

my_DL = disp/(length_wl/3.2808399)
my_FB = l_CB/length_wl
my_TW = beam_tw/beam
my_BT = beam/t
my_TA = a_tw/a_m
my_TT = depth_tw/depth
my_BA = abt/a_m
my_CWS = s/np.sqrt(length_wl*((disp*0.984207)))
mycp = c_p
mycm = c_m

#######################################################################################################
#HALF OF ANGLE OF ENTRANCE
iE = 120.019 + (69.2808/my_DL) + (0.1131*(length_wl/beam)) + (104.8640/(length_wl/beam)) - (28.5611*c_p) - (26.5287/c_p) - (24.8166*c_m) - (16.2033/c_m) + (2.6398*my_TW) - (49.6570*my_FB)
myiE = iE

#######################################################################################################

# FROUDES NUMBERS
froudes = np.array([0, 0.0498028958929961, 0.0499364157211275,
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

speeds = froudes * np.sqrt(g *  (length_wl/3.2808399))
reynolds = (speeds * (length_wl/3.2808399)) / (1.1892 * (10**(-6)))
speed_knot = speeds / 0.5144

#######################################################################################################

#THE FRICTION RESISTANCE COEFFICIENT
c_f = 0.075 / (np.log10(reynolds) - 2)**2
#FRICTION RESISTANCE
r_f = 0.5 * rho * (speeds**2) * c_f * (s/(3.2808399**2))

all_VL =  speed_knot / np.sqrt(length_wl)
my_VL = all_VL[all_VL >= 0.6]

######################################################################################################################################################################################################
######################################################################################################################################################################################################


#CR DEĞERLERİNİN BELİRLENMESİ

# CR1 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR1 = []

# Kullanıcının girdiği x değerini alın
x_value_CR1 = my_DL

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR1 in range(1, 4):
    # Dosya adını oluşturma
    file_name_CR1 = f"CR{file_number_CR1}.txt"
    
    try:
        # Verileri yükleme
        data_CR1 = np.loadtxt(file_name_CR1, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR1 = data_CR1.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR1 = 5

        # DL (x) ve y değerlerini ayırma
        DL = data_CR1[:, 0]
        y_values_CR1 = data_CR1[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR1 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR1 - 1):
            y_CR1 = y_values_CR1[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR1 = ~np.isnan(y_CR1) & (y_CR1 != 0)
            valid_DL = DL[valid_indices_CR1]
            valid_y_CR1 = y_CR1[valid_indices_CR1]

            if len(valid_DL) > 0:  # Eğer geçerli DL değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR1 = np.polyfit(valid_DL, valid_y_CR1, degree_CR1)
                polynomial_CR1 = np.poly1d(model_CR1)

                # R^2 değerini hesaplama
                y_pred_CR1 = polynomial_CR1(valid_DL)
                r2 = r2_score(valid_y_CR1, y_pred_CR1)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR1 in DL:
                    index_CR1 = np.where(DL == x_value_CR1)[0][0]
                    if not np.isnan(y_values_CR1[index_CR1, i]) and y_values_CR1[index_CR1, i] != 0:
                        predictions_array_CR1.append(y_values_CR1[index_CR1, i])
                    else:
                        predictions_array_CR1.append(None)
                else:
                    prediction_CR1 = polynomial_CR1(x_value_CR1)
                    predictions_array_CR1.append(prediction_CR1)
            else:
                print(f"1.{i} - Geçerli DL değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR1 = np.array(predictions_array_CR1)
        print(f"{file_name_CR1} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR1)
        all_predictions_array_CR1.extend(predictions_array_CR1)

    except Exception as e:
        print(f"{file_name_CR1} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR1 = np.array(all_predictions_array_CR1)



######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR2 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR2 = []

# Kullanıcının girdiği x değerini alın
x_value_CR2 = my_BT

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR2 in range(4, 7):
    # Dosya adını oluşturma
    file_name_CR2 = f"CR{file_number_CR2}.txt"
    
    try:
        # Verileri yükleme
        data_CR2 = np.loadtxt(file_name_CR2, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR2 = data_CR2.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR2 = 5

        # BT (x) ve y değerlerini ayırma
        BT = data_CR2[:, 0]
        y_values_CR2 = data_CR2[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR2 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR2 - 1):
            y_CR2 = y_values_CR2[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR2 = ~np.isnan(y_CR2) & (y_CR2 != 0)
            valid_BT = BT[valid_indices_CR2]
            valid_y_CR2 = y_CR2[valid_indices_CR2]

            if len(valid_BT) > 0:  # Eğer geçerli BT değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR2 = np.polyfit(valid_BT, valid_y_CR2, degree_CR2)
                polynomial_CR2 = np.poly1d(model_CR2)

                # R^2 değerini hesaplama
                y_pred_CR2 = polynomial_CR2(valid_BT)
                r2 = r2_score(valid_y_CR2, y_pred_CR2)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR2 in BT:
                    index_CR2 = np.where(BT == x_value_CR2)[0][0]
                    if not np.isnan(y_values_CR2[index_CR2, i]) and y_values_CR2[index_CR2, i] != 0:
                        predictions_array_CR2.append(y_values_CR2[index_CR2, i])
                    else:
                        predictions_array_CR2.append(None)
                else:
                    prediction_CR2 = polynomial_CR2(x_value_CR2)
                    predictions_array_CR2.append(prediction_CR2)
            else:
                print(f"1.{i} - Geçerli BT değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR2 = np.array(predictions_array_CR2)
        print(f"{file_name_CR2} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR2)
        all_predictions_array_CR2.extend(predictions_array_CR2)

    except Exception as e:
        print(f"{file_name_CR2} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR2 = np.array(all_predictions_array_CR2)

######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR3 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR3 = []

# Kullanıcının girdiği x değerini alın
x_value_CR3 = mycp

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR3 in range(7, 10):
    # Dosya adını oluşturma
    file_name_CR3 = f"CR{file_number_CR3}.txt"
    
    try:
        # Verileri yükleme
        data_CR3 = np.loadtxt(file_name_CR3, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR3 = data_CR3.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR3 = 5

        # Cp (x) ve y değerlerini ayırma
        mycp = data_CR3[:, 0]
        y_values_CR3 = data_CR3[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR3 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR3 - 1):
            y_CR3 = y_values_CR3[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR3 = ~np.isnan(y_CR3) & (y_CR3 != 0)
            valid_mycp = mycp[valid_indices_CR3]
            valid_y_CR3 = y_CR3[valid_indices_CR3]

            if len(valid_mycp) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR3 = np.polyfit(valid_mycp, valid_y_CR3, degree_CR3)
                polynomial_CR3 = np.poly1d(model_CR3)

                # R^2 değerini hesaplama
                y_pred_CR3 = polynomial_CR3(valid_mycp)
                r2 = r2_score(valid_y_CR3, y_pred_CR3)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR3 in mycp:
                    index_CR3 = np.where(mycp == x_value_CR3)[0][0]
                    if not np.isnan(y_values_CR3[index_CR3, i]) and y_values_CR3[index_CR3, i] != 0:
                        predictions_array_CR3.append(y_values_CR3[index_CR3, i])
                    else:
                        predictions_array_CR3.append(None)
                else:
                    prediction_CR3 = polynomial_CR3(x_value_CR3)
                    predictions_array_CR3.append(prediction_CR3)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR3 = np.array(predictions_array_CR3)
        print(f"{file_name_CR3} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR3)
        all_predictions_array_CR3.extend(predictions_array_CR3)

    except Exception as e:
        print(f"{file_name_CR3} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR3 = np.array(all_predictions_array_CR3)

######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR4 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR4 = []

# Kullanıcının girdiği x değerini alın
x_value_CR4 = mycm

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR4 in range(10, 13):
    # Dosya adını oluşturma
    file_name_CR4 = f"CR{file_number_CR4}.txt"
    
    try:
        # Verileri yükleme
        data_CR4 = np.loadtxt(file_name_CR4, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR4 = data_CR4.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR4 = 5

        # Cp (x) ve y değerlerini ayırma
        mycm = data_CR4[:, 0]
        y_values_CR4 = data_CR4[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR4 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR4 - 1):
            y_CR4 = y_values_CR4[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR4 = ~np.isnan(y_CR4) & (y_CR4 != 0)
            valid_mycm = mycm[valid_indices_CR4]
            valid_y_CR4 = y_CR4[valid_indices_CR4]

            if len(valid_mycm) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR4 = np.polyfit(valid_mycm, valid_y_CR4, degree_CR4)
                polynomial_CR4 = np.poly1d(model_CR4)

                # R^2 değerini hesaplama
                y_pred_CR4 = polynomial_CR4(valid_mycm)
                r2 = r2_score(valid_y_CR4, y_pred_CR4)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR4 in mycm:
                    index_CR4 = np.where(mycm == x_value_CR4)[0][0]
                    if not np.isnan(y_values_CR4[index_CR4, i]) and y_values_CR4[index_CR4, i] != 0:
                        predictions_array_CR4.append(y_values_CR4[index_CR4, i])
                    else:
                        predictions_array_CR4.append(None)
                else:
                    prediction_CR4 = polynomial_CR4(x_value_CR4)
                    predictions_array_CR4.append(prediction_CR4)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR4 = np.array(predictions_array_CR4)
        print(f"{file_name_CR4} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR4)
        all_predictions_array_CR4.extend(predictions_array_CR4)

    except Exception as e:
        print(f"{file_name_CR4} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR4 = np.array(all_predictions_array_CR4)


######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR5 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR5 = []

# Kullanıcının girdiği x değerini alın
x_value_CR5 = myiE

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR5 in range(13, 16):
    # Dosya adını oluşturma
    file_name_CR5 = f"CR{file_number_CR5}.txt"
    
    try:
        # Verileri yükleme
        data_CR5 = np.loadtxt(file_name_CR5, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR5 = data_CR5.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR5 = 5

        # Cp (x) ve y değerlerini ayırma
        myiE = data_CR5[:, 0]
        y_values_CR5 = data_CR5[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR5 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR5 - 1):
            y_CR5 = y_values_CR5[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR5 = ~np.isnan(y_CR5) & (y_CR5 != 0)
            valid_myiE = myiE[valid_indices_CR5]
            valid_y_CR5 = y_CR5[valid_indices_CR5]

            if len(valid_myiE) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR5 = np.polyfit(valid_myiE, valid_y_CR5, degree_CR5)
                polynomial_CR5 = np.poly1d(model_CR5)

                # R^2 değerini hesaplama
                y_pred_CR5 = polynomial_CR5(valid_myiE)
                r2 = r2_score(valid_y_CR5, y_pred_CR5)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR5 in myiE:
                    index_CR5 = np.where(myiE == x_value_CR5)[0][0]
                    if not np.isnan(y_values_CR5[index_CR5, i]) and y_values_CR5[index_CR5, i] != 0:
                        predictions_array_CR5.append(y_values_CR5[index_CR5, i])
                    else:
                        predictions_array_CR5.append(None)
                else:
                    prediction_CR5 = polynomial_CR5(x_value_CR5)
                    predictions_array_CR5.append(prediction_CR5)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR5 = np.array(predictions_array_CR5)
        print(f"{file_name_CR5} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR5)
        all_predictions_array_CR5.extend(predictions_array_CR5)

    except Exception as e:
        print(f"{file_name_CR5} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR5 = np.array(all_predictions_array_CR5)


######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR6 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR6 = []

# Kullanıcının girdiği x değerini alın
x_value_CR6 = my_TA

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR6 in range(16, 19):
    # Dosya adını oluşturma
    file_name_CR6 = f"CR{file_number_CR6}.txt"
    
    try:
        # Verileri yükleme
        data_CR6 = np.loadtxt(file_name_CR6, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR6 = data_CR6.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR6 = 5

        # Cp (x) ve y değerlerini ayırma
        my_TA = data_CR6[:, 0]
        y_values_CR6 = data_CR6[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR6 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR6 - 1):
            y_CR6 = y_values_CR6[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR6 = ~np.isnan(y_CR6) & (y_CR6 != 0)
            valid_my_TA = my_TA[valid_indices_CR6]
            valid_y_CR6 = y_CR6[valid_indices_CR6]

            if len(valid_my_TA) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR6 = np.polyfit(valid_my_TA, valid_y_CR6, degree_CR6)
                polynomial_CR6 = np.poly1d(model_CR6)

                # R^2 değerini hesaplama
                y_pred_CR6 = polynomial_CR6(valid_my_TA)
                r2 = r2_score(valid_y_CR6, y_pred_CR6)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR6 in my_TA:
                    index_CR6 = np.where(my_TA == x_value_CR6)[0][0]
                    if not np.isnan(y_values_CR6[index_CR6, i]) and y_values_CR6[index_CR6, i] != 0:
                        predictions_array_CR6.append(y_values_CR6[index_CR6, i])
                    else:
                        predictions_array_CR6.append(None)
                else:
                    prediction_CR6 = polynomial_CR6(x_value_CR6)
                    predictions_array_CR6.append(prediction_CR6)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR6 = np.array(predictions_array_CR6)
        print(f"{file_name_CR6} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR6)
        all_predictions_array_CR6.extend(predictions_array_CR6)

    except Exception as e:
        print(f"{file_name_CR6} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR6 = np.array(all_predictions_array_CR6)


######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR7 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR7 = []

# Kullanıcının girdiği x değerini alın
x_value_CR7 = my_TW

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR7 in range(19, 22):
    # Dosya adını oluşturma
    file_name_CR7 = f"CR{file_number_CR7}.txt"
    
    try:
        # Verileri yükleme
        data_CR7 = np.loadtxt(file_name_CR7, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR7 = data_CR7.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR7 = 5

        # Cp (x) ve y değerlerini ayırma
        my_TW = data_CR7[:, 0]
        y_values_CR7 = data_CR7[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR7 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR7 - 1):
            y_CR7 = y_values_CR7[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR7 = ~np.isnan(y_CR7) & (y_CR7 != 0)
            valid_my_TW = my_TW[valid_indices_CR7]
            valid_y_CR7 = y_CR7[valid_indices_CR7]

            if len(valid_my_TW) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR7 = np.polyfit(valid_my_TW, valid_y_CR7, degree_CR7)
                polynomial_CR7 = np.poly1d(model_CR7)

                # R^2 değerini hesaplama
                y_pred_CR7 = polynomial_CR7(valid_my_TW)
                r2 = r2_score(valid_y_CR7, y_pred_CR7)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR7 in my_TW:
                    index_CR7 = np.where(my_TW == x_value_CR7)[0][0]
                    if not np.isnan(y_values_CR7[index_CR7, i]) and y_values_CR7[index_CR7, i] != 0:
                        predictions_array_CR7.append(y_values_CR7[index_CR7, i])
                    else:
                        predictions_array_CR7.append(None)
                else:
                    prediction_CR7 = polynomial_CR7(x_value_CR7)
                    predictions_array_CR7.append(prediction_CR7)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR7 = np.array(predictions_array_CR7)
        print(f"{file_name_CR7} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR7)
        all_predictions_array_CR7.extend(predictions_array_CR7)

    except Exception as e:
        print(f"{file_name_CR7} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR7 = np.array(all_predictions_array_CR7)

######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR8 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR8 = []

# Kullanıcının girdiği x değerini alın
x_value_CR8 = my_TT

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR8 in range(22, 25):
    # Dosya adını oluşturma
    file_name_CR8 = f"CR{file_number_CR8}.txt"
    
    try:
        # Verileri yükleme
        data_CR8 = np.loadtxt(file_name_CR8, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR8 = data_CR8.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR8 = 5

        # Cp (x) ve y değerlerini ayırma
        my_TT = data_CR8[:, 0]
        y_values_CR8 = data_CR8[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR8 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR8 - 1):
            y_CR8 = y_values_CR8[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR8 = ~np.isnan(y_CR8) & (y_CR8 != 0)
            valid_my_TT = my_TT[valid_indices_CR8]
            valid_y_CR8 = y_CR8[valid_indices_CR8]

            if len(valid_my_TT) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR8 = np.polyfit(valid_my_TT, valid_y_CR8, degree_CR8)
                polynomial_CR8 = np.poly1d(model_CR8)

                # R^2 değerini hesaplama
                y_pred_CR8 = polynomial_CR8(valid_my_TT)
                r2 = r2_score(valid_y_CR8, y_pred_CR8)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR8 in my_TT:
                    index_CR8 = np.where(my_TT == x_value_CR8)[0][0]
                    if not np.isnan(y_values_CR8[index_CR8, i]) and y_values_CR8[index_CR8, i] != 0:
                        predictions_array_CR8.append(y_values_CR8[index_CR8, i])
                    else:
                        predictions_array_CR8.append(None)
                else:
                    prediction_CR8 = polynomial_CR8(x_value_CR8)
                    predictions_array_CR8.append(prediction_CR8)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR8 = np.array(predictions_array_CR8)
        print(f"{file_name_CR8} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR8)
        all_predictions_array_CR8.extend(predictions_array_CR8)

    except Exception as e:
        print(f"{file_name_CR8} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR8 = np.array(all_predictions_array_CR8)

######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR9 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR9 = []

# Kullanıcının girdiği x değerini alın
x_value_CR9 = my_BA

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR9 in range(25, 28):
    # Dosya adını oluşturma
    file_name_CR9 = f"CR{file_number_CR9}.txt"
    
    try:
        # Verileri yükleme
        data_CR9 = np.loadtxt(file_name_CR9, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR9 = data_CR9.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR9 = 5

        # Cp (x) ve y değerlerini ayırma
        my_BA = data_CR9[:, 0]
        y_values_CR9 = data_CR9[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR9 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR9 - 1):
            y_CR9 = y_values_CR9[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR9 = ~np.isnan(y_CR9) & (y_CR9 != 0)
            valid_my_BA = my_BA[valid_indices_CR9]
            valid_y_CR9 = y_CR9[valid_indices_CR9]

            if len(valid_my_BA) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR9 = np.polyfit(valid_my_BA, valid_y_CR9, degree_CR9)
                polynomial_CR9 = np.poly1d(model_CR9)

                # R^2 değerini hesaplama
                y_pred_CR9 = polynomial_CR9(valid_my_BA)
                r2 = r2_score(valid_y_CR9, y_pred_CR9)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR9 in my_BA:
                    index_CR9 = np.where(my_BA == x_value_CR9)[0][0]
                    if not np.isnan(y_values_CR9[index_CR9, i]) and y_values_CR9[index_CR9, i] != 0:
                        predictions_array_CR9.append(y_values_CR9[index_CR9, i])
                    else:
                        predictions_array_CR9.append(None)
                else:
                    prediction_CR9 = polynomial_CR9(x_value_CR9)
                    predictions_array_CR9.append(prediction_CR9)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR9 = np.array(predictions_array_CR9)
        print(f"{file_name_CR9} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR9)
        all_predictions_array_CR9.extend(predictions_array_CR9)

    except Exception as e:
        print(f"{file_name_CR9} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR9 = np.array(all_predictions_array_CR9)

array_size_CR9 = len(all_predictions_array_CR9)

while array_size_CR9 < 18:
    all_predictions_array_CR9 = np.append(all_predictions_array_CR9, 0)
    array_size_CR9 += 1

######################################################################################################################################################################################################
######################################################################################################################################################################################################

# CR10 DEĞERİNİN BELİRLENMESİ

# Tüm tahmin değerlerini tutacak ana array
all_predictions_array_CR10 = []

# Kullanıcının girdiği x değerini alın
x_value_CR10 = my_CWS

# Her bir dosya için işlemleri gerçekleştirme
for file_number_CR10 in range(28, 31):
    # Dosya adını oluşturma
    file_name_CR10 = f"CR{file_number_CR10}.txt"
    
    try:
        # Verileri yükleme
        data_CR10 = np.loadtxt(file_name_CR10, skiprows=1, usecols=range(7))

        # Sütun sayısını belirleme
        num_columns_CR10 = data_CR10.shape[1]

        # Kullanıcıdan eğri derecesini alın
        degree_CR10 = 5

        # Cp (x) ve y değerlerini ayırma
        my_CWS = data_CR10[:, 0]
        y_values_CR10 = data_CR10[:, 1:]

        # Tahmin edilen değerleri tutacak array'leri oluştur
        predictions_array_CR10 = []

        # Her bir y değeri için ayrı ayrı işlemler yapma
        for i in range(num_columns_CR10 - 1):
            y_CR10 = y_values_CR10[:, i]

            # NaN veya sıfır olmayan değerlere sahip satırları seçme
            valid_indices_CR10 = ~np.isnan(y_CR10) & (y_CR10 != 0)
            valid_my_CWS = my_CWS[valid_indices_CR10]
            valid_y_CR10 = y_CR10[valid_indices_CR10]

            if len(valid_my_CWS) > 0:  # Eğer geçerli Cp değerleri varsa işlem yap
                # Polynomial Regression modeli oluşturma
                model_CR10 = np.polyfit(valid_my_CWS, valid_y_CR10, degree_CR10)
                polynomial_CR10 = np.poly1d(model_CR10)

                # R^2 değerini hesaplama
                y_pred_CR10 = polynomial_CR10(valid_my_CWS)
                r2 = r2_score(valid_y_CR10, y_pred_CR10)

                # Tahmin değerini predictions_array'e ekle
                if x_value_CR10 in my_CWS:
                    index_CR10 = np.where(my_CWS == x_value_CR10)[0][0]
                    if not np.isnan(y_values_CR10[index_CR10, i]) and y_values_CR10[index_CR10, i] != 0:
                        predictions_array_CR10.append(y_values_CR10[index_CR10, i])
                    else:
                        predictions_array_CR10.append(None)
                else:
                    prediction_CR10 = polynomial_CR10(x_value_CR10)
                    predictions_array_CR10.append(prediction_CR10)
            else:
                print(f"1.{i} - Geçerli Cp değeri yok, dolayısıyla işlem yapılamıyor.")

        predictions_array_CR10 = np.array(predictions_array_CR10)
        print(f"{file_name_CR10} için Her bir sütun için tahmin edilen değerler:", predictions_array_CR10)
        all_predictions_array_CR10.extend(predictions_array_CR10)

    except Exception as e:
        print(f"{file_name_CR10} dosyası bulunamadı veya işlenirken bir hata oluştu: {e}")


#######################################################################################################
#######################################################################################################

# Tüm dosyalar için toplu tahmin array'i
all_predictions_array_CR10 = np.array(all_predictions_array_CR10)

org_VL = np.array([0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3])


# İki tek sütunlu array'leri düşey olarak birleştirme
CR_result = np.concatenate((org_VL,
                          all_predictions_array_CR1, 
                          all_predictions_array_CR2,
                          all_predictions_array_CR3,
                          all_predictions_array_CR4,
                          all_predictions_array_CR5,
                          all_predictions_array_CR6,
                          all_predictions_array_CR7,
                          all_predictions_array_CR8,
                          all_predictions_array_CR9,
                          all_predictions_array_CR10), axis=0)

# Birleştirilmiş sütunlu array'i oluşturma
CR_result_column = np.column_stack((org_VL.flatten(), 
                                      all_predictions_array_CR1.flatten(), 
                                      all_predictions_array_CR2.flatten(), 
                                      all_predictions_array_CR3.flatten(),
                                      all_predictions_array_CR4.flatten(),
                                      all_predictions_array_CR5.flatten(),
                                      all_predictions_array_CR6.flatten(),
                                      all_predictions_array_CR7.flatten(),
                                      all_predictions_array_CR8.flatten(),
                                      all_predictions_array_CR9.flatten(),
                                      all_predictions_array_CR10.flatten()))




# Veriyi düzenle ve x, y değerlerini ayır
x_values = CR_result_column[:, 0]
y_values = CR_result_column[:, 1:]

# Derecesini kullanıcıdan al
degree = 10

# Tahmin yapacak x değerlerini belirle
predict_x = my_VL.reshape(-1, 1)

# Tahminleri saklamak için bir dizi oluştur
result = np.zeros((len(my_VL), y_values.shape[1] + 1))

# İlk sütuna all_VL değerlerini ekle
result[:, 0] = my_VL

# Her bir y değeri için regresyon modelini oluştur ve tahmin yap
for i in range(y_values.shape[1]):
    y = y_values[:, i]
    
    # Sıfır olan değerleri kontrol et
    zero_indices = np.where(y == 0)[0]
    
    # Sıfır olmayan değerleri kullanarak regresyon yap
    non_zero_x = x_values[y != 0]
    non_zero_y = y[y != 0]
    
    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(non_zero_x.reshape(-1, 1))
    predict_x_poly = poly_features.transform(predict_x)
    
    model = LinearRegression()
    model.fit(x_poly, non_zero_y)
    
    predictions = model.predict(predict_x_poly)
    
    # Sonuçları result dizisine ekle
    result[:, i + 1] = predictions
    
values_of_CR = result[:, 1:]
row_sums = (np.sum(values_of_CR, axis=1))/1000

#######################################################################################################
#######################################################################################################


#TOTAL RESISTANCE
C_t = (c_f[20:]*1.190997) + row_sums + 0.0004
calc_speeds = speeds[20:]
R_t = 0.5 * C_t.reshape(-1, 1) * rho * (calc_speeds.reshape(-1, 1)**2) * (s/(3.2808399**2))

#######################################################################################################

#EFFECTIVE POWER
# p_e = R_t * speeds[20:]

#######################################################################################################

#EXPERIMENTAL RESULTS
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

real_p_e = real_r_t * speeds


#######################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

# Plotting r_t
plt.plot(froudes[20:], R_t, label='Total Resistance', color='magenta', marker = 'o')
plt.plot(froudes, real_r_t, label='Experimental Total Resistance' , color = 'blue', marker = '*')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Total Resistance [N]')
plt.title('Total Resistance vs Froudes Number (Fung Method)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# # Plotting
# plt.figure(figsize=(10, 6))

# # Plotting p_e
# plt.plot(froudes[20:], p_e, label='Effective Power (W)', color='magenta', marker = 'o')
# plt.plot(froudes, real_p_e, label='Experimental Effective Power (W)' , color = 'blue', marker = '*')

# # Adding labels and title
# plt.xlabel('Froudes Number')
# plt.ylabel('Effective Power [W]')
# plt.title('Effective Power vs Froudes Number (Fung Method)')
# plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
# plt.legend()

# # Show the plot
# plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(froudes[20:], C_t, label='Total Resistance Coefficient (N)', color='red', marker = 'o')
plt.plot(froudes[20:], c_f[20:], label='Friction Resistance Coefficient (N)', color='green', marker = 'o')
plt.plot(froudes[20:], row_sums, label='Residuary Resistance Coefficient(N)', color='blue', marker = 'o')

# Adding labels and title
plt.xlabel('Froudes Numbers')
plt.ylabel('Resistance Coefficients [N]')
plt.title('Total, Viscous and Wave Resistance Coefficients as a function of Froude number (Fung Method)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend(loc='best')

# Show the plot
plt.show()