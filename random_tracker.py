import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

## This code fills a space with particles with random velocity.
## Can be used as a tracking benchmark.

'''
         2
   **************
   *            *
   *            *
   *            *
 3 *            * 1
   *            *
   *            *
   *            *
   **************
         0
         
each tracker = [x y vx vy]
'''
class RandomTracker:
  ###
  # N == num of particles
  # DT == delta time
  # L == size of the space (square)
  # Noise == measurement noise
  # vmin, vmax
  # dmin == distance between start and finish points of each particle must be at least dmin*L
  ###
  def __init__(self, N=1, DT=0.02, L=100, Noise = 0.1, vmin=5, vmax=40, dmin = 0.5):
    self.N = N
    self.DT = DT
    self.L = L
    self.Noise = Noise
    self.vmin = vmin
    self.vmax = vmax
    self.dmin = dmin
    self.trackers = np.zeros((self.N,4))
    # Initialize all trackers
    for i in range(self.N):
      self.trackers[i,:] = self.gen_one_tracker()
        
  def gen_one_tracker(self):
    while(True):
      pick = np.random.choice(4, 2) # pick two sides of the space
      p = np.zeros((2,2)) # end points
      for i in range(2):
        x = pick[i]
        if x==0:
          p[i,0] = np.random.rand()*self.L
          p[i,1] = 0
        elif x==2:
          p[i,0] = np.random.rand()*self.L
          p[i,1] = self.L
        elif x==1:
          p[i,0] = self.L
          p[i,1] = np.random.rand()*self.L
        else: # x==3
          p[i,0] = 0
          p[i,1] = np.random.rand()*self.L
      delta_p = p[1,:]-p[0,:]
      dist = LA.norm(delta_p)
      if (dist>=self.L*self.dmin):
        v = np.random.uniform(self.vmin,self.vmax)
        theta = np.arctan2(delta_p[1],delta_p[0])
        vx, vy = v*np.cos(theta), v*np.sin(theta)
        return np.array([p[0,0],p[0,1],vx,vy])
      else:
        continue
    
  def step(self):
    self.trackers[:,:2] += self.DT*self.trackers[:,2:] # move one DT
    rows_out_of_bound = [i for i in range(self.N) if self.trackers[i,0]>self.L or self.trackers[i,0]<0 or self.trackers[i,1]>self.L or self.trackers[i,1]<0]
    self.trackers = np.delete(self.trackers, rows_out_of_bound, axis=0)
    # Generate new tracks to make total trackers = N
    n_trackers = self.trackers.shape[0]
    for i in range(self.N-n_trackers):
      self.trackers = np.vstack([self.trackers, self.gen_one_tracker()])

  def draw(self):
    plt.cla()
    plt.grid(True)
    plt.axis("equal")
    plt.xlim([0,100])
    plt.ylim([0,100])
    plt.plot(self.trackers[:,0], self.trackers[:,1], 'ko',markersize=4)
    plt.pause(self.DT)

  def print_trackers(self):
    for i in range(self.N):
      print("{}, {}".format(self.trackers[i,0], self.trackers[i,1]))


if __name__ == "__main__":
  rt = RandomTracker(N=50)
  steps = 5000
  plt.pause(5)
  for i in range(steps):
    rt.step()
    rt.draw()
    #rt.print_trackers()
  plt.show()
