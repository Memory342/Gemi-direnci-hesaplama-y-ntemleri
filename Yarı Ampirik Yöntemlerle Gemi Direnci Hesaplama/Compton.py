# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 22:48:28 2023

@author: uygur
"""

import numpy as np
import matplotlib.pyplot as plt

length_bp = (float(input('Enter Lbp: ')))*3.2808399  # Length between perpendicular
length_wl = (float(input('Enter LwL: ')))*3.2808399   # Waterline length
beam = (float(input('Enter B: ')))*3.2808399  # Beam
depth = (float(input('Enter D: ')))*3.2808399   # Depth
t_a = (float(input('Enter Ta: ')))*3.2808399   # Aft Draught
t_f = (float(input('Enter Tf: ')))*3.2808399  # Forward Draught
t = (t_a + t_f) / 2  # Midship Draught
g = 9.807  # Gravity [km/s^2]
rho = 1025  # Density [kg/m^3]
s = (float(input('Enter Wetted Surface Area, S: ')))*(3.2808399**2)  # Wetted Surface Area
disp_v = float(input('Enter the displacement volume: ')) #Displacement Volume
a_m = float(input('Enter the midship section area: '))*(3.2808399**2) #Midship Section Area
a_w = float(input('Enter the waterplane section area: '))*(3.2808399**2) #Waterplane Area

disp = (disp_v * (rho/1025)) #Displacement [t]

c_b = disp_v / ((length_wl/3.2808399) * (beam/3.2808399) * (t/3.2808399)) #Block Coefficient
c_p = disp_v / ((length_wl/3.2808399) * (a_m/3.2808399**2)) #Prismatic Coefficient
c_wp = (a_w/3.2808399**2) / ((length_wl/3.2808399)*(beam/3.2808399)) #WaterPlane Area Coefficient
c_m = (a_m/3.2808399**2) / ((beam/3.2808399) * (t/3.2808399)) #MidshipSection Coefficient

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


#######################################################################################################

# A, B, C and D Coefficients from Table
A_values = np.array([0, -3.15510, -2.97560, -2.53050, -2.36370, 
                    -3.27340, -3.30700, -2.51140, -6.30630, -13.35250, -12.80320, -10.96130])
B_values = np.array([0, 0.11734, 0.13670, 0.14597, 0.14597,
                    0.28838, 0.34376, 0.19296, 0.85295, 1.71032, 1.66136, 1.46348])
C_values = np.array([0, 0.03036, 0.02882, 0.02780, 0.03099,
                    0.03994, 0.05040, 0.05704, 0.07999, 0.11094, 0.11094, 0.09407])
D_values = np.array([0, 0.24272, 0.23790, 0.24179, 0.27135,
                    0.31552, 0.31348, 0.31572, 0.35185, 0.34211, 0.34211, 0.19962])

# Calculating A, B, C and D coefficients each Froude numbers
A = np.interp(froudes, [0, 0.1, 0.15, 0.2, 0.25, 0.3,
              0.35, 0.4, 0.45, 0.5, 0.55, 0.6], A_values)
B = np.interp(froudes, [0, 0.1, 0.15, 0.2, 0.25, 0.3,
              0.35, 0.4, 0.45, 0.5, 0.55, 0.6], B_values)
C = np.interp(froudes, [0, 0.1, 0.15, 0.2, 0.25, 0.3,
              0.35, 0.4, 0.45, 0.5, 0.55, 0.6], C_values)
D = np.interp(froudes, [0, 0.1, 0.15, 0.2, 0.25, 0.3,
              0.35, 0.4, 0.45, 0.5, 0.55, 0.6], D_values)

#######################################################################################################

# Print results
for i in range(len(froudes)):
    print(
        f"Froude={froudes[i]:.5f}  A={A[i]:.5f}  B={B[i]:.5f}  C={C[i]:.5f}  D={D[i]:.5f}")

output_array = np.column_stack((froudes, A, B, C, D))
print(output_array)


speeds = froudes * np.sqrt(g *  (length_wl/3.2808399))
reynolds = (speeds * (length_wl/3.2808399)) / (1.1892 * (10**(-6)))

#THE FRICTION RESISTANCE COEFFICIENT
c_f = 0.075 / (np.log10(reynolds) - 2)**2

#############################################################################################################

# RESIDUAL RESISTANCE COEFFICIENT
# c_r = (A + B*(L/B) + C*(Displacement//L^3) + D*(LCG/L * 100)) #Units are long ton, ft and ft^3
# 1 ft = 0.3048 m
# 1 long ton = 1.01604691 metric ton
c_r = (A + B*(465.879/62.5328083989501) + C*(103.915565949087) + D*((0/465.879) * (10**2)))/1000

#######################################################################################################


# THE FRICTION RESISTANCE COEFFICIENT
c_f = 0.075 / (np.log10(reynolds) - 2)**2

#######################################################################################################

#TOTAL RESISTANCE COEFFICIENT
c_t = (c_f*1.190997) + c_r

#TOTAL RESISTANCE
r_t = (0.5 * c_t * rho * (speeds**2) * (s/(3.2808399**2)))

#EFFECTIVE POWER
p_e = r_t * speeds

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
plt.plot(froudes, r_t, label='Total Resistance', color='purple', marker = 'o')
plt.plot(froudes, real_r_t, label='Experimental Total Resistance' , color = 'blue', marker = '*')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Total Resistance [N]')
plt.title('Total Resistance vs Froudes Number (Compton Method)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

# Plotting p_e
plt.plot(froudes, p_e, label='Effective Power (W)', color='purple', marker = 'o')
plt.plot(froudes, real_p_e, label='Experimental Effective Power (W)' , color = 'blue', marker = '*')

# Adding labels and title
plt.xlabel('Froudes Number')
plt.ylabel('Effective Power [W]')
plt.title('Effective Power vs Froudes Number (Compton Method)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()

#############################################################################################################################################

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(froudes[1:], c_t[1:], label='Total Resistance Coefficient (N)', color='red', marker = 'o')
plt.plot(froudes[1:], c_f[1:], label='Friction Resistance Coefficient (N)', color='green', marker = 'o')
plt.plot(froudes[1:], c_r[1:], label='Wave Resistance Coefficient(N)', color='blue', marker = 'o')

# Adding labels and title
plt.xlabel('Froudes Numbers')
plt.ylabel('Resistance Coefficients [N]')
plt.title('Total, Viscous and Wave Resistance Coefficients as a function of Froude number (Compton Method)')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

# Show the plot
plt.show()