from .personaje_repo import PersonajeRepo
from .arma_repo      import ArmaRepo
from .runa_repo      import RunaRepo
from .inventario_repo import InventarioRepo
from .recursos_repo  import RecursosRepo
from .pity_repo      import PityRepo

personaje_repo  = PersonajeRepo()
arma_repo       = ArmaRepo()
runa_repo       = RunaRepo()
inventario_repo = InventarioRepo()
recursos_repo   = RecursosRepo()
pity_repo       = PityRepo()