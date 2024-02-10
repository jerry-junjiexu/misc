# This is the code I wrote for an interview question:
#  People place orders when they move around. Each order has a unique id and (x, y) location.
#  We have a list of POIs that can fulfill orders. Each POI has a unique id and (x, y) location.
#  For each order, determine the closest POI.

import math
import random
from typing import List

class Poi:
  def __init__(self, id: int, x: int, y: int):
    self.id = id
    self.x = x
    self.y = y

class Order:
  def __init__(self, id: int, x: int, y: int):
    self.id = id
    self.x = x
    self.y = y

class QuadTreeNode:
  SPLIT_THRESHOLD = 100
  def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int):
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax
    self.children = []
    self.pois = []

  def insertPoiToContainingChild(self, poi: Poi) -> None:
    for child in self.children:
      if poi.x >= child.xmin and poi.x < child.xmax and poi.y >= child.ymin and poi.y < child.ymax:
        child.insertPoi(poi)
        break
      
  def split(self) -> None:
    self.children.append(QuadTreeNode(self.xmin, (self.xmin + self.xmax)//2, self.ymin, (self.ymin + self.ymax)//2))
    self.children.append(QuadTreeNode((self.xmin + self.xmax)//2, self.xmax, self.ymin, (self.ymin + self.ymax)//2))
    self.children.append(QuadTreeNode(self.xmin, (self.xmin + self.xmax)//2, (self.ymin + self.ymax)//2, self.ymax))
    self.children.append(QuadTreeNode((self.xmin + self.xmax)//2, self.xmax, (self.ymin + self.ymax)//2, self.ymax))
    for poi in self.pois:
      self.insertPoiToContainingChild(poi)
    del self.pois[:]
    
  def insertPoi(self, poi: Poi) -> None:
    if self.children:
      self.insertPoiToContainingChild(poi)
    else:
      self.pois.append(poi)
      if len(self.pois) > self.SPLIT_THRESHOLD:
        self.split()
        
  def findClosePois(self, x: int, y: int, max_distance: int) -> List[Poi]:
    if x < self.xmin - max_distance or x > self.xmax + max_distance or y < self.ymin - max_distance or y > self.ymax + max_distance:
      return []
    pois = [poi for poi in self.pois if math.sqrt((x-poi.x)**2 + (y-poi.y)**2) <= max_distance]
    for child in self.children:
      pois.extend(child.findClosePois(x, y, max_distance))
    return pois

# Fake some data to test the implementation.
pois = [Poi(i, random.randint(-1e6, 1e6), random.randint(-1e6, 1e6),) for i in range(1000)]
poi_tree = QuadTreeNode(xmin=-1e9, xmax=1e9, ymin=-1e9, ymax=1e9)
for poi in pois:
  poi_tree.insertPoi(poi)

close_poi_order_pairs = []
orders = [Order(poi.id, poi.x + random.randint(-200, 200), poi.y + random.randint(-200, 200)) for poi in pois]
for order in orders:
  close_poi_order_pairs.extend([(order.id, poi.id) for poi in poi_tree.findClosePois(x=order.x, y=order.y, max_distance=100)])
print(close_poi_order_pairs)
