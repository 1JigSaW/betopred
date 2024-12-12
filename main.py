import os

from hltv_stats import HLTVMatch
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

match_url = "/matches/2377990/red-canids-academy-vs-players-liga-gamers-club-2024-serie-a-december-cup"
match = HLTVMatch(match_url)
stats = match.parse_analytics_center()

unique_teams = set()

for i in range(len(stats[0])):
    team = stats[0][i]['team']
    unique_teams.add(team)

unique_teams_list = list(unique_teams)
print(unique_teams_list)

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {
            "role": "system",
            "content": "You are an expert in betting on esports events. "
                       "You understand statistics, analyze them perfectly, and can predict the outcome of any esports "
                       "event with flawless accuracy."
        },
        {
            "role": "user",
            "content": f"You must predict the outcome of this match {unique_teams_list} with the following statistics {stats}."
                       "You need to provide the event result and the exact score of the match."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "prediction_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "winner": {
                        "description": "Write the name of the team that will win the match",
                        "type": "string",
                    },
                    "exact_score": {
                        "description": "Write the exact score of the match",
                        "type": "string",
                    }
                }
            }
        }
    }
)

print(response.choices[0].message.content)