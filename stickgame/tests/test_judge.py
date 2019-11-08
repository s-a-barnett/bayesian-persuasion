import pytest
from pytest import approx
from stickgame.judge import Judge

@pytest.fixture(params=[3,5])
def Jdge(request):
    return Judge(request.param)

class TestJudge:
    def test_initialise(self, Jdge):
        assert isinstance(Jdge.numsticks, int)
        assert Jdge.sumlengths == approx(0.0)
