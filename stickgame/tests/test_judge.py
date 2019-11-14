import pytest
from pytest import approx
import numpy as np
from stickgame.judge import FixedJudge

@pytest.fixture(params=[3,5])
def FJudge(request):
    return FixedJudge(request.param)

class TestFixedJudge:
    def test_initialise(self, FJudge):
        assert isinstance(FJudge.numsticks, int)
        assert FJudge.sumlengths == approx(0.0)

    def test_threshold(self, FJudge):
        assert FJudge.sumlengths + FJudge.threshold >= 0.5*FJudge.numsticks
        FJudge.agent1obs.append(np.random.rand())
        FJudge.agent2obs.append(np.random.rand())
        FJudge._recompute_sum_and_threshold()
        assert FJudge.sumlengths + FJudge.threshold >= 0.5*FJudge.numsticks

    def test_lower_upper(self, FJudge):
        FJudge.agent2obs.append(0.6)
        FJudge._compute_upper_and_lower()
        assert FJudge.upper == approx(0.6)
        FJudge.agent1obs.append(0.41)
        FJudge._compute_upper_and_lower()
        assert FJudge.lower == approx(0.41)

    def test_p_long_biased(self, FJudge):
        assert FJudge.compute_p_long() == approx(0.5)
        if FJudge.numsticks == 3:
            FJudge.agent2obs.append(0.6)
            assert FJudge.compute_p_long() == approx(0.125)
            FJudge.agent1obs.append(0.41)
            assert FJudge.compute_p_long() == approx(0.578947)

    def test_p_long_neutral(self, FJudge):
        FJudge.agent1bias = 'n'
        FJudge.agent2bias = 'n'
        if FJudge.numsticks == 3:
            FJudge.agent2obs.append(0.6)
            assert FJudge.compute_p_long() == approx(0.595)
            FJudge.agent1obs.append(0.41)
            assert FJudge.compute_p_long() == approx(0.51)
