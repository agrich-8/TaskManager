# TaskManager

После развертывания проекта можно воспользоваться документацией swagger по ссылке http://127.0.0.1:8000/docs

На данный момент endpoint http://127.0.0.1:8000/user принимает post запрос по указанной ссылке, имея тело запроса (по умолчанию):
```JSON
{
  "id": 0,
  "name": "string",
  "password": "string",
  "description": "string"
}
```
Ответ сервера:
```JSON
{
  "id": 0,
  "name": "string",
  "password": "string",
  "description": "string",
  "passlen": 6
}
```
  - добавляется passlen - длина пароля. При этом длина пароля должна быть не менее 6 символов, иначе с кодом ошибки 422 вернется:
 ```JSON
{
  "detail": [
    {
      "loc": [
        "body",
        "password"
      ],
      "msg": "ensure this value has at least 6 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {
        "limit_value": 6
      }
    }
  ]
}
```
