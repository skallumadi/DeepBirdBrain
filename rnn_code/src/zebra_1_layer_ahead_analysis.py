
################################################
# Import statements
################################################

import cPickle
import os
import sys
import time
import numpy
import theano
import theano.tensor as T
from loading_functions import load_all_data, load_class_data_batch
from layer_classes import LinearRegression, Dropout, LSTM, RNN, hybridRNN
from one_ahead import GradClip, clip_gradient
from random import randint


################################################
# Variables to be set
################################################

song_size = 2459
n_hidden = 60;

num_songs_in_batch = 30

savefilename_pre = '/vega/stats/users/sl3368/rnn_code/results/lstm/1_layer/1000/generated/'

params_file = '/vega/stats/users/sl3368/rnn_code/saves/params/lstm/1_layer/1000/zebra_5th_1_500.save'

test_cost = .02 #general validation number

################################################
# Loading data
################################################


dataset_info = load_all_data()
stim = dataset_info[0]
data_set_x = theano.shared(stim, borrow=True)


###############################################################
# (Re-Define) Architecture: input --> LSTM --> predict one-ahead
###############################################################

x = T.matrix('x')  # the data is presented as a vector of inputs with many exchangeable examples of this vector
x = clip_gradient(x,1.0)    
is_train = T.iscalar('is_train') # pseudo boolean for switching between training and prediction

rng = numpy.random.RandomState(1234)

lstm_1 = LSTM(rng, x, n_in=data_set_x.get_value(borrow=True).shape[1], n_out=n_hidden)

output = LinearRegression(input=lstm_1.output, n_in=n_hidden, n_out=data_set_x.get_value(borrow=True).shape[1])

################################################
# Load learned params
################################################


f = file(params_file, 'rb')
old_p = cPickle.load(f)
f.close()

lstm_1.W_i.set_value(old_p[0].get_value(), borrow=True)
lstm_1.W_f.set_value(old_p[1].get_value(), borrow=True)
lstm_1.W_c.set_value(old_p[2].get_value(), borrow=True)
lstm_1.W_o.set_value(old_p[3].get_value(), borrow=True)
lstm_1.U_i.set_value(old_p[4].get_value(), borrow=True)
lstm_1.U_f.set_value(old_p[5].get_value(), borrow=True)
lstm_1.U_c.set_value(old_p[6].get_value(), borrow=True)
lstm_1.U_o.set_value(old_p[7].get_value(), borrow=True)
lstm_1.V_o.set_value(old_p[8].get_value(), borrow=True)
lstm_1.b_i.set_value(old_p[9].get_value(), borrow=True)
lstm_1.b_f.set_value(old_p[10].get_value(), borrow=True)
lstm_1.b_c.set_value(old_p[11].get_value(), borrow=True)
lstm_1.b_o.set_value(old_p[12].get_value(), borrow=True)
output.W.set_value(old_p[13].get_value(), borrow=True)
output.b.set_value(old_p[14].get_value(), borrow=True)



################################################
# Generate 1 ahead function
################################################
previous_samples = T.matrix()

ygen_model = theano.function(inputs=[previous_samples],
        outputs=output.E_y_given_x,
        givens={x: previous_samples})


################################################
# Generate the sequence
################################################
print 'Generating....'

#index = randint(0,num_songs_in_batch)
index = 0

print 'Song: '+str(index)

y_gen_truth = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
y_gen = ygen_model(y_gen_truth)

half = song_size/2

step = 5
y_gen_5 = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
#for i in xrange(half,song_size-1):
#    tmp = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
#    tmp[i+1-step] = ygen_model(y_gen_truth[0:i-step])[i-1-step]
#    for s in xrange(1,step):
#	tmp[i+1+s-step] = ygen_model(tmp[0:i+s-step])[i+s-1-step]
#    y_gen_5[i] = tmp[i]

print 'Done with 5...'

step = 15
y_gen_10 = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
for i in xrange(half,song_size-1):
    tmp = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
    tmp[i+1-step] = ygen_model(y_gen_truth[0:i-step])[i-1-step]
    for s in xrange(1,step):
	tmp[i+1+s-step] = ygen_model(tmp[0:i+s-step])[i+s-1-step]
    y_gen_10[i] = tmp[i]

print 'Done with 10...'

step = 25
y_gen_25 = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
#for i in xrange(half,song_size-1):
#    tmp = data_set_x[index * song_size:((index + 1) * song_size - 1)].eval()
#    tmp[i+1-step] = ygen_model(y_gen_truth[0:i-step])[i-1-step]
#    for s in xrange(1,step):
#	tmp[i+1+s-step] = ygen_model(tmp[0:i+s-step])[i+s-1-step]
#    y_gen_25[i] = tmp[i]

print 'Finished Generating...'

################################################
# Plot it
################################################

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.imshow(numpy.transpose(y_gen2))
#plt.axvline(x=1000, ymin=0, ymax = 60, linewidth=3, color='r')
#ax.set_aspect(20)
#plt.show()

################################################
# Store it
################################################
print 'Saving...'

savefilename = savefilename_pre + str(index)+'_zebra.ahead_analysis_15'

f = file(savefilename, 'wb')
for obj in [[y_gen_truth] + [y_gen] + [y_gen_5] + [y_gen_10] + [y_gen_25]]:
    cPickle.dump(obj, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
