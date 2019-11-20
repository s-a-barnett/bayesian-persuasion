import pytest
from pytest import approx
import numpy as np
from stickgame.judge import FixedJudge, Judge

@pytest.fixture(params=[3,5], scope="function")
def FJudge(request):
    return FixedJudge(request.param)

@pytest.fixture(params=[3,5], scope="function")
def Jdge(request):
    return Judge(request.param)

class TestFixedJudge:
    def test_initialise(self, FJudge):
        assert isinstance(FJudge.numsticks, int)
        assert FJudge.sumlengths == approx(0.0)

    def test_threshold(self, FJudge):
        assert FJudge.sumlengths + FJudge.threshold >= 0.5*FJudge.numsticks
        FJudge.agent1obs.append(0.1)
        FJudge.agent2obs.append(0.9)
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

class TestJudge:
    def test_initialise(self, Jdge):
        assert isinstance(Jdge.numsticks, int)
        assert np.sum(Jdge.jointbiasprior) == approx(np.ones((3,3)))

    def test_biases2indices(self, Jdge):
        biases = ['s', 'n']
        assert Jdge._biases2indices(biases) == [0, 1]
        biases = ['l', 'l']
        assert Jdge._biases2indices(biases) == [2, 2]

    def test_obslikelihood(self, Jdge):
        biases = ['s', 'n']
        Jdge.agent1obs = [0.3, 0.2]
        assert Jdge._obslikelihood(biases) == approx(0.0)
        biases = ['n', 'l']
        Jdge.agent2obs = [0.2, 0.3]
        assert Jdge._obslikelihood(biases) == approx(0.0)
        Jdge.agent1obs = [0.5]
        Jdge.agent2obs = [0.2, 0.3]
        assert Jdge._obslikelihood(biases) == approx(0.0)
        biases = ['s', 'l']
        Jdge.agent1obs = [0.7]
        Jdge.agent2obs = [0.3]
        assert Jdge._obslikelihood(biases) == approx(0.0)
        biases = ['s', 'l']
        Jdge.agent1obs = [0.3]
        Jdge.agent2obs = [0.7]
        assert Jdge._obslikelihood(biases) == approx(1.0)
        biases = ['n', 's']
        Jdge.agent1obs = [0.5]
        Jdge.agent2obs = [0.2, 0.3]
        if Jdge.numsticks == 5:
            assert Jdge._obslikelihood(biases) == approx(0.6)
        biases = ['n', 'n']
        Jdge.agent1obs = [0.5]
        Jdge.agent2obs = [0.2]
        assert Jdge._obslikelihood(biases) == approx(1.0)
        Jdge.agent1obs = []
        Jdge.agent2obs = []
        assert Jdge._obslikelihood(biases) == approx(1.0)

    def test_compute_p_long(self, Jdge):
        Jdge.agent1obs = [0.5]
        Jdge.agent2obs = [0.2]
        p_long = Jdge.compute_p_long()
        assert isinstance(p_long, float)
        assert 0.0 <= p_long <= 1.0
