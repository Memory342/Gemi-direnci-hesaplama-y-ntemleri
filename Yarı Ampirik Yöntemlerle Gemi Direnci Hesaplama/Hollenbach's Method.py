# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:02:58 2023

@author: uygur
"""


import numpy as np
import math
import matplotlib.pyplot as plt


#Required and optional input parameters for Hollenbach's Method
length_os = float(input('Enter Los: ')) #Length over wetted surface
length_bp = float(input('Enter Lbp: ')) #Length between perpendicıler
length_wl = float(input('Enter LwL: ')) #Waterline length
beam = float(input('Enter B: ')) #Beam
depth = float(input('Enter D: ')) #Depth
t_a = float(input('Enter Ta: ')) #Aft Draught
t_f = float(input('Enter Tf: ')) #Forward Draught
g = 9.807 #Gravity [km/s^2]
rho = 1025 #Density [kg/m^3]

t = (t_a + t_f)/2 # Mean Draught

s = float(input('Enter Wetted Surface Area, S: '))
s_app = float(input('Enter App. Wetted Surface Area, S: '))
c_b = float(input('Enter Cb: ')) #Block Coefficient
c_p = float(input('Enter Cp: ')) #Prismatic Coefficient
c_w = float(input('Enter Cw: ')) #Waterplane Coeffcient
a_v = float(input('Enter transverse vertical area above WL, Av: '))

#############################################################################################################################################

#A Calculation length, Lc
if length_os > length_bp:
    length_c = length_os
elif (length_bp < length_os < 11*length_bp):
    length_c = length_bp + ((2/3)*(length_os-length_bp))
elif length_os > 11*length_bp:
    length_c = 1.0667*length_bp

#############################################################################################################################################

#Coefficients for an estimate of the wetted surface for twin propeller vessel at DWL    
s0 = -0.4319
s1 = 0.1685
s2 = 0.5637
s3 = 0.5891
s4 = 0.0033
s5 = 0.0134
s6 = -0.0005
s7 = -2.7932
s8 = 0.0072

#############################################################################################################################################

#Form Factor
k = s0 + s1*(length_os/length_wl) + s2*(length_wl/length_bp) + s3*(c_b) 
+ s4*(length_bp/beam) + s5*(beam/t) + s6*(length_bp/t) 
+ s7*((t_a-t_f)/length_bp) + s8*(depth/t)

form_factor = 1 + k

#############################################################################################################################################

# Velocity values between 0 and 0.55 Froude Numbers
speeds = np.arange(0, 0.455*math.sqrt(g*length_c), 0.005*math.sqrt(g*length_c))
#Reynolds Numbers
reynolds = (speeds * length_c) / (1.1892 * (10**(-6)))
#Friction Resistance Coefficient
c_f = 0.075 / (np.log10(reynolds) - 2)**2


########################################################################################################3

#THE CALCULATION OF MEAN RESIDUARY RESISTANCE
#Coefficients for computation of the standart residuary resistance coefficient
#in Hollenbach's Method for twin screw at DWL.
b11 = -5.3475
b12 = 55.6532
b13 = -114.905
b21 = 19.2714
b22 = -192.388
b23 = 388.333
b31 = -14.3571
b32 = 142.738
b33 = -254.762

#############################################################################################################################################

#Froudes Number
froudes = speeds / np.sqrt(g * length_c)

#############################################################################################################################################

#Standart Value
c_r_std = b11 + (b12*froudes) + (b13*(froudes**2)) 
+ (b21 + (b22*froudes) + (b23*(froudes**2)))*c_b 
+ (b31 + (b32*froudes) + (b33*(froudes**2)))*(c_b**2)

c_r_std = np.abs(c_r_std)

#############################################################################################################################################

#Coefficients for correction  factors of the standar residuary resistance
#coefficient in Hollenbach's Method for twin screw at DWL
d1 = 0.897 
d2 = -1.457
d3 = 0.767
e1 = 1.8319
e2 = -0.1237
a1 = 0.2748
a2 = -0.5747
a3 = -6.761
a4 = -4.3834
a5 = 8.8158
a6 = -0.1418
a7 = -0.1258
a8 = 0.0481
a9 = 0.1699
a10 = 0.0728

#############################################################################################################################################

fr_crit = d1 + d2*c_b + d3*(c_b**2) #Critical Froude number
c1 = froudes / fr_crit
froudes = speeds / np.sqrt(g * length_c)

#############################################################################################################################################

#Froude number factor
k_fr = np.empty_like(froudes, dtype=float)  
for i, froudes in enumerate(froudes):
    if froudes < fr_crit:
        k_fr[i] = 1
    elif froudes >= fr_crit:
        k_fr[i] = (froudes/fr_crit)**c1[i]

print(k_fr)

froudes = speeds / np.sqrt(g * length_c)

#############################################################################################################################################

#Length factor
k_l = e1 * ((length_bp/(1.035*length_bp))**e2)
print(k_l)

#############################################################################################################################################

#Beam-Draught ratio factor
if (beam/t) < 1.99:
    k_bt = (1.99)**a1
elif (beam/t) >= 1.99:
    k_bt = (beam/t)**a1
print(k_bt)

#Length-Beam ratio factor
if (length_bp/beam) <= 7.11:
    k_lb = (length_bp/beam)**a2
elif (length_bp/beam) > 7.11:
    k_lb = (7.11)**a2
print(k_lb)

#############################################################################################################################################

#Wetted Length ratio factor
if (length_os/length_wl) <= 1.05:
    k_ll = (length_os/length_wl)**a3
elif (length_os/length_wl) > 1.05:
    k_ll = (1.05)**a3
print(k_ll)

#############################################################################################################################################

#Aft overhang ratio factor
if (length_wl/length_bp) <= 1.06:
    k_ao = (length_wl/length_bp)**a4
elif (length_wl/length_bp) > 1.06:
    k_ao = (1.06)**a4
print(k_ao)

#############################################################################################################################################

#Trim correction factor
k_tr = ( 1 + ((t_a-t_f)/length_bp) )**a5

#############################################################################################################################################

#Propeller Factor
if (depth/t_a) < 0.43:
    k_pr = (0.43)**a6
elif 0.43 <= (depth/t_a) <= 0.84:
    k_pr = (depth/t_a)**a6
elif (depth/t_a) > 0.84:
    k_pr = (0.84)**a6
    
c_r_bt = c_r_std * k_fr * k_l * k_bt * k_lb * k_ll * k_ao * k_tr * k_pr
c_r_bt = np.abs(c_r_bt)

#############################################################################################################################################

#Factors of lower and upper limit formulas of the range of Froude numbers
#which the Cr fomulas are valid
f1 = 0.16
f2 = 0.24
f3 = .60
g1 = .83
g2 = -.66
g3 = 0.0

#############################################################################################################################################

#lower limit
fr_min = min(f1, f1 + f2*(f3 - c_b))
fr_max = g1 + (g2*c_b) + (g3*(c_b**2))

#############################################################################################################################################

c_r_mean = c_r_bt * ((beam*t)/(10*s))

#####################################################################################################

#THE CALCULATION OF MINIMUM RESIDUARY RESISTANCE
#Coefficients for computation of the standart residuary resistance coefficient
#in Hollenbach's Method for twin screw at DWL.
b11 = 3.27279
b12 = -44.1138
b13 = 171.692
b21 = -11.5012
b22 = 166.559
b23 = -644.456
b31 = 12.4626
b32 = -179.505
b33 = 680.921

#############################################################################################################################################

#Froudes Number
froudes = speeds / np.sqrt(g * length_c)

#############################################################################################################################################

#Standart Value
c_r_std = b11 + (b12*froudes) + (b13*(froudes**2)) 
+ (b21 + (b22*froudes) + (b23*(froudes**2)))*c_b 
+ (b31 + (b32*froudes) + (b33*(froudes**2)))*(c_b**2)

c_r_std = np.abs(c_r_std)

#############################################################################################################################################

#Coefficients for correction  factors of the standar residuary resistance
#coefficient in Hollenbach's Method for twin screw at DWL
d1 = 0.0
d2 = 0.0
d3 = 0.0
a1 = 0.2748
a2 = -0.5747
a3 = -6.761
a4 = -4.3834
a5 = 0.0
a6 = 0.0
a7 = 0.0
a8 = 0.0
a9 = 0.0
a10 = 0.0

#############################################################################################################################################

fr_crit = d1 + d2*c_b + d3*(c_b**2) #Critical Froude number
c1 = froudes / fr_crit
froudes = speeds / np.sqrt(g * length_c)

#############################################################################################################################################

#Froude number factor
k_fr = 1
print(k_fr)

#############################################################################################################################################

froudes = speeds / np.sqrt(g * length_c)

#############################################################################################################################################

#Length factor
k_l = 1
print(k_l)

#############################################################################################################################################

#Beam-Draught ratio factor
if (beam/t) < 1.99:
    k_bt = (1.99)**a1
elif (beam/t) >= 1.99:
    k_bt = (beam/t)**a1
print(k_bt)

#############################################################################################################################################

#Length-Beam ratio factor
if (length_bp/beam) <= 7.11:
    k_lb = (length_bp/beam)**a2
elif (length_bp/beam) > 7.11:
    k_lb = (7.11)**a2
print(k_lb)

#############################################################################################################################################

#Wetted Length ratio factor
if (length_os/length_wl) <= 1.05:
    k_ll = (length_os/length_wl)**a3
elif (length_os/length_wl) > 1.05:
    k_ll = (1.05)**a3
print(k_ll)

#############################################################################################################################################

#Aft overhang ratio factor
if (length_wl/length_bp) <= 1.06:
    k_ao = (length_wl/length_bp)**a4
elif (length_wl/length_bp) > 1.06:
    k_ao = (1.06)**a4
print(k_ao)

#############################################################################################################################################
    
c_r_bt = c_r_std * k_fr * k_l * k_bt * k_lb * k_ll * k_ao
c_r_bt = np.abs(c_r_bt)

#############################################################################################################################################

#Factors of lower and upper limit formulas of the range of Froude numbers
#which the Cr fomulas are valid
f1 = 0.15
f2 = 0.0
f3 = 0.0
g1 = 0.952
g2 = -1.406
g3 = 0.643

#############################################################################################################################################

c_r_min = c_r_bt * ((beam*t)/(10*s))

#############################################################################################################################################

#CORRELATION ALLOWANCE
if length_bp < 175:
    c_A = (0.35-(0.002*length_bp))*(10e-3)
elif length_bp >= 175:
    c_A = 0.0 
    

#############################################################################################################################################

#APPENDAGE RESISTANCE
k2 = 1 + ( (1.7*s_app)/(s_app) )
r_aa = 0.5*rho*(speeds**2)*s_app*k2*c_f
c_aa = r_aa / (0.5*rho*(speeds**2)*s)

#############################################################################################################################################

#TOTAL RESISTANCE
c_t_mean = c_f + c_r_mean + c_A + c_aa 
c_t_min = c_f + c_r_min + c_A + c_aa 

r_t_mean = 0.5 * rho * (speeds**2) * s * c_t_mean
r_t_min = 0.5 * rho * (speeds**2) * s * c_t_min

p_e_mean = r_t_mean * speeds
p_e_min = r_t_min * speeds

#############################################################################################################################################

real_froudes = np.array([0,0.0498028958929961,0.0499364157211275,
                         0.0592828036903225,0.0700979097689624,0.0700979097689624,
                         0.0746375839254285,0.0798448572225514,0.0898588443324032,
                         0.100006351270386,0.109886818552107,0.119900805661958,
                         0.12003432549009,0.129781272943679,0.139661740225399,
                         0.139795260053531,0.150076286819645,0.159823234273234,
                         0.160090273929497,0.169837221383086,0.179851208492938,
                         0.189998715430921,0.200413262025167,0.210160209478756,
                         0.220040676760476,0.229921144042197,0.239534571667654,
                         0.250082638090031,0.25982958554362,0.269843572653472,
                         0.270244132137866,0.279991079591455,0.289871546873176,
                         0.299752014154896,0.300019053811159,0.309632481436617,
                         0.309899521092879,0.3197799883746,0.329927495312583,
                         0.339941482422435,0.349955469532286,0.359835936814007,
                         0.359969456642138,0.370116963580121,0.380130950689973,
                         0.382400787768206,0.385071184330833,0.389744378315431,
                         0.390144937799825,0.395085171440685,0.400025405081545,
                         0.410039392191397,0.419786339644986,0.429666806926706,
                         0.430200886239232,0.440214873349084,0.449961820802673,
                         0.450095340630804])
real_speeds = real_froudes * np.sqrt(g * length_c)

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

#############################################################################################################################################

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))


# Plotting c_r
plt.plot(froudes, r_t_min, label='Minimum Total Resistance', color='green')
plt.plot(froudes, r_t_mean, label='Mean Total Resistance', color='red')
plt.plot(real_froudes, real_r_t, label='Experimental Total Resistance' , color = 'blue')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Total Resistance [N]')
plt.title('Total Resistance vs Froudes Number ("Hollenbach Method")')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))


# Plotting c_r
plt.plot(froudes, r_t_min, label='Minimum Effective Power', color='green')
plt.plot(froudes, r_t_mean, label='Mean Effective Power', color='red')
plt.plot(real_froudes, real_r_t, label='Experimental Result Eff. Power' , color = 'blue')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Effective Power [W]')
plt.title('Effective Power vs Froudes Number ("Hollenbach Method")')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()