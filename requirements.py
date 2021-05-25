import math
import scipy.constants as sp

cubesat_principal_diagonal = math.sqrt((30**2)+(10**2)+(10**2))
#print("Principal diagonal is" , cubesat_principal_diagonal)

#Let nominal region with uniform field be cubeSats's bigger side (30cm) + 20cm
region_of_uni_field = 50

# Gamma  = coils' distance / side of coil
gamma = 0.5445

def side_of_coil(region_of_uni_field):
    uniform_region_ratio = 0.4
    side_of_coil = region_of_uni_field / uniform_region_ratio
    return side_of_coil/100 # returns side in meters

side = side_of_coil(region_of_uni_field)
#print("Side of coil is: ",side_of_coil(region_of_uni_field) , "m")

def field_magnitude(turns_in_coil , current_in_coil, side_of_coil, gamma):

    field_intensity = (2*(sp.mu_0)*(turns_in_coil)*(current_in_coil) )/(side_of_coil*(1+gamma**2)*(math.sqrt(2+gamma**2)))
    return field_intensity

#Let earth's magnetic field be from 10^(-5)T to 6*10^(-5)
#Let desired magnetic field be 2-3 bigger than earths magnetic field


earth_magn_field = 45*10**(-6)
#Let resistivity of copper be 1.68*10^(-8) Ohm(?)
constant = (2*sp.mu_0)/((4*(1.68*10**(-8)))*math.sqrt((2+gamma**2))*(1+gamma**2))

#Let nominal voltage be 12V
def wire_cross_sectional_area(constant, earth_magn_field,side_of_coil, voltage):
    cross_sect_area = 3 * earth_magn_field * (side_of_coil**2) / (constant * voltage)
    return cross_sect_area

cross_sect_area = wire_cross_sectional_area(constant , earth_magn_field, side ,12)

def cross_sect_diameter(cross_sect_area):
    d = math.sqrt(4*cross_sect_area/math.pi)
    return d

wire_diameter = cross_sect_diameter(cross_sect_area)

#print("Wire cross sectional area is: ", wire_cross_sectional_area(constant , earth_magn_field, side ,12))
#print("Wire's diameter area is: ", wire_diameter)

def current_threshold(wire_diameter):
    threshold = (wire_diameter**2)/(4.52*(10**(-7)))# Constant depends on the type of wire
    return threshold

threshold = current_threshold(wire_diameter)
#print("Current Threshold:", current_threshold(wire_diameter))


def Wire_turns(magnetic_field, side, gamma):
    NI = 3*magnetic_field*side*(1+gamma**2)*math.sqrt(2+gamma**2)/(2*sp.mu_0)
    resistivity = 1.68*(10**(-8))
    voltage = 12
    #constant2 = 3*2*resistivity*(1+gamma**2)*math.sqrt(2+gamma**2)/(voltage*(sp.mu_0))
    A = (2*3*magnetic_field*(side**2)*resistivity*(1+gamma**2)*math.sqrt(2+gamma**2))/(voltage* sp.mu_0)
    A = (magnetic_field*(side**2))/96.949
    d = math.sqrt(4*A/math.pi)
    I_threshold = (d**2)/(4.52*(10**(-7)))
    N = NI / I_threshold
    return N

print("\n", Wire_turns(45*(10**(-6)), 1.3, gamma), "\n")

def estimations(region_of_uniform_field , earth_magnetic_field, voltage, gamma ):
    #side = side_of_coil(region_of_uniform_field)
    print("Side of coil is: ", side_of_coil(region_of_uniform_field), "m")
    side = 1.3
    cross_sect_area = wire_cross_sectional_area(constant, earth_magnetic_field, side, 12)

    wire_diameter = cross_sect_diameter(cross_sect_area)
    print("Wire cross sectional area is: ", wire_cross_sectional_area(constant, earth_magnetic_field, side, 12))
    print("Wire's diameter area is: ", wire_diameter)

    threshold = current_threshold(wire_diameter)
    print("Current Threshold:", current_threshold(wire_diameter))

    minimum_wire_turns = Wire_turns(earth_magnetic_field, side, gamma)
    print("Min wire turns:", minimum_wire_turns)


#estimations(50, 45*10**(-6), 12)

magnetic_field = [10**-5, 2*10**-5, 3*10**-5, 4*10**-5, 5*10**-5, 6*10**-5]
desired_voltage = [12+i for i in range(11)]

for i in range(len(magnetic_field)):
    for j in range(len(desired_voltage)):
        print("Voltage is:", desired_voltage[j])
        print("Magnetic field is:", magnetic_field[i])
        estimations(50, magnetic_field[i], desired_voltage[j], gamma)
        print("\n", "***---------------------***", "\n")

#estimations(50, 45*10**-6, 12, gamma)