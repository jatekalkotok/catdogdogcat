class ScoreHandler:

    _file = "highscore.txt"
    _max = 5 # Top 5! (can't really fit more on the screen)

    @staticmethod
    def read_scores():
        with open(ScoreHandler._file, 'r') as f:
            return f.readlines()

    @staticmethod
    def write_score(user, score):
        with open(ScoreHandler._file, 'r+') as f:
            scores = [s.split(':') for s in f.read().splitlines()]
            scores.append([user, score])
            scores = sorted(
                scores,
                key=lambda score: float(score[1]),
                reverse=True
            )[:ScoreHandler._max]
            f.seek(0)
            f.write("\n".join([ ':'.join(s) for s in scores ]) + "\n")
            f.truncate()
