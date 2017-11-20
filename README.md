# iOSMultiLanguageTools
This tool could help you do internationalization automate

如果你的项目已经迭代了不少版本了，这个时候突然有需求来说要做多语言支持。你搜索了下工程里面的汉字，然后就懵逼了，太多汉字写在代码里了！人肉搬运工？NO！

下面的这个小工具可以帮你省下不少时间。

1. 拷贝`multi-lang.py`到你的工程根目录
2. 如果你在找到这个小工具前已经做了一点国际化，那么拷贝`Localizable.strings`到你的工程根目录
3. 运行`python multi-lang.py`, 你可能需要安装 `pypinyin`
3. 将根目录下`Localizable.strings`拷贝回原来的路径

你代码里面需要修改的汉字都已经替换成`NSLocalizedString`了。

当然，如果你只想看看有哪些汉字需要被替换，修改`multi-lang.py`代码，设置`onlyShowProcessResult = True`，重新运行后，查看根目录下的`out.txt`吧。

这个小工具在做`.strings`文件的key-value对应时，只是简单的把汉字翻译成拼音来作为key，当你的汉字字符串太长或者你不喜欢拼音。那么你可以这样使用

1. 修改`multi-lang.py`代码，设置`onlyShowProcessResult = True`，运行`python multi-lang.py`
2. 在`out.txt`里修改key为你喜欢的字符串。
3. 把`out.txt`里的内容，拷贝到`Localizable.strings`
4. 修改`multi-lang.py`代码，设置`onlyShowProcessResult = False`，重新运行`python multi-lang.py`
4. Done！

现在这个小工具暂时只支持OC，如果想支持其他语言，稍加改动就行了。

### Know issue

1. 暂不支持查找一行多个中文字符串
   ```
   NSArray *operators = @[@"手动档", @"自动档"];
   ```
   
   how to fix: 换成多行
   
   ```
   NSArray *operators = @[@"手动档", 
   						   @"自动档"];
   ```
