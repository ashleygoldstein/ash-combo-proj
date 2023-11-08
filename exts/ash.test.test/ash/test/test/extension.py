import omni.ext
import omni.ui as ui
import omni.kit.commands
from pxr import Usd

#import your window class from your window.py
from .window import SelectionWindow




# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[ash.test.test] some_public_function was called with x: ", x)
    return x ** x





class AshTestTestExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        self._stage = omni.usd.get_context().get_stage()
        #Step 1:Create a new window.py to build your window
        self._window = SelectionWindow("ComboBox Model Stream", width=300, height=300)

        #Step 3: create usd.prim for materials
        blue_material: Usd.Prim = self._stage.GetPrimAtPath("/World/Looks/OmniPBR_Blue")
        red_material: Usd.Prim = self._stage.GetPrimAtPath("/World/Looks/OmniPBR_Red")

        #Step 4: create check prim exists fn
        def check_prim_exists(prim: Usd.Prim) -> bool:
            if prim.IsValid():
                return True
            return False

        #Step 2: Create two new materials on start up, one for blue and one for red
        #after start up, click on materials in stage to initialize them
        ##add check prim if statement
        if check_prim_exists(blue_material) == True:
            pass
        else:
            success, result = omni.kit.commands.execute('CreateMdlMaterialPrimCommand',
                mtl_url='OmniPBR.mdl', # This can be path to local or remote MDL
                mtl_name='OmniPBR', # sourceAsset:subIdentifier (i.e. the name of the material within the MDL)
                mtl_path="/World/Looks/OmniPBR_Blue" # Prim path for the Material to create.
            )
            
        if check_prim_exists(red_material) == True:
            pass
        else:
            success, result = omni.kit.commands.execute('CreateMdlMaterialPrimCommand',
                mtl_url='OmniPBR.mdl', # This can be path to local or remote MDL
                mtl_name='OmniPBR', # sourceAsset:subIdentifier (i.e. the name of the material within the MDL)
                mtl_path="/World/Looks/OmniPBR_Red" # Prim path for the Material to create.
            )


    def on_shutdown(self):
        self._window.destroy()

        print("[ash.test.test] ash test test shutdown")
