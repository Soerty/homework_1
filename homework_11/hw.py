import numpy as np
from scipy import sparse
from collections import defaultdict

class HMM:
    START = '*'
    TERM = '$'
    REST = '$REST$' # to deal with observed states who have never appeared in train dataset.

    def cond_idx(self, u, v):
        return u + v*self.h_dim

    def fit(self, X, y):
        """
        X - list of lists, observed states
        y - list of lists, hidden states
        estimate elements of A, B matrices from train sequence.
        """

        #######################
        # YOUR CODE HERE

        self.hidden_idx2state = ([list(var) for var in set(tuple(var) for var in y)])
        self.hidden_idx2state.append([self.START, self.TERM])
        self.hidden_states = dict()
        for items in self.hidden_idx2state:
            self.hidden_states[len(items)] = items;
                    
        self.h_dim = len(self.hidden_states)

        self.observed_idx2state = [list(var) for var in set(tuple(var) for var in X)].append([self.START, self.TERM])
        self.observed_states = dict();
        for items in self.observed_idx2state:
            self.observed_states[len(items)] = items;

        self.o_dim=len(self.observed_states)

        #######################


        #######################
        # estimate emission matrix
        # YOUR CODE HERE
        self.B =sparse.csr_matrix( (self.h_dim,self.o_dim) )

        #######################

        self.B_rowsum = np.ravel(self.B.sum(axis=1))


        ########################
        # transition matrix
        # YOUR CODE HERE
        self.A = sparse.csr_matrix( (self.h_dim **2,self.h_dim))
        sparse.csr_matrix.todense(self.A)


        #remember about padding for sequence of hidden states, eg {a, b} -> {START, START, a, b, TERM}
        ########################

        self.A_rowsum = np.ravel(self.A.sum(axis=1))

        return self

    def tr_prob(self, i, j):
        """
        A_ij = q(j | i) = q(j| u, v) with Laplace smoothing
        """
        ########################
        # YOUR CODE HERE
        result = (j*i+1)/(i + self.v)
        ########################
        return result

    def em_prob(self, i, j):
        """
        B_jk = e(x_k| j) with Laplace smoothing
        """
        ########################
        # YOUR CODE HERE
        result = (x_k*j + 1)/(j + self.v)
        ########################
        return result

    def o_state(self, x):
        """
        return index of obseved state
        """
        return self.observed_states.get(x, self.observed_states[self.REST])


    def predict(self, X):
        """
        Predict the most probable sequence of hidden states for every sequence of observed states
        X - list of lists
        """
        y_pred = [self._viterbi(seq) for seq in X]
        return y_pred

    def _viterbi(self, X):
        """
        X - list of observables
        product of probabilities usually is not numerically stable
        remember, that log(ab) = log(a) + log(b) and argmax[log(f(x))] = argmax[f(x)]

        """
        T = len(X)

        # pi[t, u, v] - max probability for any state sequence ending with x_t = v and x_{t-1} = u.
        pi = np.zeros((T + 1, self.h_dim, self.h_dim))
        # backpointers, bp[t, u, v] = argmax probability for any state sequence ending with x_t = v and x_{t-1} = u.
        bp = np.zeros((T + 1, self.h_dim, self.h_dim), dtype=np.int)

        ###################
        # fill tables pi and bp
        # pi[t, u, v] = max_{w} [ pi[t-1, w, u] * q(v| w, u) * e(x_k| v) ]
        # bp[t, u, v] = argmax_{w} [ pi[t-1, w, u] * q(v| w, u) * e(x_k| v) ]
        # YOUR CODE HERE
        for k in range(1, T + 1):
             xk = self.o_state(X[k-1])

             for v in range(self.h_dim):
                 log_b_smoothed = np.log(b)
                 for u in range(self.h_dim):
                     r = np.zeros(self.h_dim)
                     for w in range(self.h_dim):
                         log_a_smoothed = np.log(a)
                         r[w] = log_b_smoothed/log_a_smoothed
                     bp[k, u, v] = np.argmax(r)
                     pi[k, u, v] = np.max(r)

        ###################

        term_idx = self.hidden_states[self.TERM]

        ###################
        # r(u,v) = pi[T, u, v] * q(TERM | u, v)
        # find argmax_{u, v} r(u, v)
        # YOUR CODE HERE
        u, v = pi[u, v]
        ###################

        h_states = [v, u]
        ###################
        # rollback backpointers
        # y_{t-2} = bp[t, y_{t-1}, y_t]
        # h_states is a reversed sequence of hidden states
        # YOUR CODE HERE
        h_states = y.reverse()

        ###################

        return [self.hidden_idx2state[i] for i in reversed(h_states[:T])]



import nltk
nltk.download('treebank')
from nltk.corpus import treebank
from sklearn import metrics

data = treebank.tagged_sents()[:3000]
test_data = treebank.tagged_sents()[3000:3010]

X_train = [[x[0] for x in y] for y in data]
y_train = [[x[1] for x in y] for y in data]

X_test = [[x[0] for x in y] for y in test_data]
y_test = [[x[1] for x in y] for y in test_data]

print('sentence: ', " ".join(X_train[0]))
print('tags: ', " ".join(y_train[0]))

def accuracy(y_true, y_pred):
    y_true = np.concatenate(y_true)
    y_pred = np.concatenate(y_pred)

    return np.mean(y_true == y_pred)

#%%time

hh = HMM().fit(X_train, y_train)
y_pred = hh.predict(X_test)
print(accuracy(y_test, y_pred))


class HmmVectorized(HMM):
    
    def _viterbi(self, X):
        """
        Vectorized version of Viterbi. Let's speed up!
        X - list of observables
        """   
        T = len(X)
        
        # One may notice, at every step t we only need pi[t-1, u, v] = pi_prev[u,v] to compute pi[t, u, v] = pi_curr[u,v]
        pi_prev = np.zeros((self.h_dim, self.h_dim))
        
        # backpointers
        bp = np.zeros((T + 1, self.h_dim, self.h_dim), dtype=np.int)
        
        a_rowsum = self.A_rowsum.reshape(self.h_dim, self.h_dim)
        
        ###################
        # fill pi and bp
        # pi_curr[u, v] = max_{w} [ pi_prev[w, u] * q(v| w, u) * e(x_k| v) ]
        # bp[t, u, v] = argmax_{w} [ pi_prev[w, u] * q(v| w, u) * e(x_k| v) ]
        # don't use tr_prob() and em_prob(), apply laplace smoothing directly here
        # YOUR CODE HERE
         for k in range(1, T + 1):            
             xk = self.o_state(X[k-1])
             pi_curr = np.zeros_like(pi_prev)
            # r(u,v) = pi[T, u, v] * q(TERM | u, v)
             for v in range(self.h_dim):
                 log_b_smoothed = np.log(b)
                 a = self.A[:, v].reshape(self.h_dim, self.h_dim)
                 log_a_smoothed = np.log(a)
                 r =  pi_curr*v
                 bp[k, :, v] = np.argmax(r, axis=1)
                 pi_curr[:, v] = np.max(r, axis=1)
                    
             pi_prev = pi_curr
        ###################
        
        term_idx = self.hidden_states[self.TERM]
        
        ###################
        # r(u,v) = pi[T, u, v] * q(TERM | u, v)
        # find argmax_{u, v} r(u, v)
        # express r(u,v) as matrix additions
        # YOUR CODE HERE
        # u, v = 
        ###################
        
        h_states = [v, u]
        ###################
        # rollback backpointers
        # y_{t-2} = bp[t, y_{t-1}, y_t]
        # h_states is a reversed sequence of hidden states
        # YOUR CODE HERE
        # h_states = 
            
        ###################
        
        return [self.hidden_idx2state[i] for i in reversed(h_states[:T])]
