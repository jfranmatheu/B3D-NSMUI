import bpy
import json

'''
class newsmui_read_json_data():
    def execute():
        with open('data.txt') as json_file:  
            data = json.load(json_file)
            for p in data['people']:
                print('Name: ' + p['name'])
                print('Website: ' + p['website'])
                print('From: ' + p['from'])
                print('')

        wgts = {}
    
        jsonFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),'widgets.json')
        if os.path.exists(jsonFile):
            f = open(jsonFile,'r')
            wgts = json.load(f)

        return (wgts)
'''

class NSMUI_OT_read_json_data(bpy.types.Operator):
    bl_idname = "nsmui.ot_read_json_data"
    bl_label = "Read .json Data"
    bl_description = "Read json file data."
    def execute(self, context):
        with open('Sculpt_Brushes/test_brush_set_001.json') as f:
            data = json.load(f)
        # Output:
        print(data)
