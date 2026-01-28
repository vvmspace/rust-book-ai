# Определение и создание экземпляров структур

Структуры похожи на кортежи, но у каждого поля есть имя. Больше не нужно запоминать, что `tup.0` — это имя, а `tup.1` — фамилия.

### Определение

```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}
```

Чтобы создать экземпляр (инстанс):

```rust
let user1 = User {
    email: String::from("someone@example.com"),
    username: String::from("someusername123"),
    active: true,
    sign_in_count: 1,
};
```

Порядок полей не важен. Главное — заполнить все.

Чтобы достать значение: `user1.email`.
Чтобы изменить (если переменная `mut`): `user1.email = String::from(...)`.

**ВАЖНО:** Нельзя сделать мутабельным только одно поле. Или вся структура `mut`, или ничего.

### Сокращенная инициализация (Field Init Shorthand)

Если имя переменной совпадает с именем поля, можно не писать дважды.

```rust
fn build_user(email: String, username: String) -> User {
    User {
        email, // Вместо email: email
        username,
        active: true,
        sign_in_count: 1,
    }
}
```

### Синтаксис обновления (Struct Update Syntax)

Хотите создать нового юзера на основе старого, изменив только email? Легко.

```rust
let user2 = User {
    email: String::from("another@example.com"),
    ..user1
};
```
Синтаксис `..user1` говорит: "Остальные поля возьми из user1".
**Осторожно!** Это перемещает (Move) данные. Если `user1.username` было `String`, оно переедет в `user2`, и `user1` станет невалидным (частично).

### Кортежные структуры (Tuple Structs)

Это когда лень придумывать имена полям, но нужен отдельный тип.

```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

let black = Color(0, 0, 0);
let origin = Point(0, 0, 0);
```

Хоть внутри одно и то же, `Color` и `Point` — разные типы. Функцию, ждущую `Color`, нельзя обмануть, подсунув `Point`.

### Unit-подобные структуры

Структуры без полей.
```rust
struct AlwaysEqual;
let subject = AlwaysEqual;
```
Полезны для трейтов (глава 10), когда данные не нужны, а поведение нужно.

---

**Анекдот:**

> Объявление:
> "Продам структуру `House`.
> Поля:
> `doors: 2`,
> `windows: 4`,
> `roof: leaked`.
> Самовывоз (Move). `Copy` не поддерживается, дом уникальный."
