# Трейт Deref: Ведем себя как ссылка

Трейт `Deref` позволяет перегрузить оператор разыменования `*`.
Это позволяет умным указателям вести себя так же, как обычные ссылки.

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
```

Теперь мы можем писать `*y` для `MyBox`, и Rust на самом деле выполнит `*(y.deref())`.

### Deref Coercion (Приведение типов через Deref)

Это магия Rust, которая делает работу с функциями удобной.
Если функция ждет `&str`, а вы передаете `&String` (или даже `&Box<String>`), Rust автоматически вызовет `deref()` столько раз, сколько нужно.

```rust
fn hello(name: &str) {
    println!("Hello, {}!", name);
}

fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&m); // Работает! &MyBox<String> -> &String -> &str
}
```
Без этого нам пришлось бы писать: `hello(&(*m)[..])`. Бррр.

---

**JavaScript Analogy:**

> Deref Coercion — это как автоматическое приведение типов в JS, только полезное, безопасное и происходит во время компиляции.
> Например, как `toString()` вызывается неявно, так и `deref()` вызывается, чтобы "докопаться" до данных.





---

**English Joke:**

> I dereferenced a null pointer and all I got was this segmentation fault.
> (Just kidding, Rust saves you from segfaults mostly).
