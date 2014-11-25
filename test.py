from matplotlib.pyplot import figure, plot
from numpy import arange

fig = figure()
xs = arange(10)
plot(xs, xs, figure=fig)

fig.savefig('/Users/paul/Desktop/pa.png')
