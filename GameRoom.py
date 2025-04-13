from datetime import datetime

class GameRoom:
    def __init__(self, room_id, room_owner):
        self.__players = []
        self.__room_id = room_id
        self.__room_owner = room_owner
        self.__create_time = datetime.now()
        self.__winner = None

    # Getters
    def get_players(self):
        return self.__players

    def get_room_id(self):
        return self.__room_id

    def get_create_time(self):
        return self.__create_time

    def get_winner(self):
        return self.__winner

    def get_room_owner(self):
        return self.__game_owner

    # Setters
    def set_winner(self, winner):
        self.__winner = winner
    

    # Methods to manage players
    def add_player(self, player):
        if isinstance(player, Player):
            self.__players.append(player)

    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)