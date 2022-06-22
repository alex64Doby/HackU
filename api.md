## エンドポイント
- http://localhost:8000/api/signup
- http://localhost:8000/api/signin
- http://localhost:8000/api/connection
- http://localhost:8000/api/all
- http://localhost:8000/api/userByPrefecture
- http://localhost:8000/api/connectionByUser
- http://localhost:8000/api/serachUser

## API一覧
説明|メゾット|エンドポイント
 -- | -- | --
ユーザ登録 | POST |/Signup
ログイン | POST |/Signin
つながり登録 | POST |/Connection
一覧表示 | GET |/All
都道府県ごとのユーザ表示 | POST | /UserbyPrefecture
ユーザごとのつながり表示 | POST | /ConnectionbyUser
ユーザの検索 | POST | /searchUser


## 各APIの仕様

### ユーザ登録 /Signup
ユーザ情報を登録するAPI

**リクエスト**
```
 {
   userId: userid,
   userName: userName,
   prefectureId: prefecture_id,
 }
 ```

 ```
 POST /Signup
 ```

 フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
userId|string|true|ユーザID
userName|string|true|ユーザの名前
prefectureId|number|true|都道府県ID

**レスポンス200応答**
```
{
  status: 200,
}
```
**レスポンス400応答**
```
{
  status: 400,
}
```


### ユーザ登録 /Signin
ログインするAPI

**リクエスト**
```
 {
   userId: userid,
 }
 ```

 ```
 POST /Signin
 ```

 フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
userId|string|true|ユーザID

**レスポンス200応答**
```
{
  status: 200,
}
```
**レスポンス400応答**
```
{
  status: 400,
}
```



### つながり登録 /Connection
ユーザ間のつながりを登録するAPI

**リクエスト**
```
 {
   userId1: userid1,
   userId2: userid2,
   status:status,
 }
 ```

 ```
 POST /Connection
 ```

 フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
userId1|string|true|ユーザID1
userId2|string|true|ユーザID2

**レスポンス200応答**
```
 {
   userId1: userid1,
   userId2: userid2,
 }
 ```
**レスポンス400応答**
```
{}
```

### 一覧表示 /All
**レスポンス200応答**
```
 {
   offlineConnections:
   [
    [0, 1, 0, 4,...],
    [0, 2, 3, 4,...],
   ],
  onlineConnections:
  [
   [0, 1, 0, 4,...],
   [0, 2, 3, 4,...],
  ],
 }
 ```
 フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
offlineConnections|array|true|オフラインのつながりの配列（47×47）
onlineConnections|array|true|オンラインのつながりの配列（47×47）
>prefectureId = i,jの都道府県に住むユーザの人数をM, Nとすると
>  Connection[i][j]はprefectureIdがiとjのつながりの個数（をMNで割った値）を表している

## 特定の都道府県のユーザ表示 /UserbyPrefecture
特定の都道府県のユーザを表示するAPI

**リクエスト**
```
 {
   prefectureId: id,
 }
 ```
  フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
prefectureId|string|true|都道府県ID


 **レスポンス200応答**
 ```
 {
   users:
   [
    {
     userId: userid,
     userName: user_name,
     prefectureId: prefecture_id,
    },
   ],
 }
 ```
フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
users|array|true|クエリで与えられた都道府県に住むユーザ情報の配列
userId|string|true|ユーザID
userName|string|true|ユーザ名
prefecture_id|string|true|都道府県ID

**レスポンス400応答**
 ```
 {
 }
 ```
 ## 特定のユーザのつながりを表示 /ConnectionByUser
 **リクエスト**
```
 {
   userId:user_id
 }
 ```
   フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
userId|string|true|ユーザID

  **レスポンス200応答**
 ```
 {
   offline_connections:
   [0, 1, 0, 4,...]

   obline_connections:
   [0, 1, 0, 4,...],

   offline_connections_detail:
   [
    [
     { userId: userid,
       userName: username,
     },
     { userId: userid,
       userName: username,
     },
    ],
   ],
   online_connections_detail:
   [
    [
     { userId: userid,
       userName: username,
     },
     { userId: userid,
       userName: username,
     },
    ],
   ],
 }
 ```
  フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
offlineConnections|array|true|オフラインのつながりの配列（47）
onlineConnections|array|true|オンラインのつながりの配列（47）
offlineConnections|array|true|オフラインで繋がっているユーザ情報の配列（47）
onlineConnections|array|true|オンラインで繋がっているユーザ情報の配列（47）
> prefectureId = iの都道府県のユーザ数をNとすると
> Connections[i]は指定されたユーザとid = i の都道府県の人とのつながりの個数を（Nで割った値を）表している

**レスポンス400応答**
```
{
}
```

## ユーザの検索 /searchUser
ユーザIDのキーワードとユーザ名のキーワードをもとに、
部分一致するユーザ情報を返す
（都道府県idが与えられた場合は、
都道府県で絞り込みをする）

**リクエスト**

```
 { 
  userIdKey: "ユーザIDのキーワード",
  userNameKey:  "ユーザ名のキーワード",
  prefectureId: 都道府県ID,
 }
```
フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
userIdKey|string|false|ユーザIDのキーワード
userNameKey|string|false|ユーザ名のキーワード
prefectureId|string|false|都道府県ID
**レスポンス200応答**

```
{
 users:
 [
  { userId: ユーザID,
    userName: ユーザ名,
    prefecture_id: 都道府県ID,
  }, 
  { userId: ユーザID,
    userName: ユーザ名,
    prefecture_id: 都道府県ID,
  }, 
 ]
}
```
**レスポンス400応答**

```
{
}
 ```
フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
users|array|true|クエリで与えられた都道府県に住むユーザ情報の配列
userId|string|true|ユーザID
userName|string|true|ユーザ名
prefecture_id|string|true|都道府県ID
