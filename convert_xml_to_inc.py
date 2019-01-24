# File:convert_xml_to_inc.py
# Author: manikSom
# Contact: manickam.som@gmail.com
#
#   This program is free software;  you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY;  without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
#   the GNU General Public License for more details.

import xml.dom.minidom
ak3dom = xml.dom.minidom.parse('recplate.xml')
f = open('Quadrat_2D_from_recplate.inp','w')
#---------------------------------------------#
#----------------Writing-Nodes----------------#
#---------------------------------------------#
f.write('*HEADING\n  Quadrat_2D\n**---------------------------------------------------\n')
f.write('*NODE\n')
node_group =ak3dom.getElementsByTagName('Nodes')
no_of_group1 = len(node_group)                                                                                                                                                                                                                                                                                                                                                                                                      
for group_no1 in range(no_of_group1):
        no_of_elements = len(node_group.item(group_no1).getElementsByTagName('Node'))                                                                                                                                                                                                                                                                                                                  
        for element in node_group.item(group_no1).getElementsByTagName('Node'):
            f.write(element.getElementsByTagName('Id').item(0).firstChild.nodeValue +', ')
            f.write(element.getElementsByTagName('x').item(0).firstChild.nodeValue +', ')
            f.write(element.getElementsByTagName('y').item(0).firstChild.nodeValue +', ')
            f.write(element.getElementsByTagName('z').item(0).firstChild.nodeValue +'\n')
#---------------------------------------------#
#---------------Writing-Elements--------------#
#---------------------------------------------#
element_groups = ak3dom.getElementsByTagName('Elements')
no_of_group = len(element_groups)
for group_no in range(no_of_group):
        f.write('*ELEMENT, TYPE='+'S4'+', ELSET='+element_groups.item(group_no).attributes['Group'].value)
        for element in element_groups.item(group_no).getElementsByTagName('PlShell9'): #Need to change shell type according to input file(Brick8/PlShell9.etc)
                f.write('\n'+element.getElementsByTagName('Id').item(0).firstChild.nodeValue)
                for i in range(4):
                        f.write(', '+ element.getElementsByTagName('N').item(i).firstChild.nodeValue)
        if (group_no != no_of_group-1 and no_of_group > 1):
                f.write('\n')
#--------------------------------------------------#                
#-------Extracting-Loads-And-Boundary-Conditions---#
#-----------(Only for displaying purpose)----------#
#--------------------------------------------------#
load_group = ak3dom.getElementsByTagName('NodalForces')
print "-----------------------------------"
print "Description of Nodal Forces"
print "-----------------------------------"
print "No of Nodal Forces:",load_group.item(0).attributes['N'].value,
load_group_no = len(load_group)
for group_no in range(load_group_no):
                for element in load_group.item(group_no).getElementsByTagName('NodalForce'):
                        print "\nLoad_ID:",element.getElementsByTagName('Id').item(0).firstChild.nodeValue,
                        print "\nNodal Force Type:",element.attributes['Type'].value
                        print "\nForce in X:",element.getElementsByTagName('Fx').item(0).firstChild.nodeValue,
                        print "\nForce in Y:",element.getElementsByTagName('Fy').item(0).firstChild.nodeValue,
                        print "\nForce in Z:",element.getElementsByTagName('Fz').item(0).firstChild.nodeValue,
print "\n-----------------------------------"
print "Where these forces are applied"
print "-----------------------------------"
node_load = ak3dom.getElementsByTagName('NodesWithLoads')
for element in node_load.item(0).getElementsByTagName('Loaded'):
                print "\nNode no:",element.getElementsByTagName('Node').item(0).firstChild.nodeValue,
                print "\tLoad Id at this Node:",element.getElementsByTagName('Load').item(0).firstChild.nodeValue,
print "\n-----------------------------------"
print "Description of Nodal Boundary Condition"
print "-----------------------------------"
node_bc = ak3dom.getElementsByTagName('NodeBCs')
print "\nNo of Nodal boundary conditions:",node_bc.item(0).attributes['N'].value,
node_bc_no = len(node_bc)
for group_no in range(node_bc_no):
                for element in node_bc.item(group_no).getElementsByTagName('NodeBC'):
                        print "\nNode Bc ID:",element.getElementsByTagName('Id').item(0).firstChild.nodeValue,
                        print "\nNode BC Type:",element.attributes['Type'].value
                        print "\nNode BC Name:",element.attributes['Name'].value
                        print "\nu1:",element.getElementsByTagName('u1').item(0).firstChild.nodeValue,
                        print "\t It's Value:",element.getElementsByTagName('valu1').item(0).firstChild.nodeValue,
                        print "\nu2:",element.getElementsByTagName('u2').item(0).firstChild.nodeValue,
                        print "\t It's Value:",element.getElementsByTagName('valu2').item(0).firstChild.nodeValue,
                        print "\nu3:",element.getElementsByTagName('u3').item(0).firstChild.nodeValue,
                        print "\t It's Value:",element.getElementsByTagName('valu3').item(0).firstChild.nodeValue,
                        print "\nw1:",element.getElementsByTagName('w1').item(0).firstChild.nodeValue,
                        print "\t It's Value:",element.getElementsByTagName('valw1').item(0).firstChild.nodeValue,
                        print "\nw2:",element.getElementsByTagName('w2').item(0).firstChild.nodeValue,
                        print "\t It's Value:",element.getElementsByTagName('valw2').item(0).firstChild.nodeValue,
                        print "\nw3:",element.getElementsByTagName('w3').item(0).firstChild.nodeValue,
                        print "\t It's Value:",element.getElementsByTagName('valw3').item(0).firstChild.nodeValue,
print "\n-----------------------------------"
print "Where we have these boundary condition"
print "-----------------------------------"
fixed_node=ak3dom.getElementsByTagName('FixedNodes')
print "No of Fixed Nodes:",fixed_node.item(0).attributes['N'].value,
for element in fixed_node.item(0).getElementsByTagName('Fixed'):
        print "\nNode no:",element.getElementsByTagName('Node').item(0).firstChild.nodeValue,
        print "\tNode_BC at this Node:",element.getElementsByTagName('BC').item(0).firstChild.nodeValue,

#---------------------------------------------#
#---------Writing-Boundary Conditions---------#
#---------------------------------------------#
f.write('\n**\n** KINEMATIC/DISTRIBUTING COUPLING\n**')
f.write('\n*COUPLING, CONSTRAINT NAME=COUPLING_1, REF NODE=1, SURFACE=SURF_COUPLING_1\n*KINEMATIC')
f.write('\n\t   1,        3')
fixed_node=ak3dom.getElementsByTagName('FixedNodes')
for element in fixed_node.item(0).getElementsByTagName('Fixed'):
        f.write('\n'+element.getElementsByTagName('Node').item(0).firstChild.nodeValue+', ')
        f.write(element.getElementsByTagName('BC').item(0).firstChild.nodeValue+'.')

#---------------------------------------------#
#-----Writing-Material-Specifications---------#
#---------------------------------------------#
material_group =ak3dom.getElementsByTagName('Materials')
no_of_group2 = len(material_group)                                                                                                                                                                                                                
for group_no in range(no_of_group2):
        for element in material_group.item(group_no).getElementsByTagName('Material'):
            f.write('\n**--------------------------------------------------------------------')    
            f.write('\n'+'*MATERIAL, '+'NAME='+element.attributes['Name'].value)
            f.write('\n'+'*ELASTIC')
            e=int(element.getElementsByTagName('E').item(0).firstChild.nodeValue)
            e=e/1000000
            f.write('\n '+str(e)+', '+element.getElementsByTagName('nu').item(0).firstChild.nodeValue)
            f.write('\n'+'*DENSITY')
            d=float(element.getElementsByTagName('rho').item(0).firstChild.nodeValue)
            d=d/1000
            f.write('\n '+str(d)+'e-09')
f.write('\n**---------------------------------------------------')
element_groups = ak3dom.getElementsByTagName('Elements')
no_of_group = len(element_groups)
for group_no in range(no_of_group):
      f.write('\n'+'*SHELL SECTION, '+'ELSET='+element_groups.item(group_no).attributes['Group'].value+', '+'MATERIAL=')
      mat=int(element_groups.item(group_no).attributes['Material'].value)
      f.write(material_group.item(0).getElementsByTagName('Material').item(mat-1).attributes['Name'].value)
      f.write('\n\t\t\t\t\t  1.,')
#-----------------------------------------#
#---------------End-Segment---------------#
#-----------------------------------------#
f.write('\n**---------------------------------------------------')
f.write('\n*Boundary, OP=NEW')
f.write('\n1, 1, 6, 0.')
f.write('\n**---------------------------------------------------')
f.write('\n*Step, name=LF01')
f.write('\n*STATIC')
f.write('\n**')
f.write('\n*CLOAD, OP=NEW')
f.write('\n2,       1,             -100             ')
f.write('\n**')
f.write('\n*Output, field')
f.write('\n*ELEMENT OUTPUT,POSITION=CENTROIDAL')
f.write('\nMISESMAX')
f.write('\n*NODE OUTPUT') 
f.write('\nU,')
f.write('\n**')
f.write('\n*END STEP')


f.write('\n**---------------------------------------------------')
f.write('\n*Step, name=LF02')
f.write('\n*STATIC')
f.write('\n**')
f.write('\n*CLOAD, OP=NEW')
f.write('\n2,       2,            -25            ')
f.write('\n**')
f.write('\n*Output, field')
f.write('\n*ELEMENT OUTPUT,POSITION=CENTROIDAL')
f.write('\nMISESMAX')
f.write('\n*NODE OUTPUT ')
f.write('\nU,')
f.write('\n**')
f.write('\n*END STEP')

#---------------------------------------------#
#----------------General Info-----------------#
#-----------(Only for displaying)-------------#
#---------------------------------------------#
print "\n-----------------------------------"
print "-----------General Info------------"
print "-----------------------------------"
print "\nRevision No:",ak3dom.getElementsByTagName('Revision').item(0).firstChild.nodeValue,
print "\nDescription:",ak3dom.getElementsByTagName('Desc').item(0).firstChild.nodeValue,
print "\nType of Analysis:",ak3dom.getElementsByTagName('Analysis').item(0).attributes['Type'].value,
print "\nType of data:"
print "\nstp?",ak3dom.getElementsByTagName('Output').item(0).getElementsByTagName('stp').item(0).firstChild.nodeValue,
print "\ntec?",ak3dom.getElementsByTagName('Output').item(0).getElementsByTagName('tec').item(0).firstChild.nodeValue,
print "\nvtk?",ak3dom.getElementsByTagName('Output').item(0).getElementsByTagName('vtk').item(0).firstChild.nodeValue,
print "\navs?",ak3dom.getElementsByTagName('Output').item(0).getElementsByTagName('avs').item(0).firstChild.nodeValue,
print "\nak3?",ak3dom.getElementsByTagName('Output').item(0).getElementsByTagName('ak3').item(0).firstChild.nodeValue,
print "\nenergy?",ak3dom.getElementsByTagName('Output').item(0).getElementsByTagName('energy').item(0).firstChild.nodeValue,
print "\n Writing into .inp file over.."
f.close()
