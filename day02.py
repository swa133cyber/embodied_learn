import numpy as np

position = np.array([[1,1],[2,4],[5,2],[4,1],[7,3],[8,1],[0,4]])
target = np.array([6,6])
test = np.array(3,)
err = target - position
print (np.linalg.norm(err,axis = 1))