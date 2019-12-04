import pytest
from pytest import approx
from stickgame.irwinhall import IrwinHall

@pytest.fixture(params=[1,2,3])
def IH(request):
    return IrwinHall(request.param)

class TestIrwinHall:
    def test_initialise(self, IH):
        assert isinstance(IH.numvars, int)
        assert isinstance(IH.lower, float)
        assert isinstance(IH.upper, float)

    def test_cdf_output(self, IH):
        assert isinstance(IH.cdf(0.0), float)

    def test_cdf_vals(self, IH):
        # Test out-of-range values
        assert IH.cdf(IH.numvars*IH.lower - 1.0) == approx(0.0)
        assert IH.cdf(IH.numvars*IH.upper + 1.0)  == approx(1.0)
        # Test the median value
        assert IH.cdf(IH.numvars / 2) == approx(0.5)
