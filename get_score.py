import requests
from concurrent.futures import ThreadPoolExecutor

class get_score(object):
    def __init__(self, league_id = 322239):
        self.league_id = league_id

    def get_data(self):
        # Get team IDs and names
        url = f"https://fantasy.premierleague.com/api/leagues-classic/{self.league_id}/standings"
        response = requests.get(url)
        data = response.json()
        data = data['standings']['results']
        selected_params = ['entry', 'entry_name']
        info = [{param: data[i][param] for param in selected_params} for i in range(len(data))]

        # Get scores for each team in parallel
        with ThreadPoolExecutor() as executor:
            scores = list(executor.map(self.get_team_score, [item['entry'] for item in info]))

        # Add scores to the info dictionary
        for i, score in enumerate(scores):
            info[i]['score'] = score

        return info

    def get_team_score(self, team_id):
        url = f"https://fantasy.premierleague.com/api/entry/{team_id}/history"
        response = requests.get(url)
        data = response.json()['current']
        n_week = len(data)
        score = []
        for j in range(n_week):
            if j == 0:
                score.append(data[j]['total_points'])
            else:
                score.append(data[j]['total_points'] - data[j-1]['total_points'])
        return score