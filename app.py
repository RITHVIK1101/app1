import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)

# Define the URL of the webpage
website_url = "https://www.wolvesfootball.com/roster/varsity"

# Send a GET request to the webpage
response = requests.get(website_url)

# Parse the HTML content of the webpage using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all player information sections with class 'list-item'
player_infos = soup.find_all('li', class_='list-item')

# Create a dictionary to store player information
players_data = {}

# Iterate through the player information sections
for player_info in player_infos:
    # Extract player name, grade, position, height, and weight
    player_name = player_info.find('h2', class_='list-item-content__title').text.strip()
    details = player_info.find('p', class_='').text.strip().split('|')
    grade = details[0].strip()
    position = details[1].strip()
    height = details[2].strip()
    weight = details[3].strip()

    # Store player information in the dictionary
    players_data[player_name] = {
        "Grade": grade,
        "Position": position,
        "Height": height,
        "Weight": weight
    }

# Define a route for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    intent = data['queryResult']['intent']['displayName']
    
    if intent == 'GetPlayerInfo':
        player_name = data['queryResult']['parameters']['player']
        if player_name in players_data:
            player_info = players_data[player_name]
            response_text = f"Player Name: {player_name}\nGrade: {player_info['Grade']}\nPosition: {player_info['Position']}\nHeight: {player_info['Height']}\nWeight: {player_info['Weight']}"
        else:
            response_text = "Sorry, I couldn't find information for that player."
    else:
        response_text = "Sorry, I couldn't understand your request."

    response = {
        "fulfillmentText": response_text
    }

    return response

if __name__ == '__main__':
    app.run(debug=True)
