class ScoreHandler:

    @staticmethod
    def read_scores():
        file = open("highscore.txt", "r")
        scores = file.readlines()
        file.close()
        return scores

    @staticmethod
    def write_score(user, score):
        with open("highscore.txt", 'r+') as f:
            scores = [s.split(':') for s in f.read().splitlines()]
            scores.append([user, score])
            scores = sorted(
                scores,
                key=lambda score: float(score[1]),
                reverse=True
            )[:5] # Top 5! (can't really fit more on the screen)
            f.seek(0)
            f.write("\n".join([ ':'.join(s) for s in scores ]) + "\n")
            f.truncate()
