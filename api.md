## API一覧
説明|メゾット|エンドポイント
ユーザ登録 | POST |Signup
つながり登録 | POST |Connection
一覧表示 | GET |all

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
```
