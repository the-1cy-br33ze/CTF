##### Решение:
> Если какой-то параметр указан неправильно - сервер возвращает код ошибки и пункт RFC, в котором указан правильный формат.

 - Заварить кофе:
```bash
root@dhxurtt:~/coffee# curl -X BREW http://localhost/coffee \
     -H "Content-Type: application/coffee-pot-command" \
     -H "Accept-Additions: cream, syrup" \
     -d "start"
Brewing started
root@dhxurtt:~/coffee# 
```

 - Завершить готовку и получить флаг:
```bash
root@dhxurtt:~/coffee# curl -X WHEN http://localhost/coffee
Coffee ready! Flag: flag{1t_w@sn't_a_j0ke}
root@dhxurtt:~/coffee#
```

##### Дополнительно: 
 - Получить добавки:
```bash
root@dhxurtt:~/coffee# curl -X PROPFIND http://localhost/coffee
<D:additions>cream syrup whisky</D:additions>
root@dhxurtt:~/coffee#
```

