import xml.etree.ElementTree as ET
from xmltag import XMLTag
import math


def convertToKDT(filename, name):
    try:
        tree = ET.parse(filename)
    except:
        return ""
    root = tree.getroot()
    if root.tag != 'program':
        return ""
    drills = []
    instr = {}
    length = int(root.attrib['dx'])
    width = int(root.attrib['dy'])
    thick = int(root.attrib['dz'])
    KDTPanelFormat = XMLTag(name='KDTPanelFormat')
    Panel = XMLTag(name="PANEL")
    PanelLength = XMLTag(name="PanelLength").addChild(XMLTag(plain_text=length))
    PanelWidth = XMLTag(name="PanelWidth").addChild(XMLTag(plain_text=width))
    PanelThickness = XMLTag(name="PanelThickness").addChild(XMLTag(plain_text=thick))
    PanelName = XMLTag(name="PanelName").addChild(XMLTag(plain_text=name))
    Panel.addChild(PanelLength, PanelWidth, PanelThickness, PanelName)
    KDTPanelFormat.addChild(Panel)
    tools = root.findall('tool')

    def getToolDiam(name):
        for t in tools:
            if t.attrib['name'] == name:
                return t.attrib['d']
    elIndex = -1
    cad = None
    vertexes = None
    defaultToolName = ""
    for el in root:
        elIndex += 1
        match el.tag:
            case 'ms':
                (cad, defaultToolName) = getPathCAD(el, getToolDiam, defaultToolName)
                vertexes = XMLTag(name='Vertexes')
                point = XMLTag(name='Point')
                x1 = XMLTag(name='X1').addChild(XMLTag(plain_text=el.attrib['x']))
                y1 = XMLTag(name='Y1').addChild(XMLTag(plain_text=el.attrib['y']))
                point.addChild(x1, y1)
                vertexes.addChild(point)
            case 'mac':
                arc = XMLTag(name='Arc')
                x = float(el.attrib['x'])
                y = float(el.attrib['y'])
                cx = float(el.attrib['cx'])
                cy = float(el.attrib['cy'])
                x1 = XMLTag(name='X1').addChild(XMLTag(plain_text=el.attrib['x']))
                y1 = XMLTag(name='Y1').addChild(XMLTag(plain_text=el.attrib['y']))
                radius = XMLTag(name='Radius').addChild(XMLTag(plain_text=math.sqrt((x-cx)**2 + (y-cy)**2)))
                direction = XMLTag(name='Direction').addChild(XMLTag(plain_text=0 if el.attrib['dir'] == 'true' else 1))
                arc.addChild(x1, y1, radius, direction)
                vertexes.addChild(arc)
                if root[elIndex+1].tag != 'mac':
                    cad.addChild(vertexes)
                    KDTPanelFormat.addChild(cad)
            case 'bf':
                KDTPanelFormat.addChild(getBFCAD(el, getToolDiam))
            case 'br':
                KDTPanelFormat.addChild(getBXCAD(el, length, width, getToolDiam))
            case 'bl':
                KDTPanelFormat.addChild(getBXCAD(el, length, width, getToolDiam))
            case 'bb':
                KDTPanelFormat.addChild(getBXCAD(el, length, width, getToolDiam))
            case 'bt':
                KDTPanelFormat.addChild(getBXCAD(el, length, width, getToolDiam))
    
    s = '<?xml version="1.0" encoding="UTF-8"?>'
    s = s + str(KDTPanelFormat)
    return s


def getPathCAD(el, getToolDiam, defaultToolName):
    cad = XMLTag(name='CAD')
    typeNo = XMLTag(name='TypeNo').addChild(XMLTag(plain_text='7'))
    typeName = XMLTag(name='TypeName').addChild(XMLTag(plain_text='Path'))
    toolName = el.attrib.get('name') or defaultToolName
    width = XMLTag(name='Width').addChild(XMLTag(plain_text=getToolDiam(toolName)))
    correction = XMLTag(name='Correction').addChild(XMLTag(plain_text=el.attrib['c']))
    depth = XMLTag(name='Depth').addChild(XMLTag(plain_text=el.attrib['dp']))
    cad.addChild(typeNo, typeName, width, correction, depth)
    return (cad, toolName)


def getBFCAD(el, getToolDiam):
    cad = XMLTag(name='CAD')
    typeNo = XMLTag(name='TypeNo').addChild(XMLTag(plain_text='1'))
    typeName = XMLTag(name='TypeName').addChild(XMLTag(plain_text='Vertical Hole'))
    planeId = XMLTag(name='PlaneID').addChild(XMLTag(plain_text='0'))
    quadrant = XMLTag(name='Quadrant').addChild(XMLTag(plain_text='1'))
    x1 = XMLTag(name='X1').addChild(XMLTag(plain_text=el.attrib['x']))
    y1 = XMLTag(name='Y1').addChild(XMLTag(plain_text=el.attrib['y']))
    depth = XMLTag(name='Depth').addChild(XMLTag(plain_text=el.attrib['dp']))
    diameter = XMLTag(name='Diameter').addChild(XMLTag(plain_text=getToolDiam(el.attrib['name'])))
    holeNo = XMLTag(name='HoleNo').addChild(XMLTag(plain_text='1'))
    intervalX = XMLTag(name='IntervalX').addChild(XMLTag(plain_text='0'))
    intervalY = XMLTag(name='IntervalY').addChild(XMLTag(plain_text='0'))
    intervalZ = XMLTag(name='IntervalZ').addChild(XMLTag(plain_text='0'))
    mirror = XMLTag(name='Mirror').addChild(XMLTag(plain_text='0'))
    cad.addChild(typeNo, typeName, planeId, quadrant, x1, y1, depth,
                 diameter, holeNo, intervalX, intervalY, intervalZ, mirror)
    return cad


def getBXCAD(el, length, width, getToolDiam):
    cad = XMLTag(name='CAD')
    typeNo = XMLTag(name='TypeNo').addChild(XMLTag( plain_text='2'))
    typeName = XMLTag(name='TypeName').addChild(XMLTag(plain_text='Horizontal Hole'))
    planeId = XMLTag(name='PlaneID').addChild(XMLTag(plain_text='2'))
    quad = 1
    x = 0
    y = 0
    match el.tag:
        case "br":
            quad = 1
            x = length
            y = el.attrib['y']
        case "bl":
            quad = 2
            x = 0
            y = el.attrib['y']
        case "bb":
            quad = 3
            y = width
            x = el.attrib['x']
        case "bt":
            quad = 4
            y = 0
            x = el.attrib['x']
    quadrant = XMLTag(name='Quadrant').addChild(XMLTag(plain_text=quad))
    x1 = XMLTag(name='X1').addChild(XMLTag(plain_text=x))
    y1 = XMLTag(name='Y1').addChild(XMLTag(plain_text=y))
    z1 = XMLTag(name='Y1').addChild(XMLTag(lain_text=el.attrib['z']))
    depth = XMLTag(name='Depth').addChild(XMLTag(plain_text=el.attrib['dp']))
    diameter = XMLTag(name='Diameter').addChild(XMLTag(plain_text=getToolDiam(el.attrib['name'])))
    holeNo = XMLTag(name='HoleNo').addChild(XMLTag(plain_text='1'))
    intervalX = XMLTag(name='IntervalX').addChild(XMLTag(plain_text='0'))
    intervalY = XMLTag(name='IntervalY').addChild(XMLTag(plain_text='0'))
    intervalZ = XMLTag(name='IntervalZ').addChild(XMLTag(plain_text='0'))
    mirror = XMLTag(name='Mirror').addChild(XMLTag(plain_text='0'))
    cad.addChild(typeNo, typeName, planeId, quadrant, x1, y1,z1, depth,
                 diameter, holeNo, intervalX, intervalY, intervalZ, mirror)
    return cad
