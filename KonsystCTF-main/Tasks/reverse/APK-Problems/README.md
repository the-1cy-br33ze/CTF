# APK-Problems Solve

1. Декомпиляция APK-файла.
   
   Сначала вам необходимо декомпилировать APK, который вы хотите изменить:

   ```
   apktool d путь_к_apk-файлу
   ```

   Это создаст директорию, содержащую декомпилированные ресурсы и файлы.

2.  После этого, используя разные инструменты, можно выполнить поиск по каталогам и обнаружить - **secret_string** в resources/res/value/String.xml

3. Она закодирована в Base64 и через CyberChef легко "вскрывается". 

https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=Wm14aFozdERNRzVUZVhOMExVRlFTeTFFWlhZa2ZRPT0


