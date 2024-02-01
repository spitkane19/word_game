# word_game
Distributed systems course project by Severi and Eemeli
1 ) Aim is to create a word multiplayer game where we have a word that needs to be guessed by the player with least amount of guesses. The players race against each other and the winner is the one with the least guesses to get the right word. In case of a tie the player that used the least time to get the right word wins. The game will use a client-server model.
2 ) Server, client, client, game state, messaging system, game logic. Pretty simple client-server model for system architecture. Object-based style will be used for software architecture. Game state has all the data about the word that needs to be guessed, the guesses so far and the times of the players. It will also handle fault tolerance so for instance if a client disconnects it will save their progress and the client will get the progress back when reconnected. Game logic checks whether the guesses are correct and updates the ui according to the guess. So a yellow color for correct letter at the wrong place, red for wrong letter, green for correct letter at right spot. Messaging system will handle messages. Logs also important for debug and evaluation of lost messages and latencies.
Optional if we have time:
Scalability for more than 2 players, other than command prompt ui, lobby for game, security, latency normalisation.
3 ) Centralized control, client-server model and centralized organization.


