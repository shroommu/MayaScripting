#Alexa Kruckenberg 11/4/18
#OC DO NOT STEAL

import maya.cmds as cmds

#create attributes on the transform control
def CreateIKFKAttributes():
    xformCtrl = cmds.ls(selection = 1)
    
    cmds.addAttr (xformCtrl, longName = "Arm_L_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)
    cmds.addAttr (xformCtrl, longName = "Arm_R_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)
    cmds.addAttr (xformCtrl, longName = "Leg_L_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)
    cmds.addAttr (xformCtrl, longName = "Leg_R_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)




#sets SDKs for IKFK parent constraints. select transform control first, then select as many constraints as you want.
#IMPORTANT!!! attrNum should be set equal to the order of the attributes on your transform control
#If you used the above code, Arm_L_IKFK is attrNum = 1, Arm_R_IKFK = 2, so on and so forth
def RKConstraintSetDrivenKey(attrNum):
    sels = cmds.ls(selection = 1)

    xformCtrl = sels[0]
    
    sels.remove(xformCtrl)

    for var in range(0, len(sels)):

        constraint = sels[var]

        #get attributes
        FKAttr = cmds.listAttr(constraint, userDefined = 1) [0]
        IKAttr = cmds.listAttr(constraint, userDefined = 1) [1]
        ctrlAttr = cmds.listAttr(xformCtrl, userDefined = 1) [attrNum - 1]

        #set attributes to FK
        cmds.setAttr((xformCtrl + "." + ctrlAttr), 0)
        cmds.setAttr((constraint + "." + FKAttr), 1)
        cmds.setAttr((constraint + "." + IKAttr), 0)

        #key attributes
        cmds.setDrivenKeyframe((constraint + "." + FKAttr), cd = (xformCtrl + "." + ctrlAttr))
        cmds.setDrivenKeyframe((constraint + "." + IKAttr), cd = (xformCtrl + "." + ctrlAttr))

        #set attributes to IK
        cmds.setAttr((xformCtrl + "." + ctrlAttr), 1)
        cmds.setAttr((constraint + "." + FKAttr), 0)
        cmds.setAttr((constraint + "." + IKAttr), 1)

        #key attributes
        cmds.setDrivenKeyframe((constraint + "." + FKAttr), cd = (xformCtrl + "." + ctrlAttr))
        cmds.setDrivenKeyframe((constraint + "." + IKAttr), cd = (xformCtrl + "." + ctrlAttr))

        cmds.setAttr((xformCtrl + "." + ctrlAttr), 0)




#sets visibility of control to SDK. select transform control first, then select as many controls as you want.
#IMPORTANT!!! only select IK controls or FK controls, not both. set isFK to 1 for FK controls, and to 0 for IK controls
#IMPORTANT!!! attrNum should be set equal to the order of the attributes on your transform control
#If you used the above code, Arm_L_IKFK is attrNum = 1, Arm_R_IKFK = 2, so on and so forth
def RKCtrlSetDrivenKey(attrNum, isFK = 1):
    sels = cmds.ls(selection = 1)
    print(sels)

    xformCtrl = sels[0]
    print(xformCtrl)
    sels.remove(xformCtrl)
    
    for var in range(0, len(sels)):
        ctrl = sels[var]

        xformCtrlAttr = ctrlAttr = cmds.listAttr(xformCtrl, userDefined = 1) [attrNum - 1]
        
        if isFK == 1:
            cmds.setAttr((xformCtrl + "." + xformCtrlAttr), 0)
            cmds.setAttr((ctrl + ".visibility"), 1)

            cmds.setDrivenKeyframe((ctrl + ".visibility"), cd = (xformCtrl + "." + xformCtrlAttr))

            cmds.setAttr((xformCtrl + "." + xformCtrlAttr), 1)
            cmds.setAttr((ctrl + ".visibility"), 0)

            cmds.setDrivenKeyframe((ctrl + ".visibility"), cd = (xformCtrl + "." + xformCtrlAttr))

        else:
            cmds.setAttr((xformCtrl + "." + xformCtrlAttr), 0)
            cmds.setAttr((ctrl + ".visibility"), 0)

            cmds.setDrivenKeyframe((ctrl + ".visibility"), cd = (xformCtrl + "." + xformCtrlAttr))

            cmds.setAttr((xformCtrl + "." + xformCtrlAttr), 1)
            cmds.setAttr((ctrl + ".visibility"), 1)

            cmds.setDrivenKeyframe((ctrl + ".visibility"), cd = (xformCtrl + "." + xformCtrlAttr))


#use these lines individually to call the different functions as you need them
RKParentConstrain()

RKConstraintSetDrivenKey(1)

RKCtrlSetDrivenKey(1, 1)