from datetime import datetime
import requests as req


response = req.get(f'https://evo-integracao.w12app.com.br/api/v1/members/1784',
        headers={
            "username":"PRIMAXFITNESS",
            "password":"0E2C8476-A2B2-44E2-B260-F35F24BC81CD",
            "Authorization":"Basic UFJJTUFYRklUTkVTUzowRTJDODQ3Ni1BMkIyLTQ0RTItQjI2MC1GMzVGMjRCQzgxQ0Q="
            }
    )


json_response = response.json()

contacts = json_response['contacts']

# print(json_response['memberships'])
def less_days_than_today(number):
    today = datetime.date(datetime.now())

    days_before = today.day - number

    old_day = today.replace(day=days_before)

    return old_day


five_day_beore = less_days_than_today(5)

print(five_day_beore)