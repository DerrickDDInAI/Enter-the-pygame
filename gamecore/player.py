#=====================================================================
# Classes
#=====================================================================

class Player:
    """
    Player has 2 attributes: name, xxx
    * name: xxx
    * xxx: xxx
    
    And Player class has 2 class attributes: count_created_players, players_list
    * count_created_players: int starting at 0, to count the number of players created
    * players_list: empty list to store the players
    """

    # class attributes
    count_created_players = 0
    players_list = []
    
    def __init__(
        self,
        name: str = None
    ):
        """
        Function to create an instance of Player class
        By default:
        * name is "player_1", then "player_2" if no name is provided
        """
        Player.count_created_players += 1
        if name is None:
            self.name = f"player_{Player.count_created_players}"
        else:
            self.name = name

        Player.players_list.append(self)

    def __repr__(self):
        """
        In order to print the Player instance in the specified format
        """
        return f"{self.name}"


#============================================================
# Main functions
#============================================================

def main():
    player_1 = Player('Yoyo')
    player_2 = Player()
    print(player_1)
    print(player_2)


#============================================================
# Run
#============================================================

## if you directly run this program, main() fct will create 2 player instances and print them
if __name__ == '__main__':
    main()