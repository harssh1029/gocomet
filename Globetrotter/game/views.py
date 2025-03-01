from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from .models import Destination

@csrf_exempt
def load_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                Destination.objects.create(
                    city=item["city"],
                    country=item["country"],
                    clues=item["clues"],
                    fun_fact=item["fun_fact"],
                    trivia=item["trivia"]
                )
            return JsonResponse({"message": "Data loaded successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

# Track used destinations for a single game session
used_destinations = set()

def reset_game():
    """ Reset used destinations when a new game starts. """
    global used_destinations
    used_destinations.clear()

def get_random_destination(request):
    global used_destinations

    destinations = list(Destination.objects.all())
    if not destinations:
        return JsonResponse({"error": "No destinations available"}, status=400)

    # Reset if all destinations have been used
    if len(used_destinations) >= len(destinations):
        reset_game()

    # Filter destinations that haven't been used
    available_destinations = [d for d in destinations if f"{d.city}, {d.country}" not in used_destinations]

    if not available_destinations:
        return JsonResponse({"error": "No more unique questions available"}, status=400)

    # Select a random correct destination
    destination = random.choice(available_destinations)
    used_destinations.add(f"{destination.city}, {destination.country}")

    # Ensure at least 1 wrong option is from the same country
    same_country_options = [d for d in destinations if d != destination and d.country == destination.country]
    different_country_options = [d for d in destinations if d != destination and d.country != destination.country]

    # Fill wrong options while ensuring uniqueness
    wrong_options = set()

    # Add at least one option from the same country
    if same_country_options:
        wrong_options.add(random.choice(same_country_options))

    # Add remaining options from different countries
    while len(wrong_options) < 3 and different_country_options:
        wrong_options.add(random.choice(different_country_options))

    # Ensure exactly 3 unique wrong options
    wrong_options = list(wrong_options)[:3]

    # Final options list with correct answer included
    options = wrong_options + [destination]
    random.shuffle(options)

    return JsonResponse({
        "clues": destination.get_random_clues() if hasattr(destination, 'get_random_clues') else [],
        "options": [f"{opt.city}, {opt.country}" for opt in options],
        "correct_answer": f"{destination.city}, {destination.country}",
        "fun_fact": destination.get_random_fact() if hasattr(destination, 'get_random_fact') else ""
    })

def game_home(request):
    return render(request, 'game/index.html')
