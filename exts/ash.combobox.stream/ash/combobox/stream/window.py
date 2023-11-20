import omni.usd
import omni.ui as ui
from pxr import Usd
import carb

PRIMS = ("Frog", "Stove", "Chair")

class SelectionWindow(ui.Window):

    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs)

        self.frame.set_build_fn(self._build_fn)
        self._stage = omni.usd.get_context().get_stage()
        

        self._combobox_sub = None
        self._current_prim = None
        self.select_prim = None
        self.option = None

        #Define prims for assets
        self.frog_prim = Usd.Prim = self._stage.GetPrimAtPath("/World/Frog_Soft_Toy")
        self.stove_prim = Usd.Prim = self._stage.GetPrimAtPath("/World/Gas_Stove")
        self.chair_prim = Usd.Prim = self._stage.GetPrimAtPath("/World/_66_Armchair")

    def _build_window(self):
        with self.frame:
            with ui.VStack():
                with ui.CollapsableFrame("Selection"):
                    with ui.VStack(height=20, spacing=4):

                        with ui.HStack():
                            ui.Label("Select Prim:", width=50)
                            combo_model: ui.AbstractItemModel = ui.ComboBox(0, *PRIMS).model

                        def check_prim_exists(prim: Usd.Prim) -> bool:
                            if prim.IsValid():
                                return True
                            return False
                        
                        def combo_selection_changed(item_model: ui.AbstractItemModel, item:ui.AbstractItem):
                            value_model = item_model.get_item_value_model(item)
                            current_index = value_model.as_int

                            self.option = PRIMS[current_index]


                            #Fixed tabbing issue
                            if self.option == "Frog":
                                if check_prim_exists(self.frog_prim) == True:
                                    self.select_prim = self.frog_prim
                                    print(f"Selected: {self.select_prim}")
                                else:
                                    carb.log_error(f"Prim {self.select_prim} does not exist")

                                
                            if self.option == "Stove":
                                if check_prim_exists(self.stove_prim) == True:
                                    self.select_prim = self.stove_prim
                                    print(f"Selected: {self.select_prim}")
                                else:
                                    carb.log_error(f"Prim {self.select_prim} does not exist")

                            if self.option == "Chair":
                                if check_prim_exists(self.chair_prim) == True:
                                    self.select_prim = self.chair_prim
                                    print(f"Selected: {self.select_prim}")
                                else:
                                    carb.log_error(f"Prim {self.select_prim} does not exist")

                            
                    self._combobox_sub = combo_model.subscribe_item_changed_fn(combo_selection_changed)

                    #make blue
                    def make_blue():
                        print(f"Button Clicked! {self.select_prim} Selected")
                        material_path = "/World/Looks/OmniPBR_Blue"

                        omni.kit.commands.execute(
                            "ChangeProperty",
                            prop_path=material_path + "/Shader.inputs:diffuse_color_constant",
                            value = (0, 0, 1),
                            prev = (0.2, 0.2, 0.2)
                            ) 
                        result = omni.kit.commands.execute('BindMaterialCommand',
                        prim_path=self.select_prim.GetPrimPath(),
                        material_path=str(material_path),
                        strength='strongerThanDescendants')  
                        
                    #make red
                    def make_red():
                        print(f"Button Clicked! {self.select_prim} Selected")
                        material_path = "/World/Looks/OmniPBR_Red"

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


                    #new frame and vstack+hstack for buttons
                with ui.CanvasFrame():
                    with ui.VStack():
                        with ui.HStack():
                            ui.Button("Make Blue", clicked_fn=make_blue)
                            ui.Button("Make Red", clicked_fn=make_red)

    def _build_fn(self):
        with ui.ScrollingFrame():
            with ui.VStack(height=10):
                self._build_window()