## エンドポイント
- http://localhost:8000/api/connection
- http://localhost:8000/api/signup
- http://localhost:8000/api/all


## API一覧
説明|メゾット|エンドポイント
 -- | -- | -- 
ユーザ登録 | POST |/Signup
つながり登録 | POST |/Connection
一覧表示 | GET |/All
都道府県ごと表示 | POST | /UserbyPrefecture
ユーザごと表示 | POST| /ConnectionbyUser


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
   userId: userid,
   userName: userName,
   prefectureId: prefecture_id,
}
```
**レスポンス400応答**
```
{}
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
> Connection[i][j]はprefectureIdがiとjのつながりの個数を表している

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
    },
   ],
 }
 ```
フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
users|array|true|クエリで与えられた都道府県に住むユーザ情報の配列（user_idで昇順）
userId|string|true|ユーザID
userName|string|true|ユーザ名

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
    ]
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
    ]
   ],
 }
 ```
  フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
offlineConnections|array|true|オフラインのつながりの配列（47）
onlineConnections|array|true|オンラインのつながりの配列（47）
offlineConnections|array|true|オフラインで繋がっているユーザ情報の配列（47）
onlineConnections|array|true|オンラインで繋がっているユーザ情報の配列（47）
> Connections[i]は指定されたユーザとid = i の都道府県の人とのつながりの個数を表している

**レスポンス400応答**
```
{
}
```
