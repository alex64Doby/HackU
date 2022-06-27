## エンドポイント
- http://localhost:8000/api/signup
- http://localhost:8000/api/signin
- http://localhost:8000/api/connection
- http://localhost:8000/api/all
- http://localhost:8000/api/userByPrefecture
- http://localhost:8000/api/connectionByUser
- http://localhost:8000/api/searchUser
- http://localhost:8000/api/searchUserByUserIdExactly
- http://locahost:8000/api/searchConnection
- http://locahost:8000/api/ranking

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
つながりの検索　| POST | /searchConnection
ランキング表示 | GET |/ranking

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

## ユーザ検索（ID完全一致）/searchUserByUserIdExactly
与えられたuserIdKeyをもとに完全一致するユーザの情報を返す。
**リクエスト**

```
 {
  userIdKey: "ユーザID",
 }
```
フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
userIdKey|string|false|ユーザID

**レスポンス200応答**

```
{
 users:
 [
  { userId: ユーザID,
    userName: ユーザ名,
    prefecture_id: 都道府県ID,
  }
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


## つながりの検索 /searchConnection
与えられたuserId1Key, userID2Key（完全一致）, pointGreaterThan, pointLessThanによって
ユーザとポイントによる絞り込みができる。（時間での絞り込みは未実装）

**リクエスト**
```
{
 userId1Key: user_id,
 userId2Key: user_id,
 pointGreaterThan: ポイントの下限値（含まない）,
 pointLessThan: ポイントの上限値（含まない）,
}
```
フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
 userId1Key | String | false | 検索したいユーザID1
 userId2Key | String | false | 検索したいユーザID2
 pointGreaterThan | Number | false | ポイントの下限値
 pointLessThan | Number | false | ポイントの上限値

 **レスポンス**
 ```
 {
  connections:
  [
   { connectionId: connection_id,
     userId1: user_id1,
     userId2: user_id2,
     createdBy: 作成日時,
     updatedBy: 更新日時,
     point: ポイント,
   }
  ]
 }
 ```

フィールド名 | 型 | 必須 | 説明
 -- | -- | -- | --
 connectionId | String | true | コネクション ID
 userId1 | String | true | ユーザID
 userId2 | String | true |　ユーザID
 createdBy | DATETIME | true | 作成日時
 updatedBy | DATETIME | true | 更新日時
 point | Number | true | ポイント

### ランキング表示 /ranking
**レスポンス200応答**
```
{
ranking:
[
 {
   userId: user_id,
   userName: user_name,
   prefectureId: prefecture_id,
   point: user_point
  },
  ,,,
 ]
}
```
フィールド名 | 型 | 必須 | 説明
-- | -- | -- | --
ranking|array|true|ランキング順のユーザ情報の配列
userId|string|true|ユーザID
userName|string|true|ユーザ名
prefecture_id|string|true|都道府県ID
point|int|true|ユーザの所有ポイント
>ランキングの上位10人のユーザ情報を取得．
>リクエスト毎にデータベースから取り出してソートする．（point=0の人は除外）
>毎回 O(n log n)かかるがデータ数が数百程度を想定しているため問題なさそう．
