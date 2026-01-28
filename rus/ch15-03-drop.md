# Трейт Drop: Уборка мусора

Трейт `Drop` позволяет настроить код, который выполняется, когда переменная выходит из области видимости (scope).
Это аналог деструкторов в C++.

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}
```

Rust вызывает `drop` автоматически. Вы **не можете** вызвать его вручную (`x.drop()`).
Если вам нужно убить переменную раньше времени (например, освободить лок), используйте `std::mem::drop(x)`.

```rust
fn main() {
    let c = CustomSmartPointer { data: String::from("some data") };
    drop(c); // Явный дроп
    println!("CustomSmartPointer dropped before the end of main.");
}
```

---

**JavaScript Analogy:**

> В JS нет деструкторов, потому что есть Garbage Collector. Но иногда мы пишем методы типа `close()` или `disconnect()` для баз данных или сокетов.
> В Rust `drop` — это автоматический `close()`, который нельзя забыть вызвать.





---

**English Joke:**

> Rust: The only language where dropping something is good.
