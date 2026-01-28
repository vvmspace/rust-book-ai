# Итераторы

Паттерн "Итератор" позволяет пройтись по последовательности, не заботясь о том, как она устроена.
В Rust итераторы **ленивые** (lazy). Они ничего не делают, пока вы их не пнёте (не вызовете *consuming adapter*).

```rust
let v1 = vec![1, 2, 3];
let v1_iter = v1.iter(); // Пока ничего не происходит!

for val in v1_iter { // А вот теперь погнали
    println!("{}", val);
}
```

### Трейт Iterator

```rust
pub trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

### Методы

1.  **Consumers (Потребители):** `sum`, `collect`, `for loop`. Они сжирают итератор и выдают результат.
2.  **Adapters (Адаптеры):** `map`, `filter`, `zip`. Они меняют итератор и возвращают *новый* итератор. Они ленивые.

```rust
let v1: Vec<i32> = vec![1, 2, 3];
let v2: Vec<_> = v1.iter().map(|x| x + 1).collect();
assert_eq!(v2, vec![2, 3, 4]);
```
Без `.collect()` этот код бы ничего не сделал (и компилятор бы ругался).

---

**JavaScript Analogy:**

> Rust итераторы — это как если бы Array методы `map` и `filter` в JS были ленивыми (как Generators).
> В JS `[1,2,3].map(...).filter(...)` создает два промежуточных массива.
> В Rust это просто цепочка логики, которая выполнится за один проход, когда вы позовете `collect()`.





---

**English Joke:**

> Why did the iterator cross the road?
> To get to the next element.
