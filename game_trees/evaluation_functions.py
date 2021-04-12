from state import *
from math import inf

# Here you will implement evaluation functions. Recall that weighing components of your
# evaluation differently can have positive effects on performance. For example, you could
# have your evaluation prioritize running away from opposing agents instead of activiating
# switches. Also remember that for values such as minimum distance to have a positive effect
# you should inverse the value as _larger_ evaluation values are better than smaller ones.

# Helpful Functions:
# You may define any helper functions you want in this file.
# GameState.get_enemies() --> returns a list of opposing agent positions.
# GameState.get_boxes() --> returns a list of (row, col) positions representing where the boxes are on the map
# GameState.get_switches() --> returns a dictionary where the keys are the locations of the switches as (row, col) and the value
#                              being True if the switch is on and False if off.
# GameState.get_player_position() --> returns the current position of the player in the form (row, col)
# GameState.get_remaining_points() --> returns a list of the positions of the remaining armory points of the map in the form (row, col) 
  
class EvaluationFunctions:

  @staticmethod
  def manhattan_heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
  
  @staticmethod
  def score_evaluation(state):
    return state.get_score()
  
  @staticmethod
  def box_evaluation(state):
    #Question 4, your box evaluation solution goes here
    #get get smallest distance between each box and switch, and add to distance between box and player

    switches = state.get_switches() #{(row, col): True/False; ... }
    boxes = state.get_boxes() # [(row, col), ... ]
    enemies = state.get_enemies() #[(row, col), ...]
    pos = state.get_player_position() #(row, col)
    
    for switch in switches:
      if switches[switch]:
        boxes.remove(switch)

    distances = []
    for box in boxes:
      for switch in switches:
        if not switches[switch]:
          d_box_switch = EvaluationFunctions.manhattan_heuristic(box, switch)
          d_player_box = 1/EvaluationFunctions.manhattan_heuristic(box, pos) 
          distances.append(d_box_switch + d_player_box)

    enemy_distances = []
    for enemy in enemies:
      d = EvaluationFunctions.manhattan_heuristic(enemy, pos)
      enemy_distances.append(d)
    
    h = 0
    if len(distances) > 0:
      h = sum(distances)
    if len(enemy_distances) > 0:
      h += sum(enemy_distances)
    return h

  @staticmethod
  def points_evaluation(state):
    #Question 5, your points evaluation solution goes here
    switches = state.get_switches()

    for k in switches:
      key = k
      if switches[key]:
        return inf

    pos = state.get_player_position()
    h = EvaluationFunctions.manhattan_heuristic(pos, key)
    if state.player_has_boots():
      return 1/h

    enemies = state.get_enemies()
    for enemy in enemies:
      h += EvaluationFunctions.manhattan_heuristic(enemy, pos)

    armories = state.get_remaining_points()
    
    for armory in armories:
      h += 1/EvaluationFunctions.manhattan_heuristic(armory, pos)
    
    return h