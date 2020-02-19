// Remove first instance of element found in l
var removeSingleElement = function(element, l) {
  var i = _.indexOf(l, element);
  return l.slice(0, i).concat(l.slice(i+1));
}

// Remove first instances of elements found in l
var removeMultipleElements = function(elements, l) {
  if (elements.length > 0) {
    var new_elements = removeSingleElement(_.first(elements), elements);
    var new_l = removeSingleElement(_.first(elements), l);
    return removeMultipleElements(new_elements, new_l);
  } else {
    return l;
  }
}

// Returns true if list includes every value in values, otherwise returns false
var includesList = function(list, values) {
  if (values.length == 0) {
    return true;
  } else if (_.includes(list, _.first(values))) {
    var new_list = removeSingleElement(_.first(values), list);
    var new_values = removeSingleElement(_.first(values), values)
    return includesList(new_list, new_values);
  } else {
    return false;
  }
}

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
}

module.exports = {
  removeSingleElement, removeMultipleElements, includesList, k_combinations
}
