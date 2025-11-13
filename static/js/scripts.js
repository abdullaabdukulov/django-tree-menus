document.addEventListener('DOMContentLoaded', function() {
    // Находим все элементы меню с детьми
    const menuContainers = document.querySelectorAll('.menu-container');

    menuContainers.forEach(container => {
        // Добавляем обработчики клика для всех ссылок
        const allLinks = container.querySelectorAll('a');

        allLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const li = this.parentElement;
                const childUl = li.querySelector(':scope > ul');

                // Если у элемента есть дети
                if (childUl) {
                    // Предотвращаем переход по ссылке
                    e.preventDefault();

                    // Переключаем видимость
                    if (li.classList.contains('expanded')) {
                        li.classList.remove('expanded');
                        childUl.style.display = 'none';
                    } else {
                        li.classList.add('expanded');
                        childUl.style.display = 'block';
                    }
                }
                // Если детей нет, ссылка работает как обычно (переход по URL)
            });
        });
    });
});