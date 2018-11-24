class ScoreHandler:

    @staticmethod
    def read_scores():
        file = open("highscore.txt", "r")
        scores = file.readlines()
        file.close()
        return scores

    # TODO: max number of highscores?
    # TODO: order the scores
    @staticmethod
    def write_score(user, score):
        file = open("highscore.txt", "a")
        file.write(user)
        file.write(":")
        file.write("{0:.2f}".format(score))
        file.write("\n")
        file.close()
