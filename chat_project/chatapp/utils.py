# chatapp/utils.py
import json

def get_suggested_friends(user_id, json_data, num_recommendations=5):
    # Load the JSON data
    user_data = json.loads(json_data)
    
    # Get the user's data
    user = None
    for user_info in user_data['users']:
        if user_info['id'] == user_id:
            user = user_info
            break
    
    if user is None:
        return []
    
    # Define a similarity score function (you can customize this)
    def similarity_score(user1, user2):
        score = 0
        for interest, preference in user1['interests'].items():
            if interest in user2['interests']:
                score += abs(preference - user2['interests'][interest])
        return score

    # Sort users by similarity score and select the top N recommendations
    suggested_friends = sorted(user_data['users'], key=lambda u: similarity_score(user, u))
    suggested_friends = suggested_friends[:num_recommendations]

    return suggested_friends
