# Ключевое слово `use`

Писать полные пути (`crate::front_of_house::hosting::add_to_waitlist`) — это путь к туннельному синдрому.
Используйте `use`, чтобы создать шорткат.

```rust
use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
    hosting::add_to_waitlist();
}
```

Это как создать симлинк в файловой системе.

### Идиоматичный `use`

Для функций: заносим в скоуп **родительский модуль**.
```rust
use crate::front_of_house::hosting;
hosting::add_to_waitlist(); // Видно, что функция не местная
```

Для структур и энамов: заносим в скоуп **сам тип**.
```rust
use std::collections::HashMap;
let mut map = HashMap::new();
```

Исключение: если имена совпадают. Тогда используем родителей или `as`.

```rust
use std::fmt::Result;
use std::io::Result as IoResult; // as спасает ситуацию
```

### `pub use`: Ре-экспорт

Если вы хотите, чтобы ваши пользователи могли использовать ваши зависимости как свои:

```rust
pub use crate::front_of_house::hosting;
```

Теперь внешний код может обращаться к `hosting` прямо через ваш корень, не зная о внутренней структуре. Это называется ре-экспорт.

### Использование внешних пакетов

В `Cargo.toml`:
```toml
rand = "0.8.3"
```

В коде:
```rust
use rand::Rng;
```
Cargo скачает магию из crates.io, и вы великолепны.

---

**Анекдот:**

> Программист на Rust заполняет декларацию:  
> — Место жительства?  
> — `use std::env::home_dir;`  
> — Нет, реальный адрес.  
> — А, тогда `crate::earth::params::address`... хотя нет, давайте я просто `pub use` квартиру родителей.
