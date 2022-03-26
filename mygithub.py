import requests
import json


class MetOptRepo:
    _repo_owner = 'grinvlad'
    _repo = 'optimization-methods'
    team = {
        'Никиты': 'shoshshesh',
        'Тани': 'ptyvvs',
        'Влада': 'grinvlad',
    }

    def __init__(self):
        req = requests.get(f'https://api.github.com/repos/{MetOptRepo._repo_owner}/{MetOptRepo._repo}/commits')
        src = req.text
        self._all_commits = json.loads(src)

    def commits_to_str(self, name: str, n: int) -> str:
        commits = self._choose_last_n_commits(name, n)
        s = ''
        for i in range(n-1, -1, -1):
            s += MetOptRepo._commit_to_str(commits[i]) + '\n'
        return s

    @staticmethod
    def _commit_to_str(commit):
        s = f"message:  '{commit['commit']['message']}'\n" \
            f"author:  {commit['author']['login']}\n" \
            f"date:  {commit['commit']['author']['date'].replace('T', '  ')[:-4]}\n"
        return s

    def _choose_last_n_commits(self, name: str, n: int) -> list:
        try:
            login = MetOptRepo.team[name]
        except KeyError:
            return self._all_commits[:n]

        last_users_commits = [commit for commit in self._all_commits if commit['author']['login'] == login]
        return last_users_commits
