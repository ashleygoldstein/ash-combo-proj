import omni.usd
import omni.ui as ui
from pxr import Usd

PRIMS = ("Frog", "Stove", "Chair")

class SelectionWindow(ui.Window):

    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs)

        self.frame.set_build_fn(self._build_fn)
        self._stage = omni.usd.get_context().get_stage()
        self.option = None

        #Define prims for assets
        self.frog_prim = Usd.Prim = self._stage.GetPrimAtPath("/World/Frog_Soft_Toy")
        self.stove_prim = Usd.Prim = self._stage.GetPrimAtPath("/World/Gas_Stove")
        self.chair_prim = Usd.Prim = self._stage.GetPrimAtPath("/World/_66_ArmChair")

    def _build_window(self):
        with self.frame:
            with ui.VStack():
                with ui.CollapsableFrame("Selection"):
                    with ui.VStack():
                        with ui.HStack():
                            ui.Label("Select Prim:", width=50)
                            combo_model: ui.AbstractItemModel = ui.ComboBox(0, *PRIMS).model

                        def combo_selection_changed(item_model: ui.AbstractItemModel, item:ui.AbstractItem):
                            value_model = item_model.get_item_value_model(item)
                            current_index = value_model.as_int

                            self.option = PRIMS[current_index]

                        def check_prim_exists(prim: Usd.Prim) -> bool:
                            if prim.IsValid():
                                return True
                            return False
                        
                        if self.option == "Frog":
                            if check_prim_exists(self.frog_prim) == True:
                                print("Frog already exists")
                                self.select_prim = self.frog_prim

                            print(f"Selected: {self.option}")

                        self._combobox_sub = combo_model.subscribe_item_changed_fn(combo_selection_changed)
                            


    def _build_fn(self):
        with ui.ScrollingFrame():
            with ui.VStack(height=10):
                self._build_window()