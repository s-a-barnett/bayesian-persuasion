How to run experiment
-------------------

1. call `npm install` to pull dependencies
2. in `screen` or `tmux`, first launch `node store.js` (make sure you have `auth.json` credentials in directory)
3. next, launch `node app.js --gameport 8888`. If you get an error try another port between 8880 and 8889.
4. navigate to `https://www.stanford-cogsci.org:8888/experiment1.js`

Notes
-----

* I typically use [`nosub`](https://github.com/longouyang/nosub) to both test (via sandbox) and launch HITs on mturk.

* Different conditions were inserted into mongo using `prep_mongo.py` script.