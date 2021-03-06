import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  for i in xrange(num_train):
        s = np.dot(X[i],W)
        s -= np.max(s)
        loss_j_nte_y = 0
        loss_j_e_y = 0
        for j in xrange(num_classes):
            if j == y[i]:
                loss += -s[j]
                loss_j_e_y = np.exp(s[j])
            else:    
                loss_j_nte_y += np.exp(s[j])
        for j in xrange(num_classes):
            #dW[:,j] += X[i,:].T
            if j != y[i]:
                dW[:,j] += np.exp(s[j])*X[i,:].T / (loss_j_e_y + loss_j_nte_y)
            if j == y[i]:
                dW[:,y[i]] += X[i].T*(-1 + (loss_j_e_y / (loss_j_e_y + loss_j_nte_y)))
        loss += np.log(loss_j_nte_y + loss_j_e_y)
  
  loss /= num_train
  dW /= num_train  

  loss += 0.5*reg*np.sum(W*W)
  dW += reg*W
  
  pass
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = X.shape[1]
    
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  s = np.dot(X,W)
  s -= np.reshape(np.max(s,axis=1),(num_train,1))
  loss_i = -s[range(num_train),y] + np.log(np.sum(np.exp(s),axis=1))
  loss = np.sum(loss_i) / num_train
  loss += 0.5*reg*np.sum(W*W)
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  sum = np.sum(np.exp(s),axis=1).astype(float)
  c = np.exp(s)
  c[range(num_train),y] = np.exp(s[range(num_train),y]) - sum
  c = np.divide(c,np.reshape(sum,(num_train,1)))  
  dW = np.dot(X.T,c)
  dW /= num_train
  dW += reg*W
  return loss, dW

