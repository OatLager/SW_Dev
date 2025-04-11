import xml.etree.ElementTree as ET

class MAVLink_message:
    def __init__(self, id, name, fields, description=""):
        self.id = id
        self.name = name
        self.fields = fields
        self.description = description

class MAVLink:
    def __init__(self, file):
        self.message_types = {}

    def load_messages(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for msg in root.findall('messages/message'):
            msg_id = int(msg.attrib['id'])
            name = msg.attrib['name']
            description = msg.find('description').text if msg.find('description') is not None else ""
            fields = []

            for field in msg.findall('field'):
                field_name = field.attrib['name']
                field_type = field.attrib['type']
                field_description = field.find('description').text if field.find('description') is not None else ""
                fields.append(MAVLink_field(field_name, field_type, field_description))

            self.message_types[name] = MAVLink_message(msg_id, name, fields, description)

class MAVLink_field:
    def __init__(self, name, type, description=""):
        self.name = name
        self.type = type
        self.description = description
