import aiohttp
import asyncio
import json

async def ask_model(question: str):
    url = "http://localhost:5039/api/model/ask"  # כתובת ה-API של השרת ב-ASP.NET

    # יצירת גוף הבקשה
    data = {
        "question": question
    }

    # שליחת הבקשה בצורה אסינכרונית
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                # קבלת התשובה מהמודל
                print(response)
                response_data = await response.json()
                print(response_data)
                print("תשובת המודל:", response_data.get('answer'))
            else:
                print(f"שגיאה: {response.status} - לא ניתן לקבל תשובה מהמודל.")

# פונקציה לקרוא שאלות ולשלוח בקשות בצורה אסינכרונית
async def main():
    question = "how much is 2 + 2?"
    await ask_model(question)

# הרצת הפונקציה
asyncio.run(main())
