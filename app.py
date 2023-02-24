from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/api/comments/search', methods=['GET'])
def search_comments():
    response = requests.get('https://dev.ylytic.com/ylytic/test')
    json_data = response.json()
    comments = json_data['comments']

    # Get the search parameters from the query string
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    # Filter the comments based on the search parameters
    filtered_comments = []
    for comment in comments:
        # Filter by author name
        if search_author and search_author.lower() not in comment['author'].lower():
            continue
        # Filter by date range
        if at_from:
            if datetime.fromisoformat(comment['at']) < datetime.fromisoformat(at_from):
                continue
        if at_to:
            if datetime.fromisoformat(comment['at']) > datetime.fromisoformat(at_to):
                continue
        # Filter by like and reply counts
        if like_from:
            if comment['like'] < int(like_from):
                continue
        if like_to:
            if comment['like'] > int(like_to):
                continue
        if reply_from:
            if comment['reply'] < int(reply_from):
                continue
        if reply_to:
            if comment['reply'] > int(reply_to):
                continue
        # Filter by text search
        if search_text and search_text.lower() not in comment['text'].lower():
            continue
        # If all filters pass, add the comment to the results
        filtered_comments.append(comment)

    # Return the filtered comments
    return jsonify(filtered_comments)

if __name__ == '__main__':
    app.run(debug=True)
