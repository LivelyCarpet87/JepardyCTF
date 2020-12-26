class NoSuchTeamException(Exception):
    def __init__(self, team):
        self.team = team
        self.err = f"Team {self.team} does not exist"
        super().__init__(self.err)

class NoSuchMemberException(Exception):
    def __init__(self, team, member):
        self.team = team
        self.member = member
        self.err = f"Team {self.team} does not contain {self.member}"
        super().__init__(self.err)
