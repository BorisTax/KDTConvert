class XMLTag():
    name: str
    attributes: dict
    children: list
    plain_text: str
    def __init__(self, **kwargs):
        self.name = kwargs.get('name') or ''
        self.attributes = dict()
        self.children = list()
        self.plain_text = str(kwargs.get('plain_text'))
        if self.plain_text == 'None': self.plain_text = ''
    def setName(self, name):
        self.name = name
    def addAttribute(self, key, value):
        self.attributes[key] = value
    def addChild(self, *child):
        for c in child: self.children.append(c)
        return self
    def addText(self, text):
        self.plain_text = str(text)
    def __str__(self):
        if self.plain_text != '': return self.plain_text
        attr = ""
        s = ""
        for key in self.attributes:
            attr = attr + f' {key}="{self.attributes[key]}"'
        s = f'<{self.name}{attr}'
        if len(self.children) == 0:
            s = f'{s}/>'
        else:
            s = s + ">"
            for c in self.children: 
                s = s + str(c)
            s = f'{s}</{self.name}>'
        return s
