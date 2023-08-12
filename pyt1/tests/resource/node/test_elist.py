from ....epure.resource.node.elist import Elist
import pytest
from ....epure.epure import epure
from typing import List

# @pytest.fixture
def elist1():

    # @epure()
    class EpureClsElist:
        elist:Elist[str] = Elist[str](['abc','defg',"the","brown","fox","jumps","over","lazy","dog"])

    return EpureClsElist()

def test_elist():
    elist = elist1().elist.save()
    pass