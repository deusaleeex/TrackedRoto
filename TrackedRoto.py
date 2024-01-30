import nuke

def link_roto(tracker_node):
    # Create Roto node
    i = nuke.createNode("Roto")
    i.setInput(0, None)

    # Link values if bool == true
    tran = tracker_node['t'].value()
    rot = tracker_node['r'].value()
    sca = tracker_node['s'].value()

    if tran:
        i['translate'].setExpression("parent." + tracker_node.name() + ".translate")
    if rot:
        i['rotate'].setExpression("parent." + tracker_node.name() + ".rotate")
    if sca:
        i['scale'].setExpression("parent." + tracker_node.name() + ".scale")

def create_knobs():
    tracker_node = nuke.thisNode()

    tab = nuke.Tab_Knob('Create Roto')
    tracker_node.addKnob(tab)

    tran = nuke.Boolean_Knob('t', 'Translate')
    tran.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(tran)

    rot = nuke.Boolean_Knob('r', 'Rotation')
    rot.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(rot)

    sca = nuke.Boolean_Knob('s', 'Scale')
    sca.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(sca)
   
    cr = nuke.PyScript_Knob('cr', 'Create Linked Roto', 'TrackedRoto.link_roto(nuke.thisNode())')
    cr.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(cr)

# Add callback
nuke.addOnUserCreate(create_knobs, nodeClass="Tracker4")