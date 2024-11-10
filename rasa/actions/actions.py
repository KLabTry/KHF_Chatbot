import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re

class ActionFetchJobListings(Action):

    def name(self) -> Text:
        return "action_fetch_job_listings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        # Retrieve the job_title and industry slots
        job_title = tracker.get_slot('job_title')
        industry = tracker.get_slot('industry')

        # Define the API endpoint
        url = "https://www.arbeitnow.com/api/job-board-api"

        try:
            # Make the GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Check if data is present
            if 'data' in data and data['data']:
                jobs = data['data']
                # Initialize lists for prioritization
                both_matches = []
                title_matches = []
                industry_matches = []

                for job in jobs:
                    title_text = job.get('title', '').lower()
                    tags = [tag.lower() for tag in job.get('tags', [])]

                    match_title = job_title.lower() in title_text if job_title else False
                    match_industry = industry.lower() in tags if industry else False

                    if match_title and match_industry:
                        both_matches.append(job)
                    elif match_title:
                        title_matches.append(job)
                    elif match_industry:
                        industry_matches.append(job)

                # Combine the lists according to priority
                filtered_jobs = both_matches + title_matches + industry_matches

                if filtered_jobs:
                    # Initialize message
                    message_parts = []
                    for idx, job in enumerate(filtered_jobs, 1):
                        title = job.get('title', 'No title provided')
                        company = job.get('company_name', 'No company name provided')
                        location = job.get('location', 'No location provided')
                        job_url = job.get('url', 'No URL provided')
                        tags = ', '.join(job.get('tags', []))

                        # Construct the job message
                        job_message = (
                            f"Job {idx}:\n"
                            f"Title     : {title}\n"
                            f"Company   : {company}\n"
                            f"Location  : {location}\n"
                            f"Tags      : {tags}\n"
                            f"Details   : {job_url}\n"
                            "------------------------------------\n"
                        )
                        message_parts.append(job_message)

                    # Combine all job messages into one message
                    message = "".join(message_parts)
                else:
                    message = "I'm sorry, but I couldn't find any job listings matching your criteria."
            else:
                message = "No job data available from the API."

        except requests.exceptions.RequestException as e:
            message = f"An error occurred while fetching job listings: {e}"

        # Send the message to the user
        dispatcher.utter_message(text=message)

        return []
    

class ActionCurrencyExchange(Action):

    def name(self) -> Text:
        return "action_currency_exchange"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        target_currency = tracker.get_slot('target_currency')
        amount = tracker.get_slot('amount')

        if not target_currency or not amount:
            dispatcher.utter_message(text="I'm missing some information to perform the conversion.")
            return []

        try:
            # Fetch exchange rates with EUR as the base currency
            url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json"
            response = requests.get(url)
            data = response.json()

            # If primary URL fails, use fallback
            if response.status_code != 200 or 'eur' not in data:
                fallback_url = "https://latest.currency-api.pages.dev/v1/currencies/eur.json"
                response = requests.get(fallback_url)
                data = response.json()

            if response.status_code == 200 and 'eur' in data:
                rates = data['eur']

                # Convert EUR to target currency
                if target_currency.lower() in rates:
                    exchange_rate = rates[target_currency.lower()]
                    conversion_result = float(amount) * exchange_rate
                    dispatcher.utter_message(
                        text=f"{amount} EUR is equal to {conversion_result:.2f} {target_currency.upper()}."
                    )
                else:
                    dispatcher.utter_message(text=f"Unsupported target currency: {target_currency.upper()}.")
            else:
                dispatcher.utter_message(text="I couldn't retrieve the exchange rate at the moment. Please try again later.")
        except Exception as e:
            dispatcher.utter_message(text="An error occurred while fetching the exchange rate.")
            print(f"Error: {e}")

        return []
