function k_combinations(set, k) {
  var i, j, combs, head, tailcombs;

  // There is no way to take e.g. sets of 5 elements from
  // a set of 4.
  if (k > set.length || k <= 0) {
    return [];
  }

  // K-sized set has only one K-sized subset.
  if (k == set.length) {
    return [set];
  }

  // There is N 1-sized subsets in a N-sized set.
  if (k == 1) {
    combs = [];
    for (i = 0; i < set.length; i++) {
      combs.push([set[i]]);
    }
    return combs;
  }

  combs = [];
  for (i = 0; i < set.length - k + 1; i++) {
    // head is a list that includes only our current element.
    head = set.slice(i, i + 1);
    // We take smaller combinations from the subsequent elements
    tailcombs = k_combinations(set.slice(i + 1), k - 1);
    // For each (k-1)-combination we join it with the current
    // and store it to the set of k-combinations.
    for (j = 0; j < tailcombs.length; j++) {
      combs.push(head.concat(tailcombs[j]));
    }
  }
  return combs;
};

// same as above, but allowing for repetitions
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

// helper function when adding up scores (to skip computing -Infinity scores)
var meetsTarget = function(stat, target) {
  return ((target == 'long') && (stat >= 0.5)) || ((target == 'short') && (stat < 0.5));
};

// target is 'long' or 'short'
// obs is a single stick value
var getJ0Score = function(target, obs, params) {
  var possibleStickSamples = repeated_k_combinations(possibleSticks, params.nSticks-1);

  var sum = -Infinity;
  for (var i = 0; i < possibleStickSamples.length; i++) {
    var evidence = _.concat(obs, possibleStickSamples[i]);
    var isLong = _.mean(evidence);
    if (meetsTarget(isLong, target)) {
      sum = numeric.logaddexp(sum, -params.nSticks * Math.log(possibleSticks.length));
    };
  };
  return sum + Math.log(possibleSticks.length);
};

// stick must be in sticks
var getS1Score = function(stick, sticks, params) {

  // prevents lying leading to improper nonsense
  if (!_.includes(sticks, stick)) {
    return -Infinity;
  };

  var target = params.agentBias > 0 ? 'long' : 'short';
  var utility = function(possibleStick) {
    return Math.abs(params.agentBias) * getJ0Score(target, possibleStick, params);
  };
  var truth = utility(stick);

  var sum = utility(sticks[0]);
  for (var i = 1; i < sticks.length; i++) {
    sum = numeric.logaddexp(sum, utility(sticks[i]));
  };
  return truth - sum;
};

var getJ1Score = function(target, obs, params) {
  var possibleStickSamples = repeated_k_combinations(possibleSticks, params.nSticks-1);

  var truth = -Infinity;
  var sum   = -Infinity;
  for (var i = 0; i < possibleStickSamples.length; i++) {
    var evidence = _.concat(obs, possibleStickSamples[i]);
    sum = numeric.logaddexp(sum, getS1Score(obs, evidence, params));
    var isLong = _.mean(evidence);
    if (meetsTarget(isLong, target)) {
      truth = numeric.logaddexp(truth, getS1Score(obs, evidence, params));
    };
  };
  return truth - sum;
};

module.exports = {
  getJ0Score, getJ1Score
}
