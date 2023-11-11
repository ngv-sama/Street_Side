from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

def preprocess_itinerary(itinerary_text):
    # Split the itinerary text into paragraphs based on day-wise information
    # You can customize this logic based on the actual structure of your itinerary text
    paragraphs = itinerary_text.split('\n')  # Assuming each day is separated by a new line
    return paragraphs


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        age = request.form.get('age')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        dietary_restrictions = request.form.get('dietary')
        budget = request.form.get('budget')
        starting_location = request.form.get('location')
        destination = request.form.get('destination')
        preferences=request.form.get('preferences')
        temp=request.form.get('temp')

        # Generate itinerary using OpenAI API
        itinerary_text = generate_itinerary(name, age, start_date, end_date, dietary_restrictions, budget, starting_location, destination, preferences, temp)

        if itinerary_text is None:
            # Handle error
            return render_template('error.html')

        itinerary_paragraphs = preprocess_itinerary(itinerary_text)

        # Pass user details and preprocessed itinerary paragraphs to the template
        return render_template('itinerary.html', name=name, age=age, start_date=start_date, end_date=end_date,
                               dietary_restrictions=dietary_restrictions, budget=budget,
                               starting_location=starting_location, destination=destination,
                               itinerary_paragraphs=itinerary_paragraphs)

    return render_template('index.html')

def generate_itinerary(name, age, start_date, end_date, dietary_restrictions, budget, starting_location, destination, preferences, temp):
    # Create a prompt for the OpenAI API
    spec=int(temp)/10
    prompt = f"A traveler named {name}, aged {age}, is planning a trip from {starting_location} to {destination}. They are available to travel from {start_date} to {end_date}. They have a budget of {budget} and have the following dietary restrictions: {dietary_restrictions}. They have special preferences for the trip as well: {preferences} Please generate a detailed itinerary for their trip."

    try:
        # Call OpenAI API to generate itinerary
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=spec
        )
        # Extract the itinerary from the response
        itinerary_text = response['choices'][0]['text']
        print(itinerary_text)
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None

    return itinerary_text

def get_weather_data(location, start_date, end_date):
    # Call OpenWeatherMap API to get weather data
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast/daily?q={location}&appid=your-openweathermap-api-key&start={start_date}&end={end_date}')
    weather_data = response.json()

    return weather_data

def get_map_data(location):
    # Call OpenStreetMap API to get map data
    response = requests.get(f'https://nominatim.openstreetmap.org/search?city={location}&format=json')
    map_data = response.json()

    return map_data

if __name__ == '__main__':
    app.run(debug=True)
