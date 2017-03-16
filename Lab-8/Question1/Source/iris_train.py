

import tensorflow as tf
import numpy as np
from tensorflow.contrib.session_bundle import exporter
from numpy import genfromtxt
# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
from sklearn import datasets
from sklearn.model_selection import train_test_split

def buildDataFromIris():
    iris = datasets.load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.33, random_state=42)
    f=open('cs-training.csv','w')
    for i,j in enumerate(X_train):
        k=np.append(np.array(y_train[i]),j   )
        f.write(",".join([str(s) for s in k]) + '\n')
    f.close()
    f=open('cs-testing.csv','w')
    for i,j in enumerate(X_test):
        k=np.append(np.array(y_test[i]),j   )
        f.write(",".join([str(s) for s in k]) + '\n')
    f.close()


# Convert to one hot
def convertOneHot(data):
    y=np.array([int(i[0]) for i in data])
    y_onehot=[0]*len(y)
    for i,j in enumerate(y):
        y_onehot[i]=[0]*(y.max() + 1)
        y_onehot[i][j]=1
    return (y,y_onehot)


buildDataFromIris()


data = genfromtxt('cs-training.csv',delimiter=',')  # Training data
test_data = genfromtxt('cs-testing.csv',delimiter=',')  # Test data

x_train=np.array([ i[1::] for i in data])
y_train,y_train_onehot = convertOneHot(data)

x_test=np.array([ i[1::] for i in test_data])
y_test,y_test_onehot = convertOneHot(test_data)


#  A number of features, 4 in this example
#  B = 3 species of Iris (setosa, virginica and versicolor)
A = data.shape[1]-1 # Number of features, Note first is y
B = len(y_train_onehot[0])
x = tf.placeholder(tf.float32, [None, A],name='x') # Features
W = tf.Variable(tf.zeros([A,B]),name='W')
b = tf.Variable(tf.zeros([B]),name='b')
#tf_softmax = tf.nn.softmax(tf.matmul(tf_in,tf_weight) + tf_bias)

sess = tf.Session()
tf.logging.set_verbosity(tf.logging.INFO)



y = tf.nn.softmax(tf.matmul(x, W) + b,name='y')
y_ = tf.placeholder(tf.float32, [None, B],name='y_')
tf.add_to_collection('variables',W)
tf.add_to_collection('variables',b)

cross_entropy = -tf.reduce_sum(y_*tf.log(y))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# save summaries for visualization
#tf.summary.histogram('weights', W)
#tf.summary.histogram('max_weight', tf.reduce_max(W))
#tf.summary.histogram('bias', b)
#tf.summary.scalar('cross_entropy', cross_entropy)
#tf.summary.histogram('cross_hist', cross_entropy)
# merge all summaries into one op
merged=tf.summary.merge_all()

trainwriter=tf.summary.FileWriter('data/iris_model'+'/logs/train',sess.graph)

init = tf.global_variables_initializer()
sess.run(init)
y_train_onehot=np.asarray(y_train_onehot)
for i in range(10):
    print(y_train_onehot)
    summary, _ = sess.run([train_step], feed_dict={x: x_train, y_: y_train_onehot})

    trainwriter.add_summary(summary, i)

# model export path
export_path = 'data/iris_model'
print('Exporting trained model to', export_path)

#
saver = tf.train.Saver(sharded=True)
model_exporter = exporter.Exporter(saver)
model_exporter.init(
    sess.graph.as_graph_def(),
    named_graph_signatures={
        'inputs': exporter.generic_signature({'images': x}),
        'outputs': exporter.generic_signature({'scores': y})})

model_exporter.export(export_path, tf.constant(1), sess)

