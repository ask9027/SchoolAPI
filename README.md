# SchoolAPI

## Setup for `.env`

```env
database_url=postgresql+psycopg2://username:password@127.0.0.1:5432/dbName
secret_key=key
algorithm=HS256
access_token_expire_weeks=1
```

## Setup alembin
```
alembin upgrade head
```

## RUN uvicorn
```
uvicorn main:app --reload
```
