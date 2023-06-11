import json
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from auth import hash_password, check_password
from models import Base, engine, Session, User, Ads

app = web.Application()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


async def get_user(session: Session, user_id: int):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({"error": "user not found"}),
            content_type="application/json",
        )
    return user

async def get_ads(session: Session, ads_id: int):
    ads = await session.get(Ads, ads_id)
    if ads is None:
        raise web.HTTPNotFound(
            text=json.dumps({"error": "ads not found"}),
            content_type="application/json",
        )
    return ads


class UserView(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])
    
    async def get(self):
            user = await get_user(self.session, self.user_id)
            return web.json_response(
                {
                    "id": user.id,
                    "name": user.name,
                    "creation_time": int(user.creation_time.timestamp()),
                }
            )

    async def post(self):
        json_data = await self.request.json()
        json_data["password"] = hash_password(json_data["password"])
        new_user = User(**json_data)
        try:
            self.session.add(new_user)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "user already exists"}),
                content_type="application/json",
            )
        return web.json_response({"id": new_user.id})

    async def patch(self):
        json_data = await self.request.json()
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = await get_user(self.session, self.user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        try:
            self.session.add(user)    
            self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "user already exists"}),
                content_type="application/json",
            )
        return web.json_response({"id": user.id})

    async def delete(self):
        user = await get_user(self.session, self.user_id)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"id": user.id})
    

class AdsView(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def ads_id(self):
        return int(self.request.match_info["ads_id"])    

    async def get(self):
        ads = await get_ads(self.session, self.ads_id)
        return web.json_response(
            {
                "id": ads.id,
                "title": ads.title,
                "description": ads.description,
                "creation_time": int(ads.creation_time.timestamp()),
                "user_id": ads.user_id
            }
        )
    async def post(self):
        user_data = self.request.headers
        ads_data = await self.request.json()
        check_pass = user_data["password"]
        user = await self.session.execute(select(User).where(User.name == user_data["name"]))
        user_models = (user.mappings().all())[0].get(User)
        right_pass = user_models.password
        if user == []:
            raise web.HTTPNotFound(
                text=json.dumps({"error": "user not found"}),
                content_type="application/json",
            )
        else:
            if check_password(right_pass, check_pass) is True:
                ads_data.update({"user_id": user_models.id})
                new_ads = Ads(**ads_data)
                self.session.add(new_ads)
                await self.session.commit()
                return web.json_response({"id": new_ads.id})
            else:
                raise web.HTTPUnauthorized(
                    text=json.dumps({"error": "wrong password"}),
                    content_type="application/json",
                )
    async def patch(self):
        user_data = self.request.headers
        ads_data = await self.request.json()
        check_pass = user_data["password"]
        user = await self.session.execute(select(User).where(User.name == user_data["name"]))
        user_models = (user.mappings().all())[0].get(User)
        right_pass = user_models.password
        if user == []:
            raise web.HTTPNotFound(
                text=json.dumps({"error": "user not found"}),
                content_type="application/json",
            )
        else:
            if check_password(right_pass, check_pass) is True:
                ads = await get_ads(self.session, self.ads_id)
                if ads.user_id == user_models.id:
                    ads_data.update({"user_id": user_models.id})
                    for field, value in ads_data.items():
                        setattr(ads, field, value)
                        self.session.add(ads)
                    new_ads = Ads(**ads_data)
                    self.session.add(new_ads)
                    await self.session.commit()
                    return web.json_response({"id": ads.id, "name": ads.title})
                else:
                    raise web.HTTPConflict(
                        text=json.dumps({"error": "user has not access"}),
                        content_type="application/json",
                    )
            else:
                raise web.HTTPUnauthorized(
                    text=json.dumps({"error": "wrong password"}),
                    content_type="application/json",
                )

    async def delete(self):
        user_data = self.request.headers
        check_pass = user_data["password"]
        user = await self.session.execute(select(User).where(User.name == user_data["name"]))
        user_models = (user.mappings().all())[0].get(User)
        right_pass = user_models.password
        if user == []:
            raise web.HTTPNotFound(
                text=json.dumps({"error": "user not found"}),
                content_type="application/json",
            )
        else:
            if check_password(right_pass, check_pass) is True:
                ads = await get_ads(self.session, self.ads_id)
                if ads.user_id == user_models.id:
                    await self.session.delete(ads)
                    await self.session.commit()
                    return web.json_response({"status": "deleted"})
                else:
                    raise web.HTTPConflict(
                        text=json.dumps({"error": "user has not access"}),
                        content_type="application/json",
                    )
            else:
                raise web.HTTPUnauthorized(
                    text=json.dumps({"error": "wrong password"}),
                    content_type="application/json",
                )

async def orm_context(app: web.Application):
    print("START")
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    print("SHUT DOWN")
    await engine.dispose()

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)  

app.add_routes(
    [
        web.post("/users/", UserView),
        web.get("/users/{user_id:\d+}", UserView),
        web.patch("/users/{user_id:\d+}", UserView),
        web.delete("/users/{user_id:\d+}", UserView),
        web.post("/ads/", AdsView),
        web.get("/ads/{ads_id:\d+}", AdsView),
        web.patch("/ads/{ads_id:\d+}", AdsView),
        web.delete("/ads/{ads_id:\d+}", AdsView),
    ]
)

if __name__ == "__main__":
    web.run_app(app)