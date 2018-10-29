Ok, my agent is still pretty dumb. Unfortunately, I didn't have that much time to invest in it.

What he does:
	- scans the whole matrix and identifies blueprints for the object and the player
	- gets a middle X for both the object and the player, the lower tip of the object, the higher tip of the player (he basically assumes that both the object and the player are squares)
	- based on these and the falling speed, he calculates if there is still time to avoid collision (RUN)
	- if not, he returns to the center, as the center is the best position to be in when the next object arrives(LIVE TO FIGHT ANOTHER DAY)


How can 'he' improve:
	- don't go trough the whole observation 'matrix' (right now, he is really slow, around 30s / test because of that); he can do that by:
		-- skiping a lot of rows by first detecting the whole object, than skip directlly to the bottom, where the player always will sit, according to the algorithm
		-- kind of "binary search"-ing for the object (but not really), by splitting the screen in half (horizontally), than in quarters etc; the player is still at the bottom
	- run even though he can't avoid collision; just because he will collide, he can still take less "damage points" by minimizing the overlapping boxes
	- clean up his act: he has some bugs

Average score: -110 (8 attempts) MUCH WORSE than the Demo Agent :(
