# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:26:41 2023

@author: uygur
"""

import numpy as np
import matplotlib.pyplot as plt

#Required and optional input parameters for Holtrop-Mennen's Method (1982)
length_bp = float(input('Enter Lbp: ')) #Length between perpendicıler
length_wl = float(input('Enter LwL: ')) #Waterline length
beam = float(input('Enter B: ')) #Beam
depth = float(input('Enter D: ')) #Depth
t_a = float(input('Enter Ta: ')) #Aft Draught
t_f = float(input('Enter Tf: ')) #Forward Draught
t = (t_a + t_f) / 2 #Midship Draught
g = 9.807 #Gravity [km/s^2]
rho = 1025 #Density [kg/m^3]

abt = float(input('Enter Transverse Area of Bulb: '))
hb = float(input('Enter hb: '))
l_CB = float(input('Enter LCB (aft of LWL/2): '))
lcb = -(l_CB/length_wl)*100
a_t = float(input('Enter immersed transom area: '))
s_app = float(input('Enter App. Wetted Surface Area, S: ')) #TOTAL APP. AREA
a_v = float(input('Enter transverse vertical area above WL, Av: '))
disp_v = float(input('Enter the displacement volume: '))
a_m = float(input('Enter the midship section area: '))
a_w = float(input('Enter the waterplane section area: '))

#############################################################################################################################################

#C-Stern
c_stern = float(input('Enter the coeffcient of afterbosy form: ')) # V-shaped:-10 /// Normal Shaped:0 ///  U-Shaped with Hogner: 10

#############################################################################################################################################

#FORM COEFFICIENTS
c_b = disp_v / (length_wl * beam * t) #Block Coefficient
c_p = disp_v / (length_wl * a_m) #Prismatic Coefficient
c_wp = a_w / (length_wl*beam) #WaterPlane Area Coefficient
c_m = a_m / (beam * t) #MidshipSection Coefficient

#############################################################################################################################################

#WETTED SURFACE AREA
s = float(input('Enter Wetted Surface Area, S: ')) #Wetted Surface Area
if s == 0:
    s = length_wl * (2*t+beam)*np.sqrt(c_m) * ( 0.453 + (0.4425*c_b) - (0.2862*c_m) - (0.003467*(beam/t)) + (0.3696*c_wp) ) + (2.38*(abt/c_b))
else:
    s = s

#############################################################################################################################################

#DISPLACEMENT (TON)
disp = disp_v * (rho/1000) #Displacement [t]

#############################################################################################################################################

#Length of the run
l_r = length_wl * ( 1 - c_p + ((0.06*c_p*lcb)/(4*c_p - 1)) )

#############################################################################################################################################

#Form Factor coefficients
c13 = 1 + 0.003*c_stern

if t/length_wl > 0.05:
    c12 = (t/length_wl)**0.2228446
elif 0.02 < t/length_wl < 0.05:
    c12 = (48.20*(((t/length_wl) - 0.02)**2.078)) + 0.479948
elif t/length_wl < 0.02:
    c12 = 0.479948
    
#FORM FACTOR
k = float(input('Enter the form factor, k: ')) 
if k == 0:
    k = c13*( 0.93 + c12*((beam/l_r)**0.92497) * ((0.95-c_p)**-0.521448) * ((1 - c_p + (0.0225*lcb))**0.6906) )
else:
    k = k
 
#############################################################################################################################################


froudes = np.array([0,0.0498028958929961,0.0499364157211275,
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

speeds = froudes * np.sqrt(g * length_wl)
reynolds = (speeds * length_wl) / (1.1892 * (10**(-6)))

#############################################################################################################################################


#THE FRICTION RESISTANCE COEFFICIENT
c_f = 0.075 / (np.log10(reynolds) - 2)**2
#FRICTION RESISTANCE
r_f = 0.5 * rho * (speeds**2) * c_f * s

#############################################################################################################################################

#Appendages Form Factor
sum_k2 = float(input('Enter the total 1 + k2: '))
k2 = (sum_k2 * s_app) / s_app

#THE APPENDAGE RESISTANCE
r_app = 0.5 * rho * (speeds**2) * s_app * (k2) * c_f

#############################################################################################################################################

#THE RESISTANCE OF BOW THRUSTER TUNNEL
dd = float(input('Enter the tunnel diameter: '))
c_bto = float(input('Enter the Cbto: ')) #The coefficient ranges from 0.003 to 0.012
if c_bto < 0.003:
    c_bto = 0.003
elif c_bto > 0.012:
    c_bto = 0.012

r_bto = rho*(speeds**2)*np.pi*(dd**2)*c_bto

#############################################################################################################################################

#THE WAVE RESISTANCE
c3 = (0.56 * (abt**1.5)) / ((beam*t)*( (0.31*np.sqrt(abt)) + t_f - hb) )
iE =  1 + 89* np.e**( -((length_wl/beam)**0.80856) * ((1 - c_wp)**0.30484) * ((1 - c_p - 0.0225*lcb)**0.6367) * ((l_r/beam)**0.34574) * (((100*disp_v)/(length_wl**3))**0.16302) )
d = -0.9

if ((length_wl**3) / disp_v) < 512:
    c15 = -1.69385
elif 512 < ((length_wl**3) / disp_v) < 1727:
    c15 = -1.69385 + ( length_wl/(disp_v**(1/3)) - 8.0 )/2.36
elif ((length_wl**3) / disp_v) > 1727:
    c15 = 0.0
    
m2 = c15 * (c_p**2) * (np.e**(-0.1*(froudes**-2)))

if c_p < 0.80:
    c16 = 8.07981*c_p - (13.8673*(c_p**2)) + (6.984388*(c_p**3)) 
elif c_p > 0.80:
    c16 = 1.73014 - 0.7067*c_p
    
m1 = (0.0140407 * (length_wl/t)) - ( 1.75254* ( (disp_v**(1/3))/length_wl ) ) - (4.79323 * (beam/length_wl)) - c16

if (length_wl/beam) < 12:
    lamda = (1.446*c_p) - (0.03 * (length_wl/beam))
elif (length_wl/beam) > 12:
    lamda = (1.446*c_p) - 0.36
    
c5 = 1 - ((0.8*a_t)/(beam*t*c_m))
c2 = np.e**(-1.89 * np.sqrt(c3))

if (beam/length_wl) < 0.11:
    c7 = 0.229577*((beam/length_wl)**(1/3))
elif 0.11 < (beam/length_wl) < 0.25:
    c7 = beam / length_wl
elif (beam/length_wl) > 0.25:
    c7 = 0.5 - 0.0625*(length_wl/beam)

c1 = 2223105 * (c7**3.78613) * ((t/beam)**1.07961) * ((90-iE)**-1.37565)

r_w = c1*c2*c5*disp_v*1025*g *  np.e**( (m1*(froudes**d)) + (m2 * np.cos(lamda * (froudes**-2)) ) ) 

#############################################################################################################################################

#THE RESISTANCE DUE TO BULBOUS BOW
froudes_ni = speeds / np.sqrt( g*(t_f - hb - (0.25*np.sqrt(abt))) + 0.15*(speeds**2) )
p_b = (0.56*np.sqrt(abt)) / (t_f - 1.5*hb)
r_b = ((0.11* np.e**(-3*(p_b**-2))) * (froudes_ni**3) * (abt**1.5) * rho * g) / ( 1 + (froudes_ni**2))

#############################################################################################################################################

#THE RESISTANCE DUE TO IMMERSED TRANSOM
froudes_nt = speeds/np.sqrt( (2*g*a_t)/(beam + beam*c_wp) )

c6 = np.where(froudes_nt < 5, 0.2 * (1 - 0.2 * froudes_nt), 0)
r_tr = 0.5 * rho * (speeds**2) * a_t * c6
    
#############################################################################################################################################

#CORRELATION ALLOWANCE COEFFICIENT
if t_f/length_wl <= 0.04:
    c4 = t_f/length_wl
elif  t_f/length_wl > 0.04:
    c4 = 0.04
    
c_a = 0.006*((length_wl + 100)**-0.16) - 0.00205 + 0.003*np.sqrt(length_wl/7.5)*(c_b**4)*c2*(0.04-c4)

#############################################################################################################################################

#MODEL-SHIP CORRELATION RESISTANCE
r_a = 0.5 * rho * (speeds**2) * s * c_a

#############################################################################################################################################

#TOTAL RESISTANCE
r_t = (r_f * k) + r_app + r_w + r_b + r_tr + r_a + r_bto

#EFFECTIVE POWER 
p_e = r_t * speeds

#############################################################################################################################################

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

#EXPERIMENTAL EFFECTICE POWER RESULTS
real_p_e = real_r_t * speeds 

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

# Plotting r_t
plt.plot(froudes, r_t, label='Total Resistance', color='brown', marker = 'o')
plt.plot(froudes, real_r_t, label='Experimental Total Resistance' , color = 'blue', marker = '*')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Total Resistance [N]')
plt.title('Total Resistance vs Froudes Number (Holtrop-Mennen 1982)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

# Plotting p_e
plt.plot(froudes, p_e, label='Effective Power (W)', color='brown', marker = 'o')
plt.plot(froudes, real_p_e, label='Experimental Effective Power (W)' , color = 'blue', marker = '*')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Effective Power [W]')
plt.title('Effective Power vs Froudes Number (Holtrop-Mennen 1982)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(froudes, r_t, label='Total Resistance (N)', color='red', marker = 'o')
plt.plot(froudes, r_f, label='Friction Resistance (N)', color='green', marker = 'o')
plt.plot(froudes, r_w, label='Wave Resistance (N)', color='blue', marker = 'o')

# Adding labels and title
plt.xlabel('Froudes Numbers')
plt.ylabel('All Resistances [N]')
plt.title('All Resistance vs Froudes Number (Holtrop-Mennen 1982)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

