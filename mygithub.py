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

    def commits_to_str(self, name: str) -> str:
        commits = self._choose_last_3_commits(name)
        s = ''
        for i in range(2, -1, -1):
            s += MetOptRepo._commit_to_str(commits[i]) + '\n'
        return s

    @staticmethod
    def _commit_to_str(commit):
        s = f"message:  '{commit['commit']['message']}'\n" \
            f"author:  {commit['author']['login']}\n" \
            f"date:  {commit['commit']['author']['date'].replace('T', '  ')[:-4]}\n"
        return s

    def _choose_last_3_commits(self, name):
        try:
            login = MetOptRepo.team[name]
        except KeyError:
            return self._all_commits[:3]

        last_3_commits = [commit for commit in self._all_commits if commit['author']['login'] == login]
        return last_3_commits
