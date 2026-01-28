# Трейты: Определение общего поведения

**Трейт (Trait)** — это интерфейс. Он говорит: "Этот тип умеет делать вот это".

### Определение трейта

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}
```
Любой, кто реализует `Summary`, обязан иметь метод `summarize`, который возвращает `String`.

### Реализация трейта

```rust
pub struct NewsArticle {
    pub headline: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by ...", self.headline)
    }
}
```

### Трейты как параметры

Мы можем принимать не конретный тип, а "что-то, что умеет Summary".

```rust
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}
```
Это синтаксический сахар для **Trait Bound** (ограничение трейтом):

```rust
pub fn notify<T: Summary>(item: &T) { ... }
```

Можно требовать несколько трейтов сразу:
```rust
fn notify(item: &(impl Summary + Display)) { ... }
```
Или использовать `where` для читаемости:
```rust
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{ ... }
```

### Возврат типов, реализующих трейт

```rust
fn returns_summarizable() -> impl Summary { ... }
```
Это работает **только если вы возвращаете один конкретный тип**. Нельзя вернуть "или NewsArticle, или Tweet". Для этого нужны Trait Objects (Глава 17).

---

**Анекдот:**

> Утка заходит в бар.
> Бармен: "Эй, мы тут не обслуживаем типа `Duck`!"
> Утка: "А я не `Duck`, я `impl Quack + Walk + Swim`. Пропустите, у меня `where` clause проходит."
