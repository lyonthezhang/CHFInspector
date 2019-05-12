import yaml
import xml.etree.ElementTree as ET

fsmListFromVars = []

yml = None
with open("emergency.yml", 'r') as stream:
    try:
        yml = yaml.safe_load(stream)

    except yaml.YAMLError as exc:
        print(exc)
        exit()

#system wrapper
xml = ET.Element('system')
xml.set("label", "5G")

VARS = ET.SubElement(xml, 'VARS')

for (var, properties) in yml["VARS"].items():
    thisVar = ET.Element('VAR')
    thisVar.set('label', var)
    for (label, value) in properties.items():
        if label == "fsm":
            if label not in fsmListFromVars:
                fsmListFromVars.append(value)
            thisProperty = ET.Element(label)
            thisProperty.text = value
            ET.Element(thisProperty)
            thisVar.append(thisProperty)
        elif label == "type":
            if value == "env_bool":
                x = ET.SubElement(thisVar, "datatype")
                x.text = "boolean"
                x = ET.SubElement(thisVar, "controltype")
                x.text = "environment"
            elif value == "state_bool":
                x = ET.SubElement(thisVar, "datatype")
                x.text = "boolean"
                x = ET.SubElement(thisVar, "controltype")
                x.text = "state"
    VARS.append(thisVar)

FSMS = ET.SubElement(xml, 'FSMs')
for (fsm, properties) in yml["FSMS"].items():
    transitionIter = 1
    thisFSM = ET.SubElement(FSMS, 'FSM')
    thisFSM.set('label', fsm)
    for (label, value) in properties.items():
        if label == "states":
            states = ET.SubElement(thisFSM, 'states')
            for state in value:
                x = ET.SubElement(states, 'state')
                x.text = state
        elif label == 'init_state':
            init_state = ET.SubElement(thisFSM, 'init_state')
            init_state.text = value
        elif label == 'transitions':
            transitions = ET.SubElement(thisFSM, 'transitions')
            for (condition, transParams) in value.items():
                transition = ET.SubElement(transitions, 'transition')
                transName = thisFSM.get('label').lower() + '_T' + str(transitionIter)
                transitionIter += 1
                transition.set('label', transName)
                actions = None #preserve LTE inspector original ordering this way
                for (transParam, paramValue) in transParams.items():
                    if transParam == "start" or transParam == "end":
                        x = ET.SubElement(transition, transParam)
                        x.text = paramValue
                        if transParam == "end":
                            y = ET.SubElement(transition, 'condition')
                            y.text = condition
                    else:
                        if not actions: actions = ET.SubElement(transition, 'actions')
                        for i, event in enumerate(paramValue):
                            action = ET.SubElement(actions, 'action')
                            channel = ET.SubElement(action, 'channel')
                            start = ET.SubElement(channel, 'start')
                            end = ET.SubElement(channel, 'end')
                            if transParam == 'set':
                                action.set('label', event)
                                start.text = 'NULL'
                                end.text = 'NULL'
                                channel.set('label', 'internal')
                            elif transParam == 'send':
                                action.set('label', list(event.keys())[0])
                                channel.set('label', list(event.values())[0]['using'])
                                start.text = yml['CHANNELS'][channel.get('label')]['tx']
                                end.text = yml['CHANNELS'][channel.get('label')]['rx']

                action = ET.SubElement(actions, 'action')
                action.set('label', 'null_action')
                channel = ET.SubElement(action, 'channel')
                channel.set('label', "NULL")
                ET.SubElement(channel, 'start').text = "NULL"
                ET.SubElement(channel, 'end').text = "NULL"
CHANNELS = ET.SubElement(xml, 'channels')
for (channelName, fields) in yml['CHANNELS'].items():
    channel = ET.SubElement(CHANNELS, 'channel')
    channel.set('label', channelName)
    ET.SubElement(channel, 'start').text = fields['tx']
    ET.SubElement(channel, 'end').text = fields['rx']
    ET.SubElement(channel, 'noisy').text = "FALSE"







tree = ET.ElementTree(xml)
tree.write(open('emergency.xml', 'wb'))
