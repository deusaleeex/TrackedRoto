import nuke
import os

def link_roto(tracker_node):
    
    # Create Roto node
    i = nuke.createNode("Roto")
    i.setInput(0, None)
    i.setXYpos(tracker_node.xpos() + 50, tracker_node.ypos() + 50) 

    link_method = tracker_node['which'].value()
    
    # Link values if bool == true
    tran = tracker_node['t'].value()
    rot = tracker_node['r'].value()
    sca = tracker_node['s'].value()
    cen = tran or rot or sca

    # Checks if the link_method is live-linked or baked
    if link_method == 'live-link':
        if tran:
            i['translate'].setExpression(tracker_node.name() + ".translate")
        if rot:
            i['rotate'].setExpression(tracker_node.name() + ".rotate")
        if sca:
            i['scale'].setExpression(tracker_node.name() + ".scale")
        if cen:
            i['center'].setExpression(tracker_node.name() + ".center")
            
    elif link_method == 'baked':
        i['translate'].fromScript(tracker_node['translate'].toScript())
        i['rotate'].fromScript(tracker_node['rotate'].toScript())
        i['scale'].fromScript(tracker_node['scale'].toScript())
        i['center'].fromScript(tracker_node['center'].toScript())
        i['label'].setValue("Baked: " + tracker_node.name())

def create_knobs():
    tracker_node = nuke.thisNode()

    tab = nuke.Tab_Knob('Create Roto')
    tracker_node.addKnob(tab)
    
    dat = nuke.Text_Knob("<b>Data")
    dat.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(dat)

    tran = nuke.Boolean_Knob('t', 'translate',)
    tran.setValue(True)
    tran.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(tran)

    rot = nuke.Boolean_Knob('r', 'rotation')
    rot.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(rot)

    sca = nuke.Boolean_Knob('s', 'scale')
    sca.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(sca)
    
    ref_frame = tracker_node['reference_frame']
    tracker_node.addKnob(ref_frame)
    
    set_frame = nuke.PyScript_Knob('set_ref', 'set to current frame', 'nuke.thisNode()["reference_frame"].setValue(nuke.frame())')
    set_frame.clearFlag(nuke.STARTLINE)
    tracker_node.addKnob(set_frame)
    
    expo = nuke.Text_Knob("<b>Export")
    expo.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(expo)
    
    which = nuke.Enumeration_Knob('which', 'link method', ['live-link', 'baked'])
    which.setFlag(nuke.STARTLINE)
    tracker_node.addKnob(which)
    
    cr = nuke.PyScript_Knob('create_roto', 'create', 'link_roto(nuke.thisNode())')
    tracker_node.addKnob(cr)


# Add callback
nuke.addOnUserCreate(create_knobs, nodeClass="Tracker4")
