import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import itertools

"""
def boltzmann_loss(y_true, y_pred):
    #wierd "boltzmann" loss function
    return np.sum(np.exp(-y_true * y_pred))
"""

def boltzmann_loss(y_true, y_pred):
    return np.sum(np.exp(np.abs(y_true - y_pred)))
def mean_squared_error(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean()

def mean_squared_logarithmic_error(y_true, y_pred):
    return ((np.log1p(y_true) - np.log1p(y_pred)) ** 2).mean()

def huber_loss(y_true, y_pred, delta=1.0):
    error = y_true - y_pred
    is_small_error = np.abs(error) <= delta
    squared_loss = 0.5 * error**2
    linear_loss = delta * (np.abs(error) - 0.5 * delta)
    return np.where(is_small_error, squared_loss, linear_loss).mean()

TARGET = np.array([3, 3])
BOUNDS = {'start': 0,
          'stop' : 10,
          'step' :0.1}
loss = {
    'boltzmann': lambda y: boltzmann_loss(y, TARGET),
    'mse': lambda y: mean_squared_error(y, TARGET),
    'msle': lambda y: mean_squared_logarithmic_error(y, TARGET),
    'huber': lambda y: huber_loss(y, TARGET),
}

x = np.arange(**BOUNDS)
y = np.arange(**BOUNDS)

X, Y = np.meshgrid(x, y)

Z = np.zeros(X.shape)

def create_surface(loss_function):
    # N.B uses global X, Y, Z
    for i, j in itertools.product(range(X.shape[0]), range(X.shape[1])):
        Z[i, j] = loss_function(np.array([X[i, j], Y[i, j]]))
    return Z

for label, loss_function in loss.items():
    Z = create_surface(loss_function)
    fig = go.Figure(go.Surface(x=X, y=Y, z=Z))
    fig.write_html("plots/{}.html".format(label))


