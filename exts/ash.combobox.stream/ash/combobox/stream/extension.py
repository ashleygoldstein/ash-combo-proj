import omni.ext
import omni.ui as ui
import omni.kit.commands
from .window import SelectionWindow
from pxr import Usd

# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[ash.combobox.stream] some_public_function was called with x: ", x)
    return x ** x




# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class AshComboboxStreamExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[ash.combobox.stream] ash combobox stream startup")

        self._stage = omni.usd.get_context().get_stage()

        self._window = SelectionWindow("ComboBox Model Stream", width=300, height=300)

        #Create materials prims
        blue_mtl = Usd.Prim = self._stage.GetPrimAtPath("/World/Looks/OmniPBR_Blue")
        red_mtl = Usd.Prim = self._stage.GetPrimAtPath("/World/Looks/OmniPBR_Red")

        def check_prim_exists(prim: Usd.Prim) -> bool:
            if prim.IsValid():
                return True
            return False
        
        if check_prim_exists(blue_mtl) and check_prim_exists(red_mtl)== True:
            print("Materials already exist")
        else:
        #Load Blue and Red Materials
            omni.kit.commands.execute('CreateMdlMaterialPrim',
                mtl_url='OmniPBR.mdl',
                mtl_name='OmniPBR',
                mtl_path='/World/Looks/OmniPBR_Blue',
                select_new_prim=True)
            omni.kit.commands.execute('CreateMdlMaterialPrim',
                mtl_url='OmniPBR.mdl',
                mtl_name='OmniPBR',
                mtl_path='/World/Looks/OmniPBR_Red',
                select_new_prim=True)


    def on_shutdown(self):
        print("[ash.combobox.stream] ash combobox stream shutdown")
