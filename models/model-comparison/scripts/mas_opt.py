import numpy as np
from jax import vmap, grad
from jax.scipy.special import logit, expit
import jax.numpy as jnp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("input/rsa-het-data.csv").query('firstStick == 0.9')[['agent1stick', 'belief']]
obs = df.to_numpy()

def ls_point(stick, belief, params):
    
    gradient  = jnp.exp(params[0])
    threshold = expit(params[1])
    strength  = expit(gradient * (stick - 0.5))

    mas_belief = 0.5 + 0.5 * (strength - threshold)
                        
    return (mas_belief - belief) ** 2

def ls(params):
    residuals = vmap(ls_point, in_axes=(0, 0, None))(obs[:,0], obs[:,1], params)
    return jnp.sum(residuals)

def step(params, eta):
    g = grad(ls)(params)
    params -= eta * g
    return params, jnp.linalg.norm(g)

num_steps = 1000
etas      = 0.1 * np.ones(num_steps)
params    = np.random.randn(2)

for i in range(num_steps):
    params, gnorm = step(params, etas[i])
    if (i % 50) == 0:
        print("iter: {}, score: {}, gnorm: {}".format(i, ls(params), gnorm))
    if gnorm < 1e-2:
        print("iter: {}, score: {}, gnorm: {}".format(i, ls(params), gnorm))
        break

lin_thresh = 1 + np.mean(obs[:, 0 ]) - 2 * np.mean(obs[:, 1])

sticks = np.linspace(0.6, 0.9, 4)

def belief(stick, gradient, threshold):
    strength = expit(gradient * (stick - 0.5))
    mas_belief = 0.5 + 0.5 * (strength - threshold)
    return mas_belief

def lin_belief(stick, threshold):
    strength = stick
    mas_belief = 0.5 + 0.5 * (strength - threshold)
    return mas_belief

plt.figure(figsize=(10, 8))
sns.lineplot(x='agent1stick', y='belief', data=df, err_style='bars', ci=95, label='Human');
plt.plot(sticks, [belief(stick, jnp.exp(params[0]), expit(params[1])) for stick in sticks], label='MAS (best logistic fit)');
plt.plot(sticks, [belief(stick, jnp.exp(params[0]), 0.9) for stick in sticks], label='MAS (with WEE)');
plt.plot(sticks, [lin_belief(stick, lin_thresh) for stick in sticks], label='MAS (best linear fit)');
plt.title('MAS Model Predictions vs. Human Weak Evidence Effect Data');
plt.xlabel('judge stick');
plt.ylabel('belief about mean');
plt.legend();

plt.xticks(sticks);
plt.yticks(np.linspace(0., 1, 11));
