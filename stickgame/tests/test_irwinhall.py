import pytest
from stickgame.irwinhall import IrwinHall

@pytest.fixture(params=[1,2,3])
def IH(request):
    return IrwinHall(request.param)

class TestIrwinHall:
    def test_initialise(self, IH):
        assert isinstance(IH.numvars, int)
