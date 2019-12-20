import maya.cmds as cmds
import random

class Toolbox():

    def __init__(self):
        self.form = "form"
        self.colorIndex = 1
        
    #create UI
    def Create(self):
        
        #main layout with tabs
        self.form = cmds.formLayout()
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout( self.form, edit=True, attachForm=((self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )
        
        #modelling tab
        self.child1 = cmds.rowColumnLayout(parent = self.tabs, numberOfColumns=1)
        
        #duplicate and scatter
        self.dupScatFrame = cmds.frameLayout(parent = self.child1, label = "Duplicate and Scatter", collapsable = True, collapse = True)
        self.dupScatRC = cmds.rowColumnLayout(parent = self.dupScatFrame, numberOfColumns = 3)

        cmds.text(parent = self.dupScatRC, label = "X range")
        self.xMinField = cmds.floatField(parent = self.dupScatRC, value = -10)
        self.xMaxField = cmds.floatField(parent = self.dupScatRC, value = 10)
        cmds.text(parent = self.dupScatRC, label = "Y range")
        self.yMinField = cmds.floatField(parent = self.dupScatRC, value = -10)
        self.yMaxField = cmds.floatField(parent = self.dupScatRC, value = 10)
        cmds.text(parent = self.dupScatRC, label = "Z range")
        self.zMinField = cmds.floatField(parent = self.dupScatRC, value = -10)
        self.zMaxField = cmds.floatField(parent = self.dupScatRC, value = 10)
        cmds.text(parent = self.dupScatRC, label = "Number of Duplicates")
        self.dupNumField = cmds.intField(parent = self.dupScatRC, value = 10)

        self.dupScatCol = cmds.columnLayout(parent = self.dupScatFrame)
        cmds.button(parent = self.dupScatFrame, label = "Duplicate", command = lambda x: self.DupAndScatter(cmds.intField(self.dupNumField, q = 1, v = 1), cmds.floatField(self.xMinField , q = 1, v = 1), cmds.floatField(self.xMaxField , q = 1, v = 1), cmds.floatField(self.yMinField , q = 1, v = 1), cmds.floatField(self.yMaxField , q = 1, v = 1), cmds.floatField(self.zMinField , q = 1, v = 1), cmds.floatField(self.zMaxField , q = 1, v = 1)))
        
        #rigging tab
        self.child2 = cmds.rowColumnLayout(parent = self.tabs, numberOfColumns=1)
        
        #locator creator
        self.createLocatorFrame = cmds.frameLayout(parent = self.child2, label = "Create Locators", collapsable = True, collapse = True)
        self.createLocatorRC = cmds.rowColumnLayout(parent = self.createLocatorFrame, numberOfColumns = 2)
        cmds.text(parent = self.createLocatorRC, label = "Type")
        self.createLocatorMenu = cmds.optionMenu(parent = self.createLocatorRC)
        cmds.menuItem(parent = self.createLocatorMenu, label = "Center of Objects")
        cmds.menuItem(parent = self.createLocatorMenu, label = "Center of Components")
        cmds.button(parent = self.createLocatorFrame, label = "Create Locator", command = lambda x: self.CreateLocator(cmds.optionMenu(self.createLocatorMenu, q = True, v = True)))

        cmds.separator(parent = self.child2, style = "double")

        #joint creator
        self.createJointFrame = cmds.frameLayout(parent = self.child2, label = "Create Joints", collapsable = True, collapse = True)
        cmds.button(parent = self.createJointFrame, label = "Create Joints", command = lambda x: self.CreateJoints())

        cmds.separator(parent = self.child2, style = "double")
        
        #joint orient
        self.jointOrientFrame = cmds.frameLayout(parent = self.child2, label = "Orient Joints", collapsable = True, collapse = True)
        
        self.primaryAxisRC = cmds.radioButtonGrp(parent = self.jointOrientFrame, label = "Primary Axis:", ad3 = 1, cw3 = [20, 20, 20], labelArray3 = ["X", "Y", "Z"], numberOfRadioButtons = 3, select = 1)

        self.secondaryAxisRC = cmds.radioButtonGrp(parent = self.jointOrientFrame,  label = "Secondary Axis:", ad3 = 1, cw3 = [20, 20, 20], labelArray3 = ["X", "Y", "Z"], numberOfRadioButtons = 3, select = 3)

        self.SAORC = cmds.radioButtonGrp(parent = self.jointOrientFrame, label = "Secondary Axis World Orientation", ad3 = 1, cw3 = [20, 20, 20], labelArray3 = ["X", "Y", "Z"], numberOfRadioButtons = 3, select = 1)
        
        self.upOrDown = cmds.optionMenu(parent = self.jointOrientFrame)
        cmds.menuItem(parent = self.upOrDown, label = "+")
        cmds.menuItem(parent = self.upOrDown, label = "-")
        
        cmds.button(parent = self.jointOrientFrame, label = "Orient Joints", command = lambda x: self.OrientJoints(self.QueryRadioButtonGrp(self.primaryAxisRC), self.QueryRadioButtonGrp(self.secondaryAxisRC), self.QueryRadioButtonGrp(self.SAORC), cmds.optionMenu(self.upOrDown, q = 1, value = 1), True, True, True))
        
        cmds.button(parent = self.jointOrientFrame, label = "Freeze Rotations", command = lambda x: self.FreezeRotation())
        
        cmds.separator(parent = self.child2, style = "double")
        
        #ik solvers
        self.ikSolversFrame = cmds.frameLayout(parent = self.child2, label = "IK Solvers", collapsable = True, collapse = True)
        cmds.text(parent = self.ikSolversFrame, label = "Spline IK")
        self.splineSelectHierarchyCB = cmds.checkBox(parent = self.ikSolversFrame, label = "Select Hierarchy")
        cmds.button(parent = self.ikSolversFrame, label = "Create Spline IK", command = lambda x: self.SplineIK(cmds.checkBox(self.splineSelectHierarchyCB, query = 1, value = 1)))
        
        cmds.separator(parent = self.child2, style = "double")

        #control creator
        self.createControlFrame = cmds.frameLayout(parent = self.child2, label = "Create Controls", collapsable = True, collapse = True)
        self.createControlRC = cmds.rowColumnLayout(parent = self.createControlFrame, numberOfColumns=2)
        self.createControlGrid = cmds.gridLayout(parent = self.createControlFrame, numberOfColumns = 8)
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 0, 0), command = lambda x: self.SetColor(1) )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.75, 0.75, 0.75), command = lambda x: self.SetColor(2) )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.5, 0.5, 0.5), command = lambda x: self.SetColor(3) )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (.8, 0, 0.2), command = lambda x: self.SetColor(4)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 0, .4), command = lambda x: self.SetColor(5)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 0, 1), command = lambda x: self.SetColor(6)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, .3, 0), command = lambda x: self.SetColor(7)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.2, 0, 0.3), command = lambda x: self.SetColor(8)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (.8, 0, .8), command = lambda x: self.SetColor(9)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.6, 0.3, 0.2), command = lambda x: self.SetColor(10)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.25, 0.13, 0.13), command = lambda x: self.SetColor(11)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.7, .2, 0), command = lambda x: self.SetColor(12)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (1, 0, 0), command = lambda x: self.SetColor(13)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 1, 0), command = lambda x: self.SetColor(14)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 0.3, 0.6), command = lambda x: self.SetColor(15)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (1, 1, 1), command = lambda x: self.SetColor(16)  )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (1, 1, 0), command = lambda x: self.SetColor(17)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 1, 1), command = lambda x: self.SetColor(18)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 1, .8), command = lambda x: self.SetColor(19)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (1, .7, .7), command = lambda x: self.SetColor(20)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.9, .7, .5), command = lambda x: self.SetColor(21)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (1, 1, 0.4), command = lambda x: self.SetColor(22)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0, 0.7, .4), command = lambda x: self.SetColor(23)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (.6, .4, .2), command = lambda x: self.SetColor(24)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (.63, .63, .17), command = lambda x: self.SetColor(25)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.4, 0.6, 0.2), command = lambda x: self.SetColor(26)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.2, 0.63, 0.35), command = lambda x: self.SetColor(27)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.18, 0.63, 0.63), command = lambda x: self.SetColor(28)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.18, 0.4, 0.63), command = lambda x: self.SetColor(29)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.43, 0.18, 0.63), command = lambda x: self.SetColor(30)   )
        cmds.button( label = "", parent = self.createControlGrid, backgroundColor = (0.63, 0.18, 0.4), command = lambda x: self.SetColor(31)   )
        cmds.text(parent = self.createControlRC, label = "Control Type")
        self.createControlOptnMenu = cmds.optionMenu(parent = self.createControlRC)
        cmds.menuItem(parent = self.createControlOptnMenu, label = "")
        cmds.menuItem(parent = self.createControlOptnMenu, label = "Circle")
        cmds.menuItem(parent = self.createControlOptnMenu, label = "Square")
        cmds.menuItem(parent = self.createControlOptnMenu, label = "Flower")
        cmds.text(parent = self.createControlRC, label = "Constrain to Joint")
        self.createControlCheckbox = cmds.checkBox(parent = self.createControlRC, value = False, label = "")
        cmds.text(parent = self.createControlRC, label = "Color Joints")
        self.colorJointsCheckbox = cmds.checkBox(parent = self.createControlRC, value = False, label = "")
        cmds.button(parent = self.createControlFrame, label = "Create Controls", command = lambda x: self.CreateControl(cmds.optionMenu(self.createControlOptnMenu, q = True, v = True), self.colorIndex, cmds.checkBox(self.createControlCheckbox, q= True, v = True), cmds.checkBox(self.colorJointsCheckbox, q= True, v = True)))
        cmds.text(parent = self.createControlRC, label = "Control Color:")
        
        cmds.separator(parent = self.child2, style = "double")
        
        #RK system tools
        self.rkFrame = cmds.frameLayout(parent = self.child2, label = "IKFK System", collapsable = True, collapse = True)
        
        cmds.button(parent = self.rkFrame, label = "Create IK FK Chains", command = lambda x: self.CreateIKFKJoints())
        
        self.scrollList = cmds.textScrollList(parent = self.rkFrame)
        cmds.button(parent = self.rkFrame, label = "Add", command = lambda x: self.AddToTextScrollList(self.scrollList))
        cmds.button(parent = self.rkFrame, label = "Create Transform Control Attributes", command = lambda x: self.CreateIKFKAttributes(self.QueryTextScrollList(self.scrollList)), ann = "Select your Transform control to run this command. Will create an IKFK attribute for two arms and two legs")

        self.rkRC1 = cmds.rowColumnLayout(parent = self.rkFrame, numberOfColumns=2)
        cmds.text(parent = self.rkRC1, label = "Attribute Number", ann = "Check the order of the user-created attributes on Transform control to get this number")
        self.rkAttrNum1 = cmds.intField(parent = self.rkRC1, value = 1)
        cmds.button(parent = self.rkFrame, label = "Key IKFK Switch", command = lambda x: self.RKConstraintSetDrivenKey(self.QueryTextScrollList(self.scrollList), cmds.intField(self.rkAttrNum1, q = 1, v = 1)), ann  = "Select your Transform control first, then select the parent constraints on your RK joint chain for one joint system (ie for the left arm)")

        self.rkRC2 = cmds.rowColumnLayout(parent = self.rkFrame, numberOfColumns=2)
        cmds.text(parent = self.rkRC2, label = "Attribute Number", ann = "Check the order of the user-created attributes on Transform control to get this number")
        self.rkAttrNum2 = cmds.intField(parent = self.rkRC2, value = 1)
        cmds.text(parent = self.rkRC2, label = "Control Type")
        self.rkOptnMenu = cmds.optionMenu(parent = self.rkRC2)
        cmds.menuItem(parent = self.rkOptnMenu, label = "FK")
        cmds.menuItem(parent = self.rkOptnMenu, label = "IK")
        cmds.button(parent = self.rkFrame, label = "Key Control Visibility", command = lambda x: self.RKCtrlSetDrivenKey(self.QueryTextScrollList(self.scrollList), cmds.intField(self.rkAttrNum2, q = 1, v = 1), cmds.optionMenu(self.rkOptnMenu, q = 1, v = 1)) , ann = "Select Transform control first, then select the controls for one joint system (ie the left arm IK controls)")
        
        cmds.separator(parent = self.child2, style = "double")

        #skinning animator
        self.skinAnimFrame = cmds.frameLayout(parent = self.child2, label = "Skinning Auto Animator", collapsable = True, collapse = True)
        cmds.button(parent = self.skinAnimFrame, label = "Animate", command = lambda x: self.SkinningAnim())
        cmds.button(parent = self.skinAnimFrame, label = "Clear Keys", command = lambda x: cmds.cutKey())

        
        
        #utility tab
        self.child3 = cmds.rowColumnLayout(parent = self.tabs, numberOfColumns=1)

        #renamer
        self.renamerFrame = cmds.frameLayout(parent = self.child3, label = "Renamer", collapsable = True, collapse = True)
        self.renamerRC = cmds.rowColumnLayout(parent = self.renamerFrame, numberOfColumns = 2)

        cmds.text(parent = self.renamerRC, label = "Name")
        self.nameField = cmds.textField(parent = self.renamerRC, text = "name")
        cmds.text(parent = self.renamerRC, label = "Number Padding")
        self.numPadField = cmds.textField(parent = self.renamerRC, text = "00")
        cmds.text(parent = self.renamerRC, label = "Number")
        self.numField = cmds.intField(parent = self.renamerRC, value = 1)
        cmds.text(parent = self.renamerRC, label = "Suffix")
        self.suffixField = cmds.textField(parent = self.renamerRC, text = "suffix")

        cmds.button(parent = self.renamerFrame, label = "Rename and Number", command = lambda x: self.RenameAndNumber(cmds.textField(self.nameField, q = 1, text = 1), cmds.textField(self.numPadField, q = 1, text = 1), cmds.intField(self.numField, q = 1, v = 1), cmds.textField(self.suffixField, q = 1, text = 1)))

        #filter selection
        self.filselFrame = cmds.frameLayout(parent = self.child3, label = "Filter Selection", collapsable = True, collapse = True)
        self.filselRC = cmds.rowColumnLayout(parent = self.filselFrame, numberOfColumns = 2)
        cmds.text(parent = self.filselRC, label = "Select Hierarchy")
        self.filselCheckbox = cmds.checkBox(parent = self.filselRC, value = True, label = "")
        cmds.text(parent = self.filselRC, label = "Node Type")
        self.filselText = cmds.textField(parent = self.filselRC)
        cmds.button(parent = self.filselFrame, label = "Filter Selection", command = lambda x: self.FilterSelection(cmds.checkBox(self.filselCheckbox, q = 1, v = 1), cmds.textField(self.filselText, q = 1, text = 1)))

        #randomize selection
        self.randSelFrame = cmds.frameLayout(parent = self.child3, label = "Randomize Selection", collapsable = True, collapse = True)
        self.randSelRC = cmds.rowColumnLayout(parent = self.randSelFrame, numberOfColumns = 2)

        cmds.text(parent = self.randSelRC, label = "Percent of Selection")
        self.percentSelField = cmds.floatField(parent = self.randSelRC, value = 50)
        cmds.button(parent = self.randSelFrame, label = "Randomize", command = lambda x: self.RandomizeSelection(cmds.floatField(self.percentSelField, q = 1, v = 1)))
        
        #set up tab layout
        cmds.tabLayout( self.tabs, edit=True, tabLabel=((self.child1, 'Modelling'), (self.child2, 'Rigging'), (self.child3, 'Utility')) )
        



    #functions

    def DupAndScatter (self, dupNum, rangeMinX, rangeMaxX, rangeMinY, rangeMaxY, rangeMinZ, rangeMaxZ):
        
        #store selected object
        sels = cmds.ls (selection = 1)
        
        #duplicate and move selected object according to min/max and dupNum vars
        for var in range(0, dupNum):
        
            #duplicate and assign to sels
            cmds.duplicate ( sels, rr= 1)
            sels = cmds.ls (selection = 1)
            
            #generate random point
            tempX = random.randrange(rangeMinX, rangeMaxX)
            tempY = random.randrange(rangeMinY, rangeMaxY)
            tempZ = random.randrange(rangeMinZ, rangeMaxZ)
            
            sel = sels[0]
            
            #move to random point
            cmds.setAttr (sel + ".translateX", tempX) 
            cmds.setAttr (sel + ".translateY", tempY) 
            cmds.setAttr (sel + ".translateZ", tempZ)    


    def CreateLocator(self, option):
        #get selection
        sels = cmds.ls(sl = 1)

        if option == "Center of Objects":
            #duplicate selection, combine duplicates into one obj, query bounding box of new obj, and find center of bounding box
            dups = cmds.duplicate(sels, rr = 1)
            dups = cmds.polyUnite(dups, ch = 1, mergeUVSets = 1, centerPivot = 1) [0]
            bbox = cmds.xform(dups, boundingBox = 1, query = 1)
            pivot = [(bbox[0] + bbox[3])/2, (bbox[1] + bbox[4])/2, (bbox[2] + bbox[5])/2]

            #clear history, delete duplicate obj
            cmds.delete(dups, ch = 1)
            cmds.delete(dups)

            #create locator, move to center of objs
            loc = cmds.spaceLocator() [0]
            cmds.xform(loc, translation = pivot, worldSpace = 1)

        elif option == "Center of Components":
            #find the pivot of the obj, create a locator, move locator to pivot
            bbox = cmds.xform(sels, boundingBox = 1, query = 1, ws = True)
            pivot = [(bbox[0] + bbox[3])/2, (bbox[1] + bbox[4])/2, (bbox[2] + bbox[5])/2]

            #create locator, move to center of objs
            loc = cmds.spaceLocator() [0]
            cmds.xform(loc, translation = pivot)

        
    def CreateJoints(self):
        
        #get selection
        sels = cmds.ls(sl = 1)
        joints = []

        for var in range(0, len(sels)):
            #clear selection so maya doesn't throw a joint-related error
            cmds.select(clear = 1)

            #create joint, move to sels[var]
            joint = cmds.joint()
            cmds.matchTransform(joint, sels[var])
            
            #add current joint to list of joints
            joints.append(joint)
                
            #clear selection again for good measure
            cmds.select(clear = 1)
            
            #on every loop except the first, parent the current joint to the last joint created
            if var is not 0:
                cmds.parent(joint, joints[var - 1])


    def QueryRadioButtonGrp(self, radioGrp):
        return cmds.radioButtonGrp(radioGrp, query = 1, select = 1)


    def OrientJoints(self, primaryAxis, secondaryAxis, secondaryAxisOrientation, upOrDown, selectHierarchy, orientToWorld, zeroLastJoint):
        
        if primaryAxis == 1:
            primaryAxis = "x"
        elif primaryAxis == 2:
            primaryAxis = "y"
        else:
            primaryAxis = "z"
            
        if secondaryAxis == 1:
            secondaryAxis = "x"
        elif secondaryAxis == 2:
            secondaryAxis = "y"
        else:
            secondaryAxis = "z"
            
        if secondaryAxisOrientation == 1:
            secondaryAxisOrientation = "x"
        elif secondaryAxisOrientation == 2:
            secondaryAxisOrientation = "y"
        else:
            secondaryAxisOrientation = "z"
        
        if(selectHierarchy == 1):
            cmds.select(hierarchy = 1)
            
        sels = cmds.ls(selection = 1)
            
        tertiaryAxis = None
        
        if (primaryAxis == "x" and secondaryAxis == "y") or (primaryAxis == "y" and secondaryAxis == "x"):
            tertiaryAxis = "z"
        elif (primaryAxis == "x" and secondaryAxis == "z") or (primaryAxis == "z" and secondaryAxis == "x"):
            tertiaryAxis = "y"
        elif (primaryAxis == "y" and secondaryAxis == "z") or (primaryAxis == "z" and secondaryAxis == "y"):
            tertiaryAxis = "x"
        else:
            cmds.warning("Primary and secondary axes are the same")
            
        if upOrDown == "+":
            upOrDown = "up"
        else:
            upOrDown = "down"
            
        secondaryAxisOrientation += upOrDown
        
        axisOrder = primaryAxis + secondaryAxis + tertiaryAxis
                
        for sel in sels:
            
            if(cmds.listRelatives(sel, children = 1) == None):
                cmds.setAttr(sel + ".jointOrientX", 0) 
                cmds.setAttr(sel + ".jointOrientY", 0) 
                cmds.setAttr(sel + ".jointOrientZ", 0)
            else:
                cmds.joint(sel, edit = 1, orientJoint = axisOrder, secondaryAxisOrient = secondaryAxisOrientation)


    def FreezeRotation(self):
        sels = cmds.ls(selection = 1)
        
        for sel in sels:
            cmds.makeIdentity(sel, rotate = 1, apply = 1)


    def CreateControl(self, controlShape, colorIndex, doConstrain, colorJoint):
            
        if controlShape != "":
            sels = cmds.ls (selection = True)
    
            if len(sels) != 0:
            
                for var in range(0, len(sels) - 1):
                    if controlShape == "Circle":
                        control = cmds.circle()
    
                    elif controlShape == "Square":
                        control = cmds.nurbsSquare
    
                    elif controlShape == "Flower":
                        control = cmds.circle()
                        cmds.select (control[0] + ".cv[0]", control[0] + ".cv[2]", control[0] + ".cv[4]", control[0] + ".cv[6]", replace = 1)
                        cmds.scale(-0.35, -0.35, -0.35, relative = True) 
                        cmds.select(control)
                        cmds.makeIdentity()
                
    
                    controlGroup = cmds.group (control)
                    cmds.matchTransform(controlGroup, sels[var])
    
                    tokenizedSel = sels[var].split("_")
                    sizeOfTokenizedSel = len(tokenizedSel)
                    nameOfControl = ""
    
                    if sizeOfTokenizedSel > 1:
                        for var in range(0, (sizeOfTokenizedSel - 1)):
                            nameOfControl += tokenizedSel[var] + "_"
    
                    else:
                        nameOfControl = tokenizedSel
                        nameOfControl = nameOfControl[0] + "_"

                    if colorJoint:    
                        self.SetJointColor(sels[var], colorIndex)

                    self.SetControlColor(control[0], colorIndex)
    
                    if doConstrain == 1:
                        self.ConstrainToJoint(sels[var], control)
                        
                    cmds.rename (str(control[0]), (nameOfControl + "CTRL"))
                    cmds.rename (controlGroup, (nameOfControl + "CTRL_GRP"))
            
            else:
                
                if controlShape == "Circle":
                    control = cmds.circle
                
                elif controlShape == "Square":
                    control = cmds.nurbsSquare()
                    
                elif controlShape == "Flower":
                        control = cmds.circle()
                        cmds.select (control[0] + ".cv[0]", control[0] + ".cv[2]", control[0] + ".cv[4]", control[0] + ".cv[6]", replace = 1)
                        cmds.scale(-0.35, -0.35, -0.35, relative = True) 
                        cmds.select(control)
                        cmds.makeIdentity()
                
    
                self.SetControlColor(control[0], colorIndex)
                cmds.group(control)
            
        else:
            cmds.warning("No control shape selected")
    
    
    def ConstrainToJoint(self, thisJoint, thisControl):
        cmds.parentConstraint (thisControl, thisJoint)
    
    
    def SetColor(self, index):
        self.colorIndex = index


    def SetJointColor(self, thisJoint, thisColor):
        cmds.setAttr (thisJoint + ".overrideEnabled", 1) 
        cmds.setAttr (thisJoint + ".overrideColor", thisColor) 


    def SetControlColor (self, thisControl, thisColor):
        cmds.setAttr (thisControl + ".overrideEnabled", 1)
        cmds.setAttr (thisControl + ".overrideColor", thisColor)


    def AddToTextScrollList(self, thisTSC):
        cmds.textScrollList(thisTSC, edit = 1, append = cmds.ls(selection = 1))
        
        
    def QueryTextScrollList(self, thisTSC):
        return cmds.textScrollList(thisTSC, q = 1, si = 1)
        
        
    def CreateIKFKJoints(self):
        sels = cmds.ls(selection = 1)
        
        fkChain = cmds.duplicate(sels, renameChildren = 1)
        ikChain = cmds.duplicate(sels, renameChildren = 1)
        
        nameOfIKHandle = ""
        tokenizedSels = sels[0].split("_")
        for var in range(0, len(tokenizedSels) - 2):
            nameOfIKHandle += tokenizedSels[var] + "_"
                
        cmds.ikHandle(name = nameOfIKHandle + "IK_HNDL", startJoint = ikChain[0], endEffector = cmds.listRelatives(cmds.listRelatives(ikChain[0], children = 1)[0], children = 1)[0])
        
        for var in reversed(range(0, 3)):
            currentRKJoint = sels[0]
            currentFKJoint = fkChain[0]
            currentIKJoint = ikChain[0]
            
            if var != 0:
                for var2 in range(0, var):
                    currentRKJoint = cmds.listRelatives(currentRKJoint, children = 1)[0]
                    currentFKJoint = cmds.listRelatives(currentFKJoint, children = 1)[0]
                    currentIKJoint = cmds.listRelatives(currentIKJoint, children = 1)[0]
            cmds.parentConstraint(currentIKJoint, currentFKJoint, currentRKJoint)
                
            nameOfJoint = currentRKJoint
            
            cmds.rename(currentFKJoint, nameOfJoint.replace("RK", "FK"))
            cmds.rename(currentIKJoint, nameOfJoint.replace("RK", "IK"))
            
    def SplineIK(self, selectHierarchy):
                                
        if selectHierarchy:
            cmds.select(hierarchy = 1)
        sels = cmds.ls(selection = 1)
        
        lastJoint = ""
        
        for sel in sels:
            if cmds.listRelatives(sel, children = 1) == None:
                lastJoint = sel
                        
        curvePoints = list()
        
        for sel in sels:
            curvePoints.append(cmds.xform(sel, query = 1, translation = 1, worldSpace = 1))
            
        tokenizedSel = sels[0].split("_")
            
        spline = cmds.curve(editPoint = curvePoints, name = tokenizedSel[0] + "_spline_IK_CV")
        ikHndl = cmds.ikHandle(startJoint = sels[0], endEffector = lastJoint, createCurve = 0, curve = spline, solver = "ikSplineSolver", name = tokenizedSel[0] + "_spline_IK_HNDL")

        ctrlJointPositions = list()

        for var in range(0, len(sels), 2):
            ctrlJointPositions.append(cmds.xform(sels[var], query = 1, translation = 1, worldSpace = 1))
            
        print(ctrlJointPositions)
       
        
    def CreateIKFKAttributes(self, xformCtrl):
    
        cmds.addAttr (xformCtrl, longName = "Arm_L_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)
        cmds.addAttr (xformCtrl, longName = "Arm_R_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)
        cmds.addAttr (xformCtrl, longName = "Leg_L_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)
        cmds.addAttr (xformCtrl, longName = "Leg_R_IKFK", attributeType = "float", defaultValue = 0, minValue = 0, maxValue = 1, keyable = 1)


    def RKConstraintSetDrivenKey(self, xformCtrl, attrNum):
        sels = cmds.ls(selection = 1)

        for var in range(0, len(sels)):

            constraint = sels[var]

            #get attributes
            FKAttr = cmds.listAttr(constraint, userDefined = 1) [1]
            IKAttr = cmds.listAttr(constraint, userDefined = 1) [0]
            ctrlAttr = cmds.listAttr(xformCtrl, userDefined = 1) [attrNum - 1]

            #set attributes to FK
            cmds.setAttr((xformCtrl + "." + ctrlAttr), 1)
            cmds.setAttr((constraint + "." + FKAttr), 1)
            cmds.setAttr((constraint + "." + IKAttr), 0)

            #key attributes
            cmds.setDrivenKeyframe((constraint + "." + FKAttr), cd = (xformCtrl + "." + ctrlAttr))
            cmds.setDrivenKeyframe((constraint + "." + IKAttr), cd = (xformCtrl + "." + ctrlAttr))

            #set attributes to IK
            cmds.setAttr((xformCtrl + "." + ctrlAttr), 0)
            cmds.setAttr((constraint + "." + FKAttr), 0)
            cmds.setAttr((constraint + "." + IKAttr), 1)

            #key attributes
            cmds.setDrivenKeyframe((constraint + "." + FKAttr), cd = (xformCtrl + "." + ctrlAttr))
            cmds.setDrivenKeyframe((constraint + "." + IKAttr), cd = (xformCtrl + "." + ctrlAttr))

            cmds.setAttr((xformCtrl + "." + ctrlAttr), 0)


    def RKCtrlSetDrivenKey(self, xformCtrl, attrNum, controlType):
        sels = cmds.ls(selection = 1)
        
        for var in range(0, len(sels)):
            ctrl = sels[var]

            xformCtrlAttr = ctrlAttr = cmds.listAttr(xformCtrl, userDefined = 1) [attrNum - 1]
            
            if controlType is "FK":
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


    def SkinningAnim (self):
        sels = cmds.ls(sl = True) [0]
        
        cmds.currentTime(0)
        cmds.setKeyframe()
        
        cmds.currentTime(10)
        cmds.setAttr (str(sels) + ".rotateX", 90)
        cmds.setKeyframe()
        cmds.currentTime(30)
        cmds.setAttr (str(sels) + ".rotateX", -90)
        cmds.setKeyframe()
        cmds.currentTime(40)
        cmds.setAttr (str(sels) + ".rotateX", 0)
        cmds.setKeyframe()
        
        cmds.currentTime(50)
        cmds.setAttr (str(sels) + ".rotateY", 90)
        cmds.setKeyframe()
        cmds.currentTime(70)
        cmds.setAttr (str(sels) + ".rotateY", -90)
        cmds.setKeyframe()
        cmds.currentTime(80)
        cmds.setAttr (str(sels) + ".rotateY", 0)
        cmds.setKeyframe()
        
        cmds.currentTime(90)
        cmds.setAttr (str(sels) + ".rotateZ", 90)
        cmds.setKeyframe()
        cmds.currentTime(110)
        cmds.setAttr (str(sels) + ".rotateZ", -90)
        cmds.setKeyframe()
        cmds.currentTime(120)
        cmds.setAttr (str(sels) + ".rotateZ", 0)
        cmds.setKeyframe()


    def RenameAndNumber (self, newName, numPad, newNum, suffix):
        
        sels = cmds.ls (selection = 1)
        newNumPad = ""
        
        for sel in sels:
        
            newNumPad = ""
            numPadDiff = len(str(numPad)) - len(str(newNum))
            
            for var in range(0, numPadDiff):
            
                newNumPad = newNumPad + "0"
            

            newNumPadTemp = newNumPad + str(newNum)
            cmds.rename(sel, (newName + "_" + newNumPadTemp + "_" + suffix))
            newNum = newNum + 1


    def FilterSelection(self, selectHierarchy, nodeType):
        
        if selectHierarchy == True:
            cmds.select(hierarchy = True)
        
        sels = cmds.ls(sl = True)
        newSels = []

        for sel in sels:
            if cmds.nodeType(sel) == nodeType:
                parent = cmds.listRelatives(sel, parent = True) [0]
                newSels.append(parent)
        cmds.select(newSels)
        

    def RandomizeSelection (self, percentOfSel):
        
        sels = cmds.ls(sl = True)
        sizeOfSels = len(sels)
        newSels = []
        sizeOfNewSels = sizeOfSels * percentOfSel/100.0
        sizeOfNewSels = int(sizeOfNewSels)

        i = 0

        while i < sizeOfNewSels:
        
            rand = random.randrange(0, (sizeOfSels - 1))
            canAdd = 1

            for sel in newSels:

                if sel == sels[rand]:
                    canAdd = 0

            if(canAdd == 1):
                newSels.append(sels[rand])

                if(i == sizeOfNewSels):
                    break
                
                else:
                    i = i + 1
        cmds.select(newSels)






global myToolbox
myToolbox = Toolbox()


def CreateWorkspace():

    ws = "Custom Tools"
    
    if cmds.workspaceControl (ws, exists = True):
        cmds.deleteUI (ws)
        
    ws = cmds.workspaceControl("Custom Tools", initialHeight = 500, initialWidth = 200, retain = False, uiScript = "myToolbox.Create()", floating = True)

CreateWorkspace()

