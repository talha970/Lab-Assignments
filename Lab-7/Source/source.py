
from __future__ import print_function
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
rng = np.random
f = open('housing.data', 'r')

trX = np.linspace(-1, 1, 101)

# create a y value which is approximately linear but with some random noise
mydata = list(map(str.split, f))
trainx=[]
trainy=[]
test_X=[]
test_Y=[]
allx=[]
ally=[]
for i in mydata:
    allx.append(float(i[12]))
    ally.append(float(i[13]))

trainx=allx[0:450];
trainy=ally[0:450];
test_X=allx[451:506]
test_Y=ally[451:506];
trainx=np.asarray(trainx)
trainy=np.asarray(trainy)
test_X=np.asarray(test_X)
test_Y=np.asarray(test_Y)
trX = trainx


trY = 2 * trX + 4+np.random.randn(*trX.shape) * 0.033
trY=trainy
# create symbolic variables

X = tf.placeholder("float")

Y = tf.placeholder("float")

# create a shared variable for the weight matrix

w = tf.Variable(rng.randn(), name="weights")

b = tf.Variable(rng.randn(), name="bias")

# prediction function
y_model = tf.add(tf.multiply(X, w), b)


# Mean squared error

cost = tf.reduce_sum(tf.pow(y_model-Y, 2))/(2*100)

# construct an optimizer to minimize cost and fit line to my data

train_op = tf.train.GradientDescentOptimizer(0.5).minimize(cost)


# Launch the graph in a session
sess = tf.Session()

# Initializing the variables

init = tf.global_variables_initializer()


# you need to initialize variables
sess.run(init)


for i in range(100):
    for (x, y) in zip(trX, trY):
        sess.run(train_op, feed_dict={X: x, Y: y})

print("Optimization Finished!")
training_cost = sess.run(cost, feed_dict={X: trX, Y: trY})

print("Training cost=", training_cost, "W=", sess.run(w), "b=", sess.run(b), '\n')

# Testing or Inference


print("Testing... (Mean square loss Comparison)")

testing_cost = sess.run(
    tf.reduce_sum(tf.pow(y_model - Y, 2)) / (2 * test_X.shape[0]),
    feed_dict={X: test_X, Y: test_Y})  # same function as cost above
print("Testing cost=", testing_cost)
print("Absolute mean square loss difference:", abs(
    training_cost - testing_cost))
plt.plot([96.6985,0,0,11.7597,8.4621,24.5398,0,28.0299,0,0,100,0,0])
plt.show()