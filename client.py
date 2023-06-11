import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
    #     print("create")
    #     response = await session.post(
    #         "http://127.0.0.1:8080/users/", json={"name": "user_5", "password": "12345"}
    #     )
    #     print(response.status)
    #     json_data = await response.json()
    #     print(json_data)

        # print("get")
        # response = await session.get(
        #     "http://127.0.0.1:8080/users/20",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("patch")
        # response = await session.patch(
        #     "http://127.0.0.1:8080/users/20", json={"name": "user_22"}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("get")
        # response = await session.get(
        #     "http://127.0.0.1:8080/users/20",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("delete")
        # response = await session.delete(
        #     "http://127.0.0.1:8080/users/1",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("get")
        # response = await session.get(
        #     "http://127.0.0.1:8080/users/20",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("create")
        # response = await session.post(
        #     "http://127.0.0.1:8080/ads/", 
        #     headers={"name": 'user_5', 'password': '12345'}, 
        #     json={"title": 'my_ads', 'description': 'My Best Ads'}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)   

        # print("get")
        # response = await session.get(
        #     "http://127.0.0.1:8080/ads/1",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("patch")
        # response = await session.patch(
        #     "http://127.0.0.1:8080/ads/1", 
        #     headers={"name": 'user_5', 'password': '12345'}, 
        #     json={"title": 'funny_ads', 'description': 'My Best Ads'}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("get")
        # response = await session.get(
        #     "http://127.0.0.1:8080/ads/1",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("delete")
        # response = await session.delete(
        #     "http://127.0.0.1:8080/ads/1",
        #     headers={"name": 'user_5', 'password': '12345'}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        print("get")
        response = await session.get(
            "http://127.0.0.1:8080/ads/1",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)

asyncio.run(main())