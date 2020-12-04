import configparser
import random

class Game():
    def __init__(self, santas, all_bad_matches):
        self.send = False
        self.santas = []
        self.players = santas
        self.all_bad_matches = all_bad_matches

    def start(self):
        self.clear()

        for player in self.players:
            player = player.split()
            name, email = player[0], player[1]

            self.build_santas(self.all_bad_matches, name, email)

        recievers = self.santas.copy()

        matches = Match.create_matches(self.santas, recievers)

        if self.bad_match_check(matches):
            return self.start()

        return matches

    def build_santas(self, all_bad_matches, name, email):
        bad_matches = []
        for match in all_bad_matches:
            match = match.split(", ")
            if name in match:
                for person in match:
                    if name != person:
                        bad_matches.append(person)

        s = Santa(name, email, bad_matches)
        self.santas.append(s)

    # this has about a 50% chance of being ran, but fixes the problem
    def bad_match_check(self, matches):
        bad = False

        for match in matches:
            if match.santa.name == match.santee.name:
                bad = True

            if match.santa.name in match.santee.bad_matches:
                bad = True

            if match.santee.name in match.santa.bad_matches:
                bad = True

        return bad

    def clear(self):
        self.santas = []



class Santa():
    def __init__(self, name, email, bad_matches):
        self.name = name
        self.email = email
        self.bad_matches = bad_matches


class Match():
    def __init__(self, santa, santee):
        self.santa = santa
        self.santee = santee

    @staticmethod
    def create_matches(santas, santees):
        aas = santas.copy()
        ees = santees.copy()

        matches = []
        try:
            for a in aas:
                ee = Match.select_santee(a, ees)
                ees.remove(ee)
                matches.append(Match(a, ee))
        except:
            return Match.create_matches(santas, santees)

        return matches

    @staticmethod
    def select_santee(santa, santees):
        rand = random.choice(santees)

        if santa.name == rand.name or santa.name in santa.bad_matches:
            if len(santees) < 2:
                raise Exception("need a redo")
            else:
                return Match.select_santee(santa, santees)

        return rand

    def __str__(self):
        return "Match: " + self.santa + " -> " + self.santee


class SMTP():
    def __init__(self, info):
        self.server = info[0]
        self.port = info[1]
        self.username = info[2]
        self.password = info[3]

    #@staticmethod
    def sendmail(self, match):
        print("sending email to " + match.santa.name + " about " + match.santee.name)


class Parser():
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

        game = self.config['GAME']
        self.players = game['PLAYERS'].strip().splitlines()
        self.all_bad_matches = game['BADMATCHES'].strip().splitlines()

        smtp = self.config['SMTP']
        self.smtp_info = [smtp['SERVER'],
                            smtp['PORT'],
                            smtp['USERNAME'],
                            smtp['PASSWORD']]

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        self._players = value

    @property
    def all_bad_matches(self):
        return self._all_bad_matches

    @all_bad_matches.setter
    def all_bad_matches(self, value):
        self._all_bad_matches = value

    @property
    def smtp_info(self):
        return self._smtp_info

    @smtp_info.setter
    def smtp_info(self, value):
        self._smtp_info = value


def main():
    parser = Parser('config.ini')
    game = Game(parser.players, parser.all_bad_matches)
    smtp = SMTP(parser.smtp_info)

    matches = game.start()

    for match in matches:
        smtp.sendmail(match)


def efficiency_test(game, trials):
    bad_count = 0
    for i in range(trials):

        matches = game.start(santas, all_bad_matches)
        bad = False

        for match in matches:
            if match.santa.name == match.santee.name:
                bad = True
            if match.santa.name in match.santee.bad_matches:
                bad = True
            if match.santee.name in match.santa.bad_matches:
                bad = True

        if bad:
            bad_count += 1

    print("failure rate: " + str(bad_count / trials))


if __name__ == "__main__":
    main()
