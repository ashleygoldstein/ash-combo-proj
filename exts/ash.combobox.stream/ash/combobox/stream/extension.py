import omni.ext
import omni.ui as ui
import omni.kit.commands

# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[ash.combobox.stream] some_public_function was called with x: ", x)
    return x ** x


PRIMS = ["frog", "gas stove", "chair"]

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class AshComboboxStreamExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[ash.combobox.stream] ash combobox stream startup")

            
        self._stage = omni.usd.get_context().get_stage()
        self._combobox = None
            

        self._window = ui.Window("ComboBox LWM Stream", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                self._comboBox = ui.ComboBox(0,*PRIMS).model
            
                def combo_changed(item_model, item):
                    value_model = item_model.get_item_value_model(item)
                    self.current_selection = PRIMS[value_model.as_int]
                    #The bottom two lines are WIP, we will connect these to our combo box next stream
                    # self.current_index = value_model.as_int
                    #self._combo_changed_sub = self.combo_model.subscribe_item_changed_fn(combo_changed)                    
                        
                #Temp function to subscribe to item, we will replace this with our Prims later
                def get_prim():
                    omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                            prim_type='Cube',
                            prim_path=None,
                            select_new_prim=True,
                            prepend_default_prim=True)
                        
                    omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                        prim_type='Cylinder',
                        prim_path=None,
                        select_new_prim=True,
                        prepend_default_prim=True)
                    

                    omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                        prim_type='Sphere',
                        prim_path=None,
                        select_new_prim=True,
                        prepend_default_prim=True)



                def make_blue():
                    pass

                def make_red():
                    pass

                

                with ui.HStack():
                    ui.Button("Make Blue", clicked_fn=get_prim)
                    ui.Button("Make Red", clicked_fn=make_red)

    def on_shutdown(self):
        print("[ash.combobox.stream] ash combobox stream shutdown")
