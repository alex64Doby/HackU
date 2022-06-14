## API一覧
説明|メゾット|エンドポイント
 -- | -- | -- 
ユーザ登録 | POST |/Signup
つながり登録 | POST |/Connection
一覧表示 | GET |/All

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
prefectureId|string|true|都道府県ID

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
> connection[i][j]はprefectureIdがiとjのつながりの個数を表している
