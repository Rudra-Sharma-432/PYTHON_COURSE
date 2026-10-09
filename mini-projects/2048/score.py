def currentScore(grid):
  score = 0
  for row in grid:
    for value in row:
      score += value

  return score
