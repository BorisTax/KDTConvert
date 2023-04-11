import xml.etree.ElementTree as ET
from xmltag import XMLTag

def convertToXNC(filename):
    try:
        tree = ET.parse(filename)
    except Exception as e:
        print(e)
        return ""
    root = tree.getroot()
    if root.tag != 'KDTPanelFormat':
        return ""
    drills = []
    paths = []
    instr = {}
    length = round(float(root.find('./PANEL/PanelLength').text))
    width = round(float(root.find('./PANEL/PanelWidth').text))
    thick = round(float(root.find('./PANEL/PanelThickness').text))
    name = root.find('./PANEL/PanelName').text
    for cad in root.findall('CAD'):
        match cad.find('TypeNo').text:
            case "7":#Path
                diam = round(float(cad.find('Width').text))
                instr[diam]=f'D{diam}'
                cor = round(float(cad.find('Correction').text))
                depth = round(float(cad.find('Depth').text))
                path = cad.find('Vertexes')
                for p in path:
                    node = XMLTag()
                    match p.tag:
                        case "Point":
                            x = float(p.find("X1").text)
                            y = float(p.find("Y1").text)
                            node.setName("ms")
                            node.addAttribute("x", x).addAttribute("y", y).addAttribute("dp", depth).addAttribute("c", cor).addAttribute("fwd", "true").addAttribute("name", f'D{diam}')
                        case "Line":
                            x = float(p.find("X1").text)
                            y = float(p.find("Y1").text)
                            node.setName("ml")
                            node.addAttribute("x", x).addAttribute("y", y).addAttribute("dp", depth)
                        case "Arc":
                            x = float(p.find("X1").text)
                            y = float(p.find("Y1").text)
                            radius =  float(p.find("Radius").text)
                            dir = int(p.find("Direction").text)
                            node.setName("ma")
                            node.addAttribute("x", x).addAttribute("y", y).addAttribute("dp", depth).addAttribute("r", radius).addAttribute("dir", "true" if dir==0 else "false")
                    paths.append(node)

            case "1", "2":
                drill = {}
                drill['X1']=round(float(cad.find('X1').text))
                drill['Y1']=round(float(cad.find('Y1').text))
                drill['TypeName']=cad.find('TypeName').text
                drill['Depth']=round(float(cad.find('Depth').text))
                diam = round(float(cad.find('Diameter').text))
                instr[diam]=f'D{diam}'
                drill['Diameter']=diam
                if drill['TypeName'] == 'Horizontal Hole':
                    drill['Z1']=round(float(cad.find('Z1').text))
                    drill['Quad'] = cad.find('Quadrant').text
                drills.append(drill)

    program = XMLTag(name = 'program')
    program.addAttribute("dx",length)
    program.addAttribute("dy",width)
    program.addAttribute("dz",thick)
    for key in instr:
        tool = XMLTag(name='tool').addAttribute('name', instr[key]).addAttribute("d",key)
        program.addChild(tool)
    for drill in drills:
        x = drill["X1"]
        y = drill["Y1"]
        bore = XMLTag(name = "")
        x = x if x >= 0 else 'dx' + str(x)
        bore.addAttribute("x", x)
        y = y if y >= 0 else 'dy' + str(y)
        bore.addAttribute("y", y).addAttribute("dp",drill["Depth"])
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
            bore.addAttribute("z", drill["Z1"]).addAttribute('ver', '2').addAttribute("m", 'false')
        bore.setName(n)
        bore.addAttribute("ac", "1").addAttribute("name",instr[drill['Diameter']])
        program.addChild(bore)
    for p in paths:
        program.addChild(p)
    s = '<?xml version="1.0" encoding="UTF-8"?>'
    s = s + str(program)
    return s
