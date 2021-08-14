var math = require('mathjs');

// lists ways of drawing k items with replacement
function repeated_k_combinations(set, k) {
  var i, combs, head, appendHead;
  // There is no way to take e.g. sets of 5 elements from
  // a set of 4.
  if (k > set.length || k <= 0) {
    return [];
  };

  // K-sized set has only one K-sized subset.
  if (k == set.length) {
    return [set];
  };

  // There is N 1-sized subsets in a N-sized set.
  if (k == 1) {
    combs = [];
    for (i = 0; i < set.length; i++) {
      combs.push([set[i]]);
    }
    return combs;
  };

  combs = [];
  for (var i = 0; i < set.length; i++) {
    head = set[i]
    appendHead = function(set) { return _.flattenDeep(_.concat(set, head)); };
    combs.push(_.map(repeated_k_combinations(set, k-1), appendHead));
  };
  return _.flatten(combs);
};

var possibleSticks = _.map(_.range(0.0, 1.1, .1), function(v) {
  return _.round(v, 3);
});

// support for J1 prior over biases (if bias unknown)
var possibleBiases = [-10.0, -5.0, -2.0, 0.0, 2.0, 5.0, 10.0];

// helper function when adding up scores (to skip computing -Infinity scores)
var meetsTarget = function(stat, target) {
  return ((target == 'long') && (stat >= 0.5)) || ((target == 'short') && (stat < 0.5));
};

// target is 'long' or 'short'
// obs is a single stick value
var getAAScore = function(target, obs, params) {

  var strength = 1 / (1 + Math.exp(-params.gradient * (obs - 0.5)));
  var pLong = 0.5 + 0.5 * (strength - params.threshold);
  var logProb = target == 'long' ? Math.log(pLong) : Math.log(1-pLong);
  return logProb;
};

var getOrthogonal = function(matrix) {
  var qr = math.qr(matrix);
  return qr.Q;
};

var getQuantumScore = function(target, obs, params) {

  var key = String(params.shiftMatrix);
  if (getQuantumScore[key]) {
    return getQuantumScore[key];
  }

  var preshift = math.add(params.shiftMatrix, math.identity(20));
  var shift = getOrthogonal(preshift);

  // get prior vector
  var prior = math.multiply(1 / math.sqrt(20), math.ones(20));

  // transform with shift
  var shiftPrior = math.multiply(shift, prior);

  // project based on observed stick
  var stickIdx = Math.floor(obs * 10) - 1;

  var projMatrix = math.zeros(20, 20);
  projMatrix.subset(math.index(stickIdx, stickIdx), 1);
  projMatrix.subset(math.index(stickIdx+10, stickIdx+10), 1);

  var posterior = math.multiply(projMatrix, shiftPrior);
  posterior     = math.multiply(1 / math.norm(posterior), posterior);

  // normalize and take appropriate hypothesis as final value
  var targetIdx = target == 'long' ? 0 : 10;
  var prob = Math.pow(math.subset(posterior, math.index(stickIdx+targetIdx)), 2);
  var score = Math.log(prob);

  getQuantumScore[key] = score;

  return score;
};

// target is 'long' or 'short'
// obs is a single stick value or array of values
var getJ0Score = function(target, obs, params) {

  // turn obs into array if not already, and then sort it to reduce caching
  var sortObs = _.flatten([obs]).sort()
  var key = params.nSticks + '_' + sortObs + '_' + target;
  if (getJ0Score[key]) {
    return getJ0Score[key];
  };

  var possibleStickSamples = repeated_k_combinations(possibleSticks, params.nSticks-sortObs.length);

  var sum = -Infinity;
  for (var i = 0; i < possibleStickSamples.length; i++) {
    var evidence = _.concat(obs, possibleStickSamples[i]);
    var isLong = _.mean(evidence);
    if (meetsTarget(isLong, target)) {
      sum = numeric.logaddexp(sum, -params.nSticks * Math.log(possibleSticks.length));
    };
  };

  var score = sum + (sortObs.length * Math.log(possibleSticks.length));
  getJ0Score[key] = score;
  return score;
};

// stick must be in sticks
var getS1Score_generator = function(params) {
  var getS1Score = function(stick, sticks, params) {
    var key = params.agentBias + '_' + stick + '_' + sticks;
    if (getS1Score[key]) {
      return getS1Score[key];
    };

    // prevents lying leading to improper nonsense
    if (!_.includes(sticks, stick)) {
      return -Infinity;
    };

    var target = params.agentBias > 0 ? 'long' : 'short';
    var utility = function(possibleStick) {
      var absBias = Math.abs(params.agentBias);
      // bug fix for case of 0 * -Infinity
      return absBias > 0 ? Math.abs(params.agentBias) * getJ0Score(target, possibleStick, params) : 0;
    };
    var truth = utility(stick);

    var sum = utility(sticks[0]);
    for (var i = 1; i < sticks.length; i++) {
      sum = numeric.logaddexp(sum, utility(sticks[i]));
    };

    // bug fix for nSticks = 2, sticks = [1, 1], agentBias < 0 case
    var score = ((truth == -Infinity) && (sum == -Infinity)) ? - Math.log(sticks.length) : truth - sum;
    getS1Score[key] = score;
    return score;
  };
  return getS1Score;
};

// helper function for normalizing scores as list of objects
var normalize = function(dist, sum) {
  var normalizeScalar = function(point) {
    point['score'] = point['score'] - sum;
    return point;
  };
  return _.map(dist, normalizeScalar);
};

// returns array with list of objects giving the scores
//   log p_{J1}(target, possibleBias)
//   for each target and possible bias value
// obs is a single value
var getJ1Joint = function(obs, params) {

  var key = params.nSticks + '_' + obs;
  if (getJ1Joint[key]) {
    return getJ1Joint[key];
  };

  var possibleStickSamples = repeated_k_combinations(possibleSticks, params.nSticks-1);

  // init joint as empty list
  var joint = [];
  // make copy of params to modify
  var testParams = JSON.parse(JSON.stringify(params));
  // init sum of scores across all outcomes
  var sum = -Infinity;

  for (var j = 0; j < possibleBiases.length; j++) {

    testParams.agentBias = possibleBiases[j]
    var getS1Score = getS1Score_generator(testParams);
    var long  = -Infinity;
    var short = -Infinity;

    for (var i = 0; i < possibleStickSamples.length; i++) {

      var evidence = _.concat(obs, possibleStickSamples[i]);
      var speakerScore = getS1Score(obs, evidence, testParams);
      sum = numeric.logaddexp(sum, speakerScore);
      var isLong = _.mean(evidence);

      if (meetsTarget(isLong, 'long')) {
        long = numeric.logaddexp(long, speakerScore);
      } else {
        short = numeric.logaddexp(short, speakerScore);
      };
    };

    joint.push({isLong: 'long', agentBias: testParams.agentBias, score: long});
    joint.push({isLong: 'short', agentBias: testParams.agentBias, score: short});
  };

  var jointDist = normalize(joint, sum);
  getJ1Joint[key] = jointDist;
  return jointDist;
};

var getJ1Score_generator = function(params) {
  var getS1Score = getS1Score_generator(params);
  var getJ1Score = function(target, obs, params) {
    var key = params.nSticks + '_' + params.agentBias + '_' + obs + '_' + target;
    if (getJ1Score[key]) {
      return getJ1Score[key];
    };

    var possibleStickSamples = repeated_k_combinations(possibleSticks, params.nSticks-1);

    var truth = -Infinity;
    var sum   = -Infinity;
    for (var i = 0; i < possibleStickSamples.length; i++) {
      var evidence = _.concat(obs, possibleStickSamples[i]);
      var speakerScore = getS1Score(obs, evidence, params);
      sum = numeric.logaddexp(sum, speakerScore);
      var isLong = _.mean(evidence);
      if (meetsTarget(isLong, target)) {
        truth = numeric.logaddexp(truth, speakerScore);
      };
    };

    var score = truth - sum;
    getJ1Score[key] = score;
    return score;
  };
  return getJ1Score;
};

// computes marginal probability according to dist that rv is target
var marginalize = function(dist, rv, target) {
  return _.reduce(_.map(_.filter(dist, [rv, target]), 'score'), function(sum, n) {
    return numeric.logaddexp(sum, n);
  });
};

var getS2Score_generator = function(params) {
  var getS2Score = function(stick, sticks, params) {
    var key = params.agentBias + '_' + params.biasPenalty + '_' + stick + '_' + sticks;
    if (getS2Score[key]) {
      return getS2Score[key];
    };

    // prevents lying leading to improper nonsense
    if (!_.includes(sticks, stick)) {
      return -Infinity;
    };

    var target = params.agentBias > 0 ? 'long' : 'short';
    var utility = function(possibleStick) {
      var judgeDist = getJ1Joint(possibleStick, params);
      var judgeScore = Math.abs(params.agentBias) * marginalize(judgeDist, 'isLong', target);

      // compute penalty as expected belief of bias magnitude, with coefficient
      var penalty = params.biasPenalty * _.sum(_.map(judgeDist, function(point) {
        return Math.abs(point.agentBias) * Math.exp(point.score);
      }));

      return judgeScore - penalty;
    };
    var truth = utility(stick);

    var sum = utility(sticks[0]);
    for (var i = 1; i < sticks.length; i++) {
      sum = numeric.logaddexp(sum, utility(sticks[i]));
    };

    var score = truth - sum;
    getS2Score[key] = score;
    return score;
  };
  return getS2Score;
};

var getJ2Score_generator = function(params) {
  var getS2Score = getS2Score_generator(params);
  var getJ2Score = function(target, obs, params) {
    var key = params.nSticks + '_' + params.agentBias + '_' + params.biasPenalty + '_' + obs + '_' + target;

    if (getJ2Score[key]) {
      return getJ2Score[key];
    };

    var possibleStickSamples = repeated_k_combinations(possibleSticks, params.nSticks-1);

    var truth = -Infinity;
    var sum   = -Infinity;
    for (var i = 0; i < possibleStickSamples.length; i++) {
      var evidence = _.concat(obs, possibleStickSamples[i]);
      var speakerScore = getS2Score(obs, evidence, params);
      sum = numeric.logaddexp(sum, speakerScore);
      var isLong = _.mean(evidence);
      if (meetsTarget(isLong, target)) {
        truth = numeric.logaddexp(truth, speakerScore);
      };
    };

    var score = truth - sum;
    getJ2Score[key] = score;
    return score;
  };
  return getJ2Score;
};

// function that returns the number of times it has previously been called
var iterationTracker = function() {
  if (_.isFinite(iterationTracker['iter'])) {
    iterationTracker['iter'] += 1;
  } else {
    iterationTracker['iter'] = 0;
  };
  return iterationTracker['iter'];
};

// determines whether iteration should be recorded
var isRecordedIter = function(iter, burn, lag) {
  var cond1 = iter > burn;
  var cond2 = ((iter - burn) % (lag + 1)) == 0;
  return (cond1 && cond2);
};

var logSumExp = function(array) {
  return _.reduce(array, function(sum, x) {return numeric.logaddexp(sum, x)}, -Infinity);
};

module.exports = {
  getJ0Score, getJ1Score_generator, getS1Score_generator, getS2Score_generator,
  getJ2Score_generator, iterationTracker, isRecordedIter, getAAScore, getQuantumScore,
  logSumExp
};