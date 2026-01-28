# `RefCell<T>` и Внутренняя Мутабельность (Interior Mutability)

**Внутренняя мутабельность** — это паттерн, разрешающий изменять данные внутри иммутабельной структуры.
Это немного "обман" правил Rust, но обман легальный, потому что проверки переносятся с этапа компиляции на этап исполнения (runtime).

`RefCell<T>` позволяет делать это.

### Правила заимствования
*   Компайл-тайм (обычные ссылки): нарушение = ошибка компиляции.
*   Рантайм (`RefCell<T>`): нарушение = `panic!`.

### Зачем это нужно?
Например, для Mock-объектов в тестах. У вас есть иммутабельный интерфейс `Messenger`, но внутри мока вы хотите накапливать отправленные сообщения.

```rust
pub trait Messenger {
    fn send(&self, msg: &str); // &self иммутабелен!
}

struct MockMessenger {
    sent_messages: RefCell<Vec<String>>,
}

impl Messenger for MockMessenger {
    fn send(&self, message: &str) {
        // Мы берем мутабельную ссылку на вектор внутри иммутабельного self!
        self.sent_messages.borrow_mut().push(String::from(message));
    }
}
```

### Сочетание `Rc<T>` и `RefCell<T>`
Это комбо позволяет иметь **несколько владельцев** и при этом **изменять** данные.

```rust
let value = Rc::new(RefCell::new(5));
let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));
*value.borrow_mut() += 10;
```

---

**JavaScript Analogy:**

> В JS `const obj = { x: 1 };` запрещает менять саму ссылку `obj`, но разрешает менять `obj.x = 2`.
> `RefCell` похож на это: внешне структура неизменна, но внутри кипит мутабельная жизнь.





---

**English Joke:**

> Interior mutability is like cheating on your diet.
> It's fine as long as nobody sees you (at compile time).
