import requests
import random
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()
url = "https://api.notion.com/v1/search"
data = {
  "filter": {
    "value": "page",
    "property": "object"
  }
}
headers = {
    "Authorization": "Bearer " + os.getenv("API_KEY"),
    "Notion-Version": "2022-06-28"
}
send_email = os.getenv("SEND_EMAIL")


def main():
    try:
      response = requests.post(url, json=data, headers=headers)
      results = response.json()['results']

      while response.json()['has_more']:
        next_cursor = response.json()['next_cursor']
        data["start_cursor"] = next_cursor
        response = requests.post(url, json=data, headers=headers)
        results.extend(response.json()['results'])

      print("Number of pages returned:" + str(len(results)))
      random_page = random.choice(results)
      print("Link to random page: " + random_page['url'])

      if send_email == "true": 
        try:
          yag = yagmail.SMTP(os.getenv("EMAIL_RECIPIENT"), os.getenv("GMAIL_APP_PASSWORD"))
          yag.send(
            to=os.getenv("EMAIL_RECIPIENT"),
            subject="Your daily random notion page",
            contents=random_page['url']
          )
          print("E-Mail successfully sent")
        except:
          print("Error while sending E-Mail")
    except:
       print("Error while getting random page")

if __name__ == "__main__":
    main()