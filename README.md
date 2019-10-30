# 个人博客

基于 Hugo 的个人博客

## 生成站点的过程

生成站点

```powershell
.\bin\hugo.exe new site blog
```

下载主题

```powershell
git submodule add https://github.com/matcornic/hugo-theme-learn.git blog/themes/hugo-theme-learn

echo 'theme = "hugo-theme-learn"' >> blog/config.toml
```

手动添加文章

```powershell
.\bin\hugo.exe -s ./blog new posts/hello.md
```

基于 hugo-theme-learn 的常见动作

```powershell
# 创建章节
./bin/hugo new 1-hugo/_index.md --kind chapter -s ./blog
# 创建内容页
./bin/hugo new 1-hugo/install.md -s ./blog
```

启动服务器

```powershell
.\bin\hugo.exe -s ./blog server -D
```

修改配置

打开 config.toml 文件, 修改配置

生成静态站点

```powershell
.\bin\hugo.exe -s ./blog
```

添加子模块

git submodule add -b master git@github.com:zhenhua32/zhenhua32.github.io.git zhenhua32.github.io
