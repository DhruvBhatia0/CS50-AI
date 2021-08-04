import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        return 0 if player == 1 else 1

    def switch_player(self):
        self.player = Nim.other_player(self.player)

    def move(self, action):
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        if (tuple(state),tuple(action)) in self.q.keys():
            return self.q[tuple(state),tuple(action)]
        return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        new_p = old_q + self.alpha*(future_rewards - old_q + reward)
        self.q[tuple(state),tuple(action)] = new_p

    def best_future_reward(self, state):
        best = 0
        for i in Nim.available_actions(state):
            if self.get_q_value(state,i) > best:
                best = self.get_q_value(state,i)
        return best

    def choose_action(self, state, epsilon=True):
        
        if epsilon:
            a = random.randint(1,100)
            if a <= (self.epsilon * 100):
                return random.sample(list(Nim.available_actions(state)),1)[0]
        best = float('-inf')
        for action in Nim.available_actions(state):
            if self.get_q_value(state,action) > best:
                best = self.get_q_value(state,action)
                best_action = action
        return best_action
        


def train(n):

    player = NimAI()

    # Play n games
    print(f'the ai will now play itself {n} times')
    print('training begins in 3')
    time.sleep(1)
    print('training begins in 2')
    time.sleep(1)
    print('training begins in 1')
    time.sleep(1)
    for i in range(n):
        print(f"getting that bread: {i + 1} 👌")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("😎😎😎😎😎😎😎😎")

    # Return the trained AI
    return player


def play(ai, human_player=None):

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}", pile*'😼')
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            if winner == 'Human':
                l = ['(╬▔皿▔)╯','┗|｀O′|┛','o((>ω< ))o']
                print(random.sample(l,1)[0])
            else:
                l=['╰(*°▽°*)╯','(⌐■_■)','(✿◡‿◡)']
                print(random.sample(l,1)[0])
            return
