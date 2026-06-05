# 解答・解説集

> Q01 から順番に修正してください。1問直すと次のエラーが現れます。
> posts_urls.py と views.py には複数のエラーが仕込まれています。
> 上から順に直していくと自然に次のエラーが露出します。

---

### Q01 【初級】`config_urls.py` — runserver起動時に ModuleNotFoundError

**出るエラー（ターミナル）**
```
ModuleNotFoundError: No module named 'urls'
```

**エラー箇所**
```python
path('posts/', include('urls')),
```

**修正後**
```python
path('posts/', include('posts.urls')),
```

**ポイント**
`include()` には `'アプリ名.urls'` の形式で渡します。

---

### Q02 【初級】`posts_urls.py` — /posts/ アクセス時に NoReverseMatch

**出るエラー（ブラウザ）**
```
NoReverseMatch: 'posts' is not a registered namespace
```

**エラー箇所**
```python
app_name = 'post'   # 's' が抜けている
```

**修正後**
```python
app_name = 'posts'
```

**ポイント**
`app_name` は `redirect()` や `{% url %}` の名前空間と完全一致が必要です。
※ このファイルにはもう1つエラーがあります（Q06）。今は触らずそのままにしてください。

---

### Q03 【初級】`views.py` — /posts/ アクセス時に TemplateDoesNotExist

**出るエラー（ブラウザ）**
```
TemplateDoesNotExist: index.html
```

**エラー箇所**
```python
return render(request, 'index.html', {'posts': posts})
```

**修正後**
```python
return render(request, 'posts/index.html', {'posts': posts})
```

**ポイント**
テンプレートパスは `'アプリ名/ファイル名'` の形式で書きます。
※ このファイルにはあと2つエラーがあります（Q09・Q10）。今は触らずそのままにしてください。

---

### Q04 【初級】`settings.py` — CSSが反映されない（動作異常）

**出るエラー**
エラーは出ないが CSS が当たっておらず見た目が崩れている。
ブラウザの開発者ツール（F12）のネットワークタブで CSS ファイルが 404 になっている。

**エラー箇所**
```python
STATICFILES_DIRS = [BASE_DIR / 'statics']   # 's' が余分
```

**修正後**
```python
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**ポイント**
CSS・画像が表示されないときはブラウザの開発者ツール（F12）のネットワークタブで 404 になっていないか確認しましょう。

---

### Q05 【初級】`index.html` — 「新規投稿」リンクで NoReverseMatch

**出るエラー（ブラウザ）**
```
NoReverseMatch: Reverse for 'create' not found.
```

**エラー箇所**
```html
<a href="{% url 'create' %}">新規投稿</a>
```

**修正後**
```html
<a href="{% url 'posts:create' %}">新規投稿</a>
```

**ポイント**
`{% url %}` と `redirect()` は同じルール。`app_name` を設定したらすべての逆引きに `名前空間:` を付けます。

---

### Q06 【初級】`posts_urls.py` — 投稿フォームを開くと 404

**出るエラー（ブラウザ）**
```
Page not found (404)
/posts/create/ に一致するURLパターンが見つかりませんでした
```

**エラー箇所**
```python
path('creates/', views.CreateView.as_view(), name='create'),
```

**修正後**
```python
path('create/', views.CreateView.as_view(), name='create'),
```

**ポイント**
404 が出たときはまず `urls.py` のパス定義を見直しましょう。

---

### Q07 【初級】`create.html` — 投稿ボタンを押すと 403 Forbidden

**出るエラー（ブラウザ）**
```
403 Forbidden
CSRF verification failed. Request aborted.
```

**エラー箇所**
```html
<form method="post">
  {{ form.content }}   ← {% csrf_token %} がない
```

**修正後**
```html
<form method="post">
  {% csrf_token %}
  {{ form.content }}
  <button type="submit">投稿する</button>
</form>
```

**ポイント**
`method="post"` のフォームには必ず `{% csrf_token %}` を書きます。

---

### Q08 【初級】`forms.py` — 投稿ボタンを押すと TypeError

**出るエラー（ブラウザ）**
```
TypeError: PostForm.Meta.fields cannot be a string.
Did you mean to type: fields = ['content']?
```

**エラー箇所**
```python
fields = 'content'
```

**修正後**
```python
fields = ['content']
```

**ポイント**
`fields` はリストで指定します。文字列で渡すと各文字をフィールド名として解釈しようとして `TypeError` になります。

---

### Q09 【初級】`views.py` — 投稿後に NoReverseMatch

**出るエラー（ブラウザ）**
```
NoReverseMatch: Reverse for 'index' not found.
```

**エラー箇所**
```python
return redirect('index')
```

**修正後**
```python
return redirect('posts:index')
```

**ポイント**
`redirect()` も `{% url %}` と同じく名前空間が必要です。
※ このファイルにはあと1つエラーがあります（Q10）。

---

### Q10 【初級】`views.py` — 投稿しても一覧に表示されない（動作異常）

**出るエラー**
エラーは出ないが、投稿ボタンを押しても一覧ページに投稿が表示されない。

**エラー箇所**
```python
form.save   # () が抜けている
```

**修正後**
```python
form.save()
```

**ポイント**
`form.save` は括弧がないためメソッドを呼び出していません。Python はこの記述をエラーにしないため気づきにくいバグです。「エラーは出ないのに動かない」場合は `()` 抜けを疑いましょう。

---

## エラー出現フロー まとめ

```
$ python manage.py runserver
  │
  └─ Q01 config_urls.py:  ModuleNotFoundError   → include('posts.urls') に修正
          ↓ 起動成功。ブラウザで /posts/ を開く
  └─ Q02 posts_urls.py:   NoReverseMatch        → app_name = 'posts' に修正
  └─ Q03 views.py:        TemplateDoesNotExist  → 'posts/index.html' に修正
          ↓ ページ表示成功。CSSが当たっていない
  └─ Q04 settings.py:     CSS未適用             → STATICFILES_DIRS = [BASE_DIR / 'static']
          ↓ 「新規投稿」リンクをクリック
  └─ Q05 index.html:      NoReverseMatch        → {% url 'posts:create' %} に修正
          ↓ /posts/create/ を開く
  └─ Q06 posts_urls.py:   404 Not Found         → path('create/', ...) に修正
          ↓ フォーム表示成功。投稿ボタンを押す
  └─ Q07 create.html:     403 Forbidden         → {% csrf_token %} を追加
  └─ Q08 forms.py:        TypeError             → fields = ['content'] に修正
  └─ Q09 views.py:        NoReverseMatch        → redirect('posts:index') に修正
          ↓ 投稿成功。でも一覧に表示されない
  └─ Q10 views.py:        動作異常              → form.save() に修正

✔ 全問クリア！
```

## ファイルとエラーの対応表

| # | ファイル | エラー内容 | タイミング |
|---|---------|-----------|----------|
| Q01 | config_urls.py | include() パスミス | runserver起動時 |
| Q02 | posts_urls.py | app_name タイポ | ページアクセス時 |
| Q03 | views.py | テンプレートパスミス | ページアクセス時 |
| Q04 | settings.py | STATICFILES_DIRS ミス | ページ表示時 |
| Q05 | index.html | {% url %} 名前空間漏れ | ページ表示時 |
| Q06 | posts_urls.py | URL パスタイポ | リンククリック時 |
| Q07 | create.html | csrf_token 欠落 | 投稿ボタン押下時 |
| Q08 | forms.py | fields が文字列 | 投稿ボタン押下時 |
| Q09 | views.py | redirect 名前空間漏れ | 投稿後 |
| Q10 | views.py | form.save() 括弧なし | 投稿後 |
