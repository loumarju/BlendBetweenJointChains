import maya.cmds as cmds

#Definimos un controlador
controller = "Page_01_loc"

# Seleccionar y obtener las cadenas de huesos en la escena y almacenarlas en una lista.
cmds.select("Page_01_Skin_jnt_01", hierarchy=True)
skin = cmds.ls(selection=True)

cmds.select("L_BlockPage_jnt_01", hierarchy=True)
left = cmds.ls(selection=True)

cmds.select("Mid_jnt_01", hierarchy=True)
middle = cmds.ls(selection=True)

cmds.select("R_BlockPage_jnt_01", hierarchy=True)
right = cmds.ls(selection=True)

# Función para configurar la página con las cuatro variables arriba definidas
#Si el locator no tiene el atributo Page, se le añade.

def pagesetup(controller, left, middle, right, skin):
    if not cmds.attributeQuery("page", node=controller, exists=True):
        cmds.addAttr(controller, longName="page", attributeType="double", min=-10, max=10, defaultValue=0)
        cmds.setAttr(f"{controller}.page", edit=True, keyable=True)

 #Para cada joint en la lista de skin, se crean 6 nodos "blendweighted" con nombres basados en en nombre del joint y
##las letras 'rx', 'ry', 'rz', 'tx', 'ty', 'tz'   
##Estos nodos se utilizan para mezclar diferentes transformaciones basadas en los pesos asignados.

    for i in range(len(skin)):
        rx = cmds.createNode("blendWeighted", name=f"{skin[i]}_rx")
        ry = cmds.createNode("blendWeighted", name=f"{skin[i]}_ry")
        rz = cmds.createNode("blendWeighted", name=f"{skin[i]}_rz")
        tx = cmds.createNode("blendWeighted", name=f"{skin[i]}_tx")
        ty = cmds.createNode("blendWeighted", name=f"{skin[i]}_ty")
        tz = cmds.createNode("blendWeighted", name=f"{skin[i]}_tz")
        
        # Inicializar pesos y entradas de blendWeighted a 0
        for attr in [rx, ry, rz, tx, ty, tz]:
            for index in range(3):
                cmds.setAttr(f"{attr}.weight[{index}]", 0)
                cmds.setAttr(f"{attr}.input[{index}]", 0)
        
        # Conectar joints de objetivo a blendWeighted
        cmds.connectAttr(f"{left[i]}.rx", f"{rx}.input[0]")
        cmds.connectAttr(f"{left[i]}.ry", f"{ry}.input[0]")
        cmds.connectAttr(f"{left[i]}.rz", f"{rz}.input[0]")
        cmds.connectAttr(f"{middle[i]}.rx", f"{rx}.input[1]")
        cmds.connectAttr(f"{middle[i]}.ry", f"{ry}.input[1]")
        cmds.connectAttr(f"{middle[i]}.rz", f"{rz}.input[1]")
        cmds.connectAttr(f"{right[i]}.rx", f"{rx}.input[2]")
        cmds.connectAttr(f"{right[i]}.ry", f"{ry}.input[2]")
        cmds.connectAttr(f"{right[i]}.rz", f"{rz}.input[2]")

        cmds.connectAttr(f"{left[i]}.tx", f"{tx}.input[0]")
        cmds.connectAttr(f"{left[i]}.ty", f"{ty}.input[0]")
        cmds.connectAttr(f"{left[i]}.tz", f"{tz}.input[0]")
        cmds.connectAttr(f"{middle[i]}.tx", f"{tx}.input[1]")
        cmds.connectAttr(f"{middle[i]}.ty", f"{ty}.input[1]")
        cmds.connectAttr(f"{middle[i]}.tz", f"{tz}.input[1]")
        cmds.connectAttr(f"{right[i]}.tx", f"{tx}.input[2]")
        cmds.connectAttr(f"{right[i]}.ty", f"{ty}.input[2]")
        cmds.connectAttr(f"{right[i]}.tz", f"{tz}.input[2]")

        # Conectar blendWeighted a sus respectivas conexiones
        cmds.connectAttr(f"{rx}.output", f"{skin[i]}.rx")
        cmds.connectAttr(f"{ry}.output", f"{skin[i]}.ry")
        cmds.connectAttr(f"{rz}.output", f"{skin[i]}.rz")
        cmds.connectAttr(f"{tx}.output", f"{skin[i]}.tx")
        cmds.connectAttr(f"{ty}.output", f"{skin[i]}.ty")
        cmds.connectAttr(f"{tz}.output", f"{skin[i]}.tz")

        # Configurar las claves de conducción en blendWeighted
        set_driven_keys(controller, rx, ry, rz, tx, ty, tz)

def set_driven_keys(controller, rx, ry, rz, tx, ty, tz):
    # Definir los valores para las claves de conducción
    driven_values = [
        (-10, 1, 0, 0),
        (0, 0, 1, 0),
        (10, 0, 0, 1)
    ]
    
    # Atributos de rotación
    for dv, rx_w0, rx_w1, rx_w2 in driven_values:
        cmds.setDrivenKeyframe(f"{rx}.weight[0]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w0, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{ry}.weight[0]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w0, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{rz}.weight[0]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w0, inTangentType="flat", outTangentType="flat")
        
        cmds.setDrivenKeyframe(f"{rx}.weight[1]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w1, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{ry}.weight[1]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w1, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{rz}.weight[1]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w1, inTangentType="flat", outTangentType="flat")
        
        cmds.setDrivenKeyframe(f"{rx}.weight[2]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w2, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{ry}.weight[2]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w2, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{rz}.weight[2]", currentDriver=f"{controller}.page", driverValue=dv, value=rx_w2, inTangentType="flat", outTangentType="flat")
    
    # Atributos de traslación
    for dv, tx_w0, tx_w1, tx_w2 in driven_values:
        cmds.setDrivenKeyframe(f"{tx}.weight[0]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w0, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{ty}.weight[0]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w0, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{tz}.weight[0]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w0, inTangentType="flat", outTangentType="flat")
        
        cmds.setDrivenKeyframe(f"{tx}.weight[1]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w1, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{ty}.weight[1]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w1, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{tz}.weight[1]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w1, inTangentType="flat", outTangentType="flat")
        
        cmds.setDrivenKeyframe(f"{tx}.weight[2]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w2, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{ty}.weight[2]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w2, inTangentType="flat", outTangentType="flat")
        cmds.setDrivenKeyframe(f"{tz}.weight[2]", currentDriver=f"{controller}.page", driverValue=dv, value=tx_w2, inTangentType="flat", outTangentType="flat")

# Llamar a la función pagesetup con los parámetros adecuados
pagesetup(controller, left, middle, right, skin)
