import openai
import os
from apiKey import openAi_key  # Assuming your API key is stored here

# Set your OpenAI API key
openai.api_key = openAi_key

# Function to get recycling information from GPT-4
def get_recycling_info(trash_item, weather):
    prompt = f"How can a {trash_item} be recycled in a creative way when the weather is {weather}? Provide specific steps or suggestions. Give your response in HTML format. Do not put html, body, title, link tag because I parsing whatever you give me to an already existing html scripts. Only create an unordered list of the recycling tips. Use the ul tag and make the list-style-type square using inline css styling. Do not include a title. Put the recylcling tips under each other, row by row, and not besides each other. Do not put escpae characters like  slash n."
    
    try:
        # Call the GPT-4 model using the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use GPT-4 model
            messages=[
                {"role": "system", "content": "You are a recycling expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,  # Adjust the token limit depending on how much detail you want
            n=1,  # We want a single response
            temperature=0.7,  # Controls randomness (higher = more creative responses)
        )

        # Extract the message from the response
        recycling_info = response['choices'][0]['message']['content']
        return recycling_info

    except Exception as e:
        return f"Error occurred: {str(e)}"

'''
# Example usage
if __name__ == "__main__":
    # Example trash items, you can modify or replace them with user input
    trash_items = ["plastic bottle", "aluminum can", "old electronics", "glass jar"]

    # Loop through each item and get recycling information
    for item in trash_items:
        print(f"\nRecycling Information for {item.capitalize()}:")
        recycling_info = get_recycling_info(item, "snowing")
        print(recycling_info)
'''