import random
import math 
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl  


#-------------------------------------------------------#
#TERRESTRIAL NETWORK (TN) CLASS  This creates an instance of the 5G Terrestrial Network
#--------------------------------------------------------#
class TN:  
 def __init__(self):

  self.TN_PRB = 277 #Number of Physical Resource Blocks(PRB) 
  self.free_PRB = 277 #Number of PRBs free 
  self.TN_LF = 0.0 #TN Load Factor
 
  self.user_List = [] #stores users in TN 
 
 #Function to add user to TN
 def add_user(self, user): 
  self.user_List.append(user) 
  self.free_PRB = self.free_PRB - user.numPRB #Load after user have been added
  self.TN_LF = (1 - self.free_PRB/self.TN_PRB)*100 # Load Factor
  #print(TN.free_PRB)
  #print(TN.TN_LF)
  
 #This function returns the current TN capacity 
 def capacity(self): 
  return self.TN_LF, self.free_PRB, len(self.user_List) 
  
 def print_user(self):  
  n = 1 
  print("TERRESTRIAL NETWORK") 
  print("-----------------------------------------------------------------------")
  for user in self.user_List:       
      print("USER ",n)
      print("\nData Rate: ",user.DR, "\nPRBs use: ",user.numPRB) 
      print("LEO_SS: ",user.LEO_SS,"\nTN_SS: ", user.TN_SS)
      n = n + 1 
  
 #---------------------------------------------------------------# 
 #NON-TERRESTRIAL NETWORK: Low Earth Orbit(LEO) satellite class
 #----------------------------------------------------------------#
class LEO: 
 def __init__(self):  
	 
	 self.LEO_B = 400000000#400000000  
	 self.free_B = 400000000 #free Bandwidth 
	 self.LEO_LF = 0.0 #TN Load Factor
	 
	 self.user_List = [] #stores users in TN 
	 
	 #function to add user to LEO
 def add_user(self, user): 
	 self.user_List.append(user) 
	 self.free_B = self.free_B - user.B #Load after user have been added
	 self.LEO_LF = (1 - self.free_B/self.LEO_B)*100 # Load Factor
	 #print(LEO.free_B)
	 #print(LEO.LEO_LF)
	  
	 #FUNCTION RETURNS THE LOAD FACTOR OF TN NETWORK 
 def capacity(self): 
	 return self.LEO_LF, self.free_B, len(self.user_List)
	  
	 #FUNCTION PRINTS ALL USERS IN TN NETWORK '
 def print_user(self):  
	 n = 1 
	 print("LEO NETWORK") 
	 print("-----------------------------------------------------------------------")
	 for user in self.user_List:       
	      print("USER ",n)
	      print("\nData Rate: ",user.DR, "\nPRBs use: ",user.numPRB) 
	      print("LEO_SS: ",user.LEO_SS,"\nTN_SS: ", user.TN_SS,"\nRST: ",user.RST)
	      n = n + 1 
	 #print(LEO.free_PRB)
	 #print(LEO.LEO_LF)
 
#------------------------------------------------------# 
#USER 
#------------------------------------------------------# 
class user: 
   def __init__(self): 
    #SS-------------------------------------------------------------#
    self.n = random.uniform(1000,9000) 
    self.b = random.uniform(240,1050)
	 
    self.LEO_SS = 44 + 38 -1*(20*math.log10(self.n) + 32.45 + 48.9) #LEO satellite Network Recieved Signal Strength(LEO_SS)
    self.TN_SS = 46 + 30 -1*(354.2 -414.6 +1.12 + 38.35*1.47*math.log10(self.b) + 3 + 46.3)#Terrestrial Network Recieved Signal Strength(TN_SS)
    #----------------------------------------------------------------------------------#
    #DATA RATE 
    self.DR = random.triangular(0.0, 20,8) #random.uniform(0.0,20)    
    #-----------------------------------------------------------------------------------# 
    # Calculate required LEO bandwidth to serve users call
    self.B = self.DR*10**6 / math.log2(1 + self.LEO_SS/-87.96)
   
    # Calculate required TN bandwidth
    self.B1 = self.DR*10**6 / math.log2(1 + self.TN_SS/-87.96)
    
    #Number of PRBs needed to serve uses call
    self.numPRB = self.B1 /1440000 
     
    #-----------------------------------------------------------------------------------# 
    #user's Average Request Service Time 
    self.RST = random.uniform(0.0, 22)

#------------------------------------------------------------------------------------# 
#FUZZY FUNCTION
#------------------------------------------------------------------------------------# 
def fuzzy(user, TN ,LEO): 

 #DEFINE INPUTS 
 SS_TN = ctrl.Antecedent(np.arange(-85.0,-45.0,0.5), 'SS_TN')#Terrestrial Network Signal Strength 
 SS_LEO = ctrl.Antecedent(np.arange(-85.0,-45.0,0.5), 'SS_LEO')#LEO Network Signal Strength 
 
 data_rate = ctrl.Antecedent(np.arange(0.0,20.0,0.5), 'data_rate') #Data rate 
 rst = ctrl.Antecedent(np.arange(0.0,22.0,0.5), 'rst') #Requested Service Time
 
 LF_TN = ctrl.Antecedent(np.arange(0,100,0.5), 'LF_TN') #Load Factor of Terrestrial Network 
 LF_LEO = ctrl.Antecedent(np.arange(0,100,0.5), 'LF_LEO') #Load Factor of Terrestrial Network
 #-----------------------------------------------------------------------------------------------# 
 #DEFINE OUTPUTS 
 RAN = ctrl.Consequent(np.arange(0,101,1), 'RAN') # Radio Access Network that user will connect to 
 
 #--------------------------------------------------------------------------------------------------#
 #DEFINE MEMBERSHIP FUNCTIONS 
 #TN SS 
 SS_TN['low'] = fuzz.trimf(SS_TN.universe, [-85.0,-85.0,-65.0]) 
 SS_TN['mid'] = fuzz.trimf(SS_TN.universe, [-75,-65.0,-55.0])
 SS_TN['high'] = fuzz.trimf(SS_TN.universe, [-65.0,-45.0,-45.0]) 
 
 #LEO SS
 SS_LEO['low'] = fuzz.trimf(SS_LEO.universe, [-85.0,-85.0,-65.0]) 
 SS_LEO['mid'] = fuzz.trimf(SS_LEO.universe, [-75.0,-65.0,-55.0])
 SS_LEO['high'] = fuzz.trimf(SS_LEO.universe, [-65.0,-45.0,-45.0])  
 
 #data rate 
 data_rate['low'] = fuzz.trimf(data_rate.universe, [0.0,0.0,10]) 
 data_rate['mid'] = fuzz.trimf(data_rate.universe, [7.0,10.0,15.0])
 data_rate['high'] = fuzz.trimf(data_rate.universe, [10,20,20])  
 
 #TN load factor 
 LF_TN['low'] = fuzz.trimf(LF_TN.universe, [-1,-1,50.0])  
 LF_TN['mid'] = fuzz.trimf(LF_TN.universe, [30,50.0,75.0])
 LF_TN['high'] = fuzz.trimf(LF_TN.universe, [50.0,90.0,90.0]) 
 LF_TN['V_high'] = fuzz.trimf(LF_TN.universe, [90.0,100.0,100.0])  
 
 #LEO load factor 
 LF_LEO['low'] = fuzz.trimf(LF_LEO.universe, [-1,-1,50.0]) 
 LF_LEO['mid'] = fuzz.trimf(LF_LEO.universe, [30,50.0,75.0])
 LF_LEO['high'] = fuzz.trimf(LF_LEO.universe, [50.0,90.0,90.0])
 LF_LEO['V_high'] = fuzz.trimf(LF_LEO.universe, [90.0,100.0,100.0])
 
 #requested service time
 rst['low'] = fuzz.trimf(rst.universe, [0.0,0.0,5]) 
 rst['mid'] = fuzz.trimf(rst.universe, [5.0,10.0,15.0])
 rst['high'] = fuzz.trimf(rst.universe, [10.0,22.0,22.0]) 
 
 #RAN Network for user connection 
 RAN['LEO'] = fuzz.trimf(RAN.universe, [0.0,0.0,50.0]) 
 RAN['TN'] = fuzz.trimf(RAN.universe, [50.0,100.0,100.0])
 
 #---------------------------------------------------------------------------------# 
 #DEFINE RULES  
 #tn high 
 rule1 = ctrl.Rule(LF_TN['high'] &  LF_LEO['low'], RAN['LEO']) 
 rule2 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['low'], RAN['LEO'])  
 rule3 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['low'], RAN['LEO'])   
 rule4 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['low'], RAN['LEO'])
 rule5 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['mid'], RAN['LEO']) 

 
 #leo high 
 rule6 = ctrl.Rule(LF_TN['low'] &  LF_LEO['high'], RAN['TN'])
 rule7 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['mid'], RAN['TN'])  
 rule8 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['high'], RAN['LEO'])
 rule9 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['mid'], RAN['TN']) 
 rule10 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['high'] & SS_TN['high'] & SS_LEO['mid'], RAN['TN'])
 
 #tn mid
 
 rule11 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['high'], RAN['TN']) 
 rule12 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['mid'], RAN['TN']) 
 rule13 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['mid'], RAN['TN']) 
 rule14 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['high'] & SS_TN['high'] & SS_LEO['high'], RAN['TN'])  
 
 #leo mid  
 rule15 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['high'], RAN['LEO'])   
 rule16 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['high'], RAN['LEO']) 
 rule17 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['high'], RAN['LEO'])
 
 #tn low
   
 rule18 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['mid'], RAN['TN'])
 rule19 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['low'], RAN['TN']) 
 rule20 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['mid'], RAN['TN'])
 
 #leo low 
 rule21 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['mid'], RAN['LEO']) 
 rule22 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'], RAN['TN']) 
 rule23 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['mid'], RAN['LEO'])  
 rule24 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['low'], RAN['TN']) 
 rule25 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['high'], RAN['TN'])  
 rule26 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['high'], RAN['LEO']) 
 
 #DR RULES 
 rule27 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['low'], RAN['LEO'])  
 rule28 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['mid'], RAN['LEO']) 
 rule29 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['high'], RAN['TN'])
 
 rule30 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['low'] & data_rate['low'], RAN['LEO']) 
 rule31 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['low'] & data_rate['mid'], RAN['LEO']) 
 rule32 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['low'] & data_rate['high'], RAN['TN']) 
   
 rule33 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['low'], RAN['LEO']) 
 rule34 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['mid'], RAN['TN']) 
 rule35 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['high'], RAN['TN'])  
 
 rule36 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['low'], RAN['LEO'])  
 rule37 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['mid'], RAN['LEO']) 
 rule38 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['high'], RAN['TN']) 
 
 rule39 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['mid'] & data_rate['low'], RAN['LEO'])  
 rule40 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['mid'] & data_rate['mid'], RAN['LEO']) 
 rule41 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['high'] & SS_LEO['mid'] & data_rate['high'], RAN['TN']) 
    
 rule42 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['low'], RAN['TN'])   
 rule43 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['mid'], RAN['LEO'])
 rule44 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['high'], RAN['LEO']) 
 
 rule45 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['high'] & data_rate['low'], RAN['TN']) 
 rule46 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['high'] & data_rate['mid'], RAN['TN']) 
 rule47 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['high'] & data_rate['high'], RAN['LEO']) 
  

 rule48 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['low'], RAN['LEO'])    
 rule49 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['mid'], RAN['LEO'])
 rule50 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'] & data_rate['high'], RAN['TN']) 
 
 rule51 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['high'] & data_rate['low'], RAN['TN']) 
 rule52 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['high'] & data_rate['mid'], RAN['LEO']) 
 rule53 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['high'] & data_rate['high'], RAN['LEO']) 
 
 #RST RULES
 rule54 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['low'] & rst['low'], RAN['LEO']) 
 rule55 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['low'] & rst['mid'], RAN['LEO'])  
 rule56 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['low'] & rst['high'] , RAN['TN'])
 
 rule57 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['low'] & data_rate['low'], RAN['LEO'])  
 rule58 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['low'] & data_rate['mid'], RAN['LEO']) 
 rule59 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['low'] & data_rate['high'], RAN['TN']) 
  
 rule60 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['low'] & rst['low'], RAN['LEO']) 
 rule61 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['low'] & rst['mid'], RAN['LEO'])
 rule62 = ctrl.Rule(LF_TN['low'] &  LF_LEO['low'] & SS_TN['low'] & SS_LEO['low'] & rst['high'], RAN['TN'])
 
 rule63 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['high'] & SS_LEO['high'] & rst['low'], RAN['LEO']) 
 rule64 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['high'] & SS_LEO['high'] & rst['mid'], RAN['LEO'])
 rule65 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['high'] & SS_LEO['high'] & rst['high'], RAN['TN'])
 
 rule66 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['mid'] & rst['low'], RAN['LEO']) 
 rule67 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['mid'] & rst['mid'], RAN['LEO']) 
 rule68 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['mid'] & rst['high'], RAN['TN']) 
 
 rule69 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['low'] & rst['low'], RAN['LEO']) 
 rule70 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['low'] & rst['mid'], RAN['TN'])
 rule71 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['low'] & SS_LEO['low'] & rst['high'], RAN['TN']) 
 
 rule72 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['high'] & data_rate['low'], RAN['TN'])   
 rule73 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['high'] & data_rate['mid'], RAN['LEO'])
 rule74 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['high'] & data_rate['high'], RAN['LEO'])  

 rule75 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['low'], RAN['LEO'])
 rule76 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['mid'], RAN['TN']) 
 rule77 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['mid'] & SS_LEO['low'] & data_rate['high'], RAN['TN'])
  
 rule78 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['low'] & rst['low'], RAN['LEO'])    
 rule79 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['low'] & rst['mid'], RAN['TN'])
 rule80 = ctrl.Rule(LF_TN['mid'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['low'] & rst['high'], RAN['TN'])  
 
 rule81 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['low'] & SS_LEO['mid'], RAN['LEO']) 
 rule82 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['mid'] & SS_LEO['mid'], RAN['LEO']) 
 rule83 = ctrl.Rule(LF_TN['high'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['mid'], RAN['LEO'])  
 
 rule84 = ctrl.Rule(LF_TN['high'] &  LF_LEO['high'] & SS_TN['high'] & SS_LEO['low'], RAN['LEO']) 
 rule85 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['high'], RAN['LEO']) 
 rule86 = ctrl.Rule(LF_TN['high'] &  LF_LEO['V_high'], RAN['TN']) 
 
 rule87 = ctrl.Rule(LF_TN['low'] &  LF_LEO['mid'] & SS_TN['high'] & SS_LEO['low'], RAN['TN'])
 rule88 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['low'] & SS_LEO['low'], RAN['TN'],) 
 rule89 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['low'] & SS_LEO['mid'], RAN['LEO'],)
 rule90 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['low'] & SS_LEO['high'], RAN['LEO'],)  
 
 rule91 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['mid'] & SS_LEO['low'], RAN['TN'],) 
 rule92 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['mid'] & SS_LEO['mid'], RAN['TN'],)
 rule93 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['mid'] & SS_LEO['high'], RAN['LEO'],)  
 
 rule94 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['high'] & SS_LEO['low'], RAN['TN'],) 
 rule95 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['high'] & SS_LEO['mid'], RAN['TN'],)
 rule96 = ctrl.Rule(LF_TN['V_high'] &  LF_LEO['V_high'] & SS_TN['high'] & SS_LEO['high'], RAN['TN'],) 
 
#----------------------------------------------------------------------------------------------------------------------------# 
 #CREATE CONTROL SYSTEM / FUZZIFIER
 RAN_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13,rule14,rule15,rule16,rule17,rule18,rule19,rule20,rule21,rule22,rule23,rule24,rule25,rule26,rule27,rule28,rule29,rule30,rule31,rule32,rule33,rule34,rule35,rule36,rule37,rule38,rule39,rule40,rule41,rule42,rule43,rule44,rule45,rule46,rule47,rule48,rule49,rule50,rule51,rule52,rule53,rule54,rule55,rule56,rule57,rule58,rule59,rule60,rule61,rule62,rule63,rule64,rule65,rule66,rule67,rule68,rule69,rule70,rule71,rule72,rule73,rule74,rule75,rule76,rule77,rule78,rule79,rule80,rule81,rule82,rule83,rule84,rule85,rule86,rule87,rule88,rule89,rule90,rule91,rule92,rule93,rule94,rule95,rule96])
 
 #------------------------------------------------------------------------------------------------------------------------------# 
 #CREATE SIMULATION 
 RAN_choice_sim = ctrl.ControlSystemSimulation(RAN_ctrl)  
 
 #---------------------------------------------------------------------------------------------------------------------------------# 
 #INPUTS GO THROUGH THE FUZZIFICATION PROCESS
 RAN_choice_sim.input['LF_TN'] = TN.TN_LF #TN Load Factor 
 RAN_choice_sim.input['LF_LEO'] = LEO.LEO_LF  # LEO Load Factor  
 RAN_choice_sim.input['SS_TN'] = user.TN_SS  # TN Signal Strength
 RAN_choice_sim.input['SS_LEO'] = user.LEO_SS #LEO Signal Strength
 
 RAN_choice_sim.input['data_rate'] = user.DR # user data rate
 RAN_choice_sim.input['rst'] = user.RST #user rst 
 
 #PERFORM FUZZY INFERENCE 
 RAN_choice_sim.compute() 
 
 #OUTPUT / DEFUZZIFICATION 
 ran_output = RAN_choice_sim.output['RAN'] 
 
 # DEPENDING ON OUTPUT USER WILL CONNECT TO LEO OR TN
 if ran_output < 50:
  LEO.add_user(user) 
 else:
  TN.add_user(user) 

     
#----------------------------------------------------------------------------------# 
#TEST
#-----------------------------------------------------------------------------------# 
#TESTING PROTOCOL 
def test1(numTest): #THIS TEST IS USED TO INSERT USERS TILL BOTH NETWORKS REACH MAX CAPACITY
 TN_total = 0
 LEO_total = 0
 TN_AVG = 0
 LEO_AVG = 0 
 TN_list = [] 
 LEO_list = [] 
  
 for n in range(numTest): #numTest = AMOUNT OF NETWORK SIMULATIONS
  T = TN()  #TN NETWORK
  L = LEO()  #LEO satellite Network
    
  print("NETWORK SIM-",n+1) 
   
  for i in range(200): #ADD USERS TO NETWORK
   x = user()
       
   if x.numPRB < T.free_PRB and x.B < L.free_B: #USES FUZZY LOGIC TO ASSIGN USERS A NETWORK
    fuzzy(x,T,L)
   
   if x.numPRB > T.free_PRB or x.B > L.free_B: #IF USERS CALL IS BLOCKED BY ONE RAT, CHECK TO SEE IF OTHER CAN SERVICE USERS CALL
    if x.numPRB < T.free_PRB:
     T.add_user(user())
   
    if x.numPRB < L.free_B: 
     L.add_user(user()) 
     
    if L.LEO_LF > 99.99 and T.TN_LF > 99.99: #BOTH NETWORKS HAVE REACHED MAX CAPACITY, SIMULATION ENDS
     T.TN_LF = 100 
     L.LEO_LF = 100
     break
    
  print("TN LF:",T.TN_LF) 
  print("LEO_LF",L.LEO_LF,"\n#--------------------------------------------------------#")
  TN_list.append(T.TN_LF) 
  LEO_list.append(L.LEO_LF)
 
 for n in range(len(TN_list)): #ADD THE LF
    #print(n)
    TN_total = TN_total + TN_list[n] 
    LEO_total = LEO_total + LEO_list[n]
  

 TN_AVG = TN_total/numTest #AVERAGE LOAD FACTOR OF TN
 LEO_AVG = LEO_total/numTest #AVERAGE LOAD FACTOR OF LEO
 
 J_N = (TN_AVG + LEO_AVG)**2 #JFI NUMERATOR     
 J_D = 2*(TN_AVG**2 + LEO_AVG**2) #JFI DENOMINATOR

 JFI = J_N/J_D  #Jains Fair Index 
   
 
 print("TN AVG LF: ",TN_AVG,"\nLEO AVG LF: ",LEO_AVG,"\n JFI: ",JFI) #PRINT OUTPUT OF NETWORK SIMULATION
 
  
def test2(numTest):#test2 WAS USED FOR TESTS 1-7  
 TN_total = 0
 LEO_total = 0
 TN_AVG = 0
 LEO_AVG = 0 
 TN_list = [] 
 LEO_list = [] 
  
 for n in range(numTest): #LOOP NETWORK SIMULATIONS
  T = TN()  #TN NETWORK
  L = LEO()  #LEO NETWORK
    
  print("NETWORK SIM-",n+1) 
   
  for i in range(200): #ADD USERS TO NETWORK
   x = user()
       
   if x.numPRB < T.free_PRB and x.B < L.free_B:
    fuzzy(x,T,L)
   
   if T.TN_LF >= 15: #   T.TN_LF >= 10:   L.LEO_LF >= 20 or T.TN_LF >= 20: 
    break
  
  print("TN LF:",T.TN_LF) 
  print("LEO_LF",L.LEO_LF,"\n#--------------------------------------------------------#")
  TN_list.append(T.TN_LF) 
  LEO_list.append(L.LEO_LF)
 
 for n in range(len(TN_list)): #ADD THE LF
    #print(n)
    TN_total = TN_total + TN_list[n] 
    LEO_total = LEO_total + LEO_list[n]
  
 #print(TN_total) 
 #print(LEO_total) 
 TN_AVG = TN_total/numTest #GET THE AVERAGES
 LEO_AVG = LEO_total/numTest 
 
 J_N = (TN_AVG + LEO_AVG)**2     
 J_D = 2*(TN_AVG**2 + LEO_AVG**2)

 JFI = J_N/J_D  #Jains Fair Index
 
 
 print("TN AVG LF: ",TN_AVG,"\nLEO AVG LF: ",LEO_AVG,"\n JFI: ",JFI)
  
  
  
    
test2(10) # THIS RUNS 20 NETWORK SIMULATIONS AND DETERMINES THE AVERAGE LOAD FACTOR OF THE TN AND LEO NETWORKS, AND THE JFI 






 













 
 
 
