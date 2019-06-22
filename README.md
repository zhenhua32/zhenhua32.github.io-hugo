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

echo 'theme = "ananke"' >> blog/config.toml
```

手动添加文章

```powershell
.\bin\hugo.exe -s ./blog new posts/hello.md
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
