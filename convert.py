import xml.etree.ElementTree as ET
from xmltag import XMLTag

def convert(filename):
    try:
        tree = ET.parse(filename)
    except:
        return ""
    root = tree.getroot()
    if root.tag != 'KDTPanelFormat':
        return ""
    drills = []
    instr = {}
    length = round(float(root.find('./PANEL/PanelLength').text))
    width = round(float(root.find('./PANEL/PanelWidth').text))
    thick = round(float(root.find('./PANEL/PanelThickness').text))
    name = root.find('./PANEL/PanelName').text
    for cad in root.findall('CAD'):
        drill = {}
        drill['X1']=round(float(cad.find('X1').text))
        drill['Y1']=round(float(cad.find('Y1').text))
        
        drill['TypeName']=cad.find('TypeName').text
        drill['Depth']=round(float(cad.find('Depth').text))
        diam = round(float(cad.find('Diameter').text))
        instr[diam]=f'D{diam}'
        drill['Diameter']=diam
        drill['TypeName']=cad.find('TypeName').text
        if drill['TypeName'] == 'Horizontal Hole':
            drill['Z1']=round(float(cad.find('Z1').text))
            drill['Quad'] = cad.find('Quadrant').text
        drills.append(drill)

    program = XMLTag(name = 'program')
    program.addAttribute("dx",length)
    program.addAttribute("dy",width)
    program.addAttribute("dz",thick)
    for key in instr:
        tool = XMLTag(name='tool')
        tool.addAttribute('name', instr[key])
        tool.addAttribute("d",key)
        program.addChild(tool)
    for drill in drills:
        x = drill["X1"]
        y = drill["Y1"]
        bore = XMLTag(name = "")
        x = x if x >= 0 else 'dx' + str(x)
        bore.addAttribute("x", x)
        y = y if y >= 0 else 'dy' + str(y)
        bore.addAttribute("y", y)
        bore.addAttribute("dp",drill["Depth"])
        if drill['TypeName'] == 'Vertical Hole':
            n="bf"
            bore.addAttribute("av", 'false')
        else:
            n="br"
            match drill['Quad']:
                case "1":
                    n = "br"
                case "2":
                    n = "bl"
                case "3":
                    n = "bb"
                case "4":
                    n = "bt"
            bore.addAttribute("z", drill["Z1"])
            bore.addAttribute('ver', '2')
            bore.addAttribute("m", 'false')
        bore.setName(n)
        bore.addAttribute("ac", "1")
        bore.addAttribute("name",instr[drill['Diameter']])
        program.addChild(bore)

    s = '<?xml version="1.0" encoding="UTF-8"?>'
    s = s + str(program)
    return s
