from typing import List
import omni.ui as ui
import omni.kit.commands
import omni.usd
from pxr import Usd, Sdf, Gf, UsdGeom
import logging


#Create at step 8 - tuple to store combobox options
PRIMS = ("Frog", "Stove", "Chair")

#Step 1: Create a window class
class SelectionWindow(ui.Window):

#Step 2: create init function to store variables
    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs) 

#Step 3: Store frame build fn and stage
#then Create build fn callback below
        self.frame.set_build_fn(self._build_fn)
        self._stage = omni.usd.get_context().get_stage()

        self._combobox_sub = None
        self._current_prim = None
        self.select_prim = None
        self.option = None
        

        #Step 15: Create variables for prims 
        self.frog_prim: Usd.Prim = self._stage.GetPrimAtPath("/World/Frog_Soft_Toy")
        self.stove_prim: Usd.Prim = self._stage.GetPrimAtPath("/World/Gas_Stove")
        self.chair_prim: Usd.Prim = self._stage.GetPrimAtPath("/World/_66_Armchair")

#Step 4: create build window fn for frame 
    def _build_window(self):
        with self.frame:
            #Step 5: Create a Vstack and Frame for the window
            with ui.VStack():
                with ui.CollapsableFrame("Selection"):
                    #Step 6: Create a Vstack and Hstack for the frame to nest labels and combobox
                    with ui.VStack(height=20, spacing=4):
                            
                        with ui.HStack():
                            #Step 7: Create a label for your combobox and create combomodel using AbstractItemModel
                            ui.Label("TEST", width=50)
                            #Step 8: when creating ui.combobox, create PRIMS tuple
                            combo_model: ui.AbstractItemModel= ui.ComboBox(0,*PRIMS).model

                        #Step 16 part 2: create check prim exists    
                        def check_prim_exists(prim: Usd.Prim) -> bool:
                            if prim.IsValid():
                                return True
                            return False
                        
                        #Step 11: create combo_selection_changed function to store combobox selection - got from 
                        #mati's developer office hours
                        def combo_selection_changed(item_model: ui.AbstractItemModel, item: ui.AbstractItem):
                            value_model = item_model.get_item_value_model(item)
                            current_index = value_model.as_int
                            #step 12: when making option variable, store in init
                            self.option = PRIMS[current_index]
                            
                            #Step 16: create if statements for each prim
                            if self.option == "Frog":
                                if check_prim_exists(self.frog_prim) == True:
                                    self.select_prim = self.frog_prim
                                    
                                    print(f"{self.select_prim} selected")
                                else:
                                    logging.error(f"{self.select_prim} does not exist")


                            if self.option == "Stove": 
                                if check_prim_exists(self.stove_prim) == True:
                                    self.select_prim = self.stove_prim
                                    
                                    print(f"{self.select_prim} selected")
                                else:
                                    logging.error(f"{self.select_prim} does not exist")


                            if self.option == "Chair": 
                                if check_prim_exists(self.chair_prim) == True:
                                    self.select_prim = self.chair_prim
                                    print(f"{self.select_prim} selected")
                                else:
                                    logging.error(f"{self.select_prim} does not exist")

                            

                            #Step 13
                            #print(f"Selected '{option}' at index {current_index}.")

                        #Step 14: create subscription for combobox - store in init
                        self._combobox_sub = combo_model.subscribe_item_changed_fn(combo_selection_changed)
                        

                        #Step 10: create methods for buttons blue and red - print button clicked
                        def make_blue():
                            #Step 17: change button to show select prim selected
                            print(f"Button Clicked! {self.select_prim} selected")

                            #Step 18: Define material path for corresponding material
                            material_path = '/World/Looks/OmniPBR_Blue'

                            #Step 19: execute change property command to change diffuse color
                            omni.kit.commands.execute(
                                        "ChangeProperty",
                                        prop_path=material_path + "/Shader.inputs:diffuse_color_constant",
                                        value = (0, 0, 1),
                                        prev = (0.2, 0.2, 0.2)
                                    ) 
                            
                            #Step 20: Bind material to prim
                            result = omni.kit.commands.execute('BindMaterialCommand',
                            prim_path=self.select_prim.GetPrimPath(),
                            material_path=str(material_path),
                            strength='strongerThanDescendants')                       



                        #Step 21: Do the same from blue button
                        def make_red():
                            material_path = '/World/Looks/OmniPBR_Red'

                            omni.kit.commands.execute(
                                        "ChangeProperty",
                                        prop_path=material_path + "/Shader.inputs:diffuse_color_constant",
                                        value = (1, 0, 0),
                                        prev = (0.2, 0.2, 0.2)
                                    ) 
                            
                            result = omni.kit.commands.execute('BindMaterialCommand',
                            prim_path=self.select_prim.GetPrimPath(),
                            material_path=str(material_path),
                            strength='strongerThanDescendants')      


                #Step 9: Create a new frame and Vstack to store buttons. Make 2 buttons
                with ui.CanvasFrame():
                    with ui.VStack():
                        with ui.HStack():
                            ui.Button("Make Blue", clicked_fn=make_blue)
                            ui.Button("Make Red", clicked_fn=make_red)

#From step 3: Create build fn callback to build window
    def _build_fn(self):
        with ui.ScrollingFrame():
            with ui.VStack(height=10):
                self._build_window()

    #def destroy(self):
    #    self._combobox_changed_sub = None
    #    return super().destroy()
