# 解答・解説集

> ストーリー形式：Q01 から順番に修正すると次のエラーが現れます。
> 実際のDjango開発で遭遇しやすいエラーを体験しながら学べます。

---

## ── フェーズ1：サーバー起動時のエラー ──

---

### Q01 【初級】`settings.py` — サーバーが起動しない

**出るエラー（ターミナル）**
```
django.core.exceptions.ImproperlyConfigured:
  'posts' is not installed. ...
```
または `python manage.py runserver` 時に posts アプリが認識されない。

**エラー箇所**
```python
INSTALLED_APPS = [
    ...
    'django_extensions',
    # 'posts' が無い！
]
```

**原因**
新しく作った `posts` アプリを `INSTALLED_APPS` に登録していないため、Django がアプリの存在を知らない状態です。モデル・ビュー・テンプレートすべてが認識されません。

**修正後**
```python
INSTALLED_APPS = [
    ...
    'django_extensions',
    'posts',   # ← 追加
]
```

**ポイント**
`startapp` でアプリを作ったら `INSTALLED_APPS` への追加と `makemigrations → migrate` はセットで行う習慣をつけましょう。

---

### Q02 【初級】`config/urls.py` — サーバー起動時に ModuleNotFoundError

**出るエラー（ターミナル）**
```
ModuleNotFoundError: No module named 'urls'
```

**エラー箇所**
```python
path('posts/', include('urls')),
```

**原因**
`include()` には **アプリ名を含めたドット記法のモジュールパス** を渡す必要があります。`'urls'` というモジュールは存在しません。

**修正後**
```python
path('posts/', include('posts.urls')),
```

**ポイント**
複数アプリがある場合は `'アプリ名.urls'` の形式で必ず書きます。

---

### Q03 【初級】`posts/urls.py` — NoReverseMatch（名前空間のタイポ）

**出るエラー（ブラウザ）**
```
NoReverseMatch: 'posts' is not a registered namespace
```

**エラー箇所**
```python
app_name = 'post'   # 's' が抜けている
```

**原因**
`views.py` やテンプレートで `'posts:index'` `'posts:create'` と参照しているのに、`app_name` が `'post'` なので名前空間が一致しません。

**修正後**
```python
app_name = 'posts'
```

**ポイント**
`app_name` は `{% url 'app_name:view_name' %}` や `redirect('app_name:view_name')` と **完全一致** していなければなりません。1文字のタイポでも即エラーになります。

---

## ── フェーズ2：ページ表示時のエラー ──

---

### Q04 【初級】`models.py` — マイグレーションが通らない

**出るエラー（ターミナル）**
```
django.db.utils.OperationalError: table "posts" does not exist
```
または `makemigrations` 時：
```
SystemCheckError: 'posts.Post.content' field: CharFields must define a 'max_length' attribute.
```

**エラー箇所**
```python
content = models.CharField(blank=True)  # max_length がない
```

**原因**
`CharField` は `max_length` が **必須** です。省略するとシステムチェックでエラーになり、マイグレーションが作成されません。

**修正後**
```python
content = models.CharField(max_length=255, blank=True)
```

**ポイント**
`blank=True` はフォームの入力を空にしてよいという設定。`null=True` はDBレベルでNULLを許可する設定。`CharField` では通常 `blank=True` のみ使います。

---

### Q05 【初級】`views.py` — TemplateDoesNotExist

**出るエラー（ブラウザ）**
```
TemplateDoesNotExist: index.html
```

**エラー箇所**
```python
return render(request, 'index.html', {'posts': posts})
```

**原因**
テンプレートファイルは `templates/posts/index.html` に置かれていますが、パスが `'index.html'` になっているため Django がファイルを見つけられません。

**修正後**
```python
return render(request, 'posts/index.html', {'posts': posts})
```

**ポイント**
`APP_DIRS: True` の場合、テンプレートは `アプリ名/templates/` 以下を探します。アプリ間の名前衝突を防ぐため `templates/posts/` のようにアプリ名サブディレクトリを切るのが慣習です。

---

### Q06 【初級】`index.html` — NoReverseMatch（テンプレートの名前空間漏れ）

**出るエラー（ブラウザ）**
```
NoReverseMatch: Reverse for 'create' not found.
```

**エラー箇所**
```html
<a href="{% url 'create' %}">新規投稿</a>
```

**原因**
`posts/urls.py` で `app_name = 'posts'` を定義しているため、テンプレートの `{% url %}` タグも名前空間付きで書く必要があります。

**修正後**
```html
<a href="{% url 'posts:create' %}">新規投稿</a>
```

**ポイント**
`redirect()` と `{% url %}` は同じルールです。`app_name` を設定したら **すべての逆引き** に `名前空間:` を付けます。

---

## ── フェーズ3：フォーム・DB操作のエラー ──

---

### Q07 【初級】`create.html` — 403 Forbidden

**出るエラー（ブラウザ）**
```
403 Forbidden
CSRF verification failed. Request aborted.
```

**エラー箇所**
```html
<form method="post">
  {{ form.content }}   ← csrf_token がない
```

**原因**
Django は POST リクエストに CSRF トークンを要求します。`{% csrf_token %}` がないと悪意あるサイトからの不正リクエストと区別できないため、403エラーを返します。

**修正後**
```html
<form method="post">
  {% csrf_token %}
  {{ form.content }}
  <button type="submit">投稿する</button>
</form>
```

**ポイント**
`method="post"` のフォームには **必ず** `{% csrf_token %}` を書きます。これはXSRF攻撃を防ぐDjangoの組み込みセキュリティ機能です。

---

### Q08 【初級】`forms.py` — TypeError（fieldsの型ミス）

**出るエラー（ブラウザ）**
```
TypeError: PostForm.Meta.fields cannot be a string.
Did you mean to type: fields = ['content']?
```

**エラー箇所**
```python
fields = 'content'
```

**原因**
`fields` はリストで渡す必要があります。文字列を渡すと Django が各文字（`'c'`, `'o'`, `'n'`...）をフィールド名として解釈しようとして `TypeError` になります。

**修正後**
```python
fields = ['content']
```

**ポイント**
全フィールドを対象にする場合は `fields = '__all__'`（文字列）も使えますが、セキュリティ上は明示的にリストで指定するのがベストプラクティスです。

---

### Q09 【初級】`views.py` — NoReverseMatch（redirectの名前空間漏れ）

**出るエラー（ブラウザ）**
```
NoReverseMatch: Reverse for 'index' not found.
```

**エラー箇所**
```python
return redirect('index')
```

**原因**
Q03・Q06 と同じく、`app_name = 'posts'` を定義しているため `redirect()` も名前空間付きで書く必要があります。

**修正後**
```python
return redirect('posts:index')
```

**ポイント**
`redirect()` と `{% url %}` は同じ逆引き機能を使っています。どちらも `'名前空間:URL名'` の形式で統一します。

---

### Q10 【中級】`views.py` — バリデーションエラーが無視される

**出るエラー（ブラウザ）**
エラーは出ないが、**空のまま投稿するとそのまま一覧に空投稿が保存されてしまう**。

**エラー箇所**
```python
def post(self, request, *args, **kwargs):
    form = PostForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('posts:index')  # ← is_valid() が False でもリダイレクト
```

**原因**
`form.is_valid()` が `False`（バリデーション失敗）のとき、エラーメッセージをフォームに表示せずそのまま一覧画面へリダイレクトしています。ユーザーは何が間違っていたか分かりません。
（今回 `content` は `blank=True` なので空投稿も通ってしまいますが、将来 `blank=False` にしたときに問題が顕在化します）

**修正後**
```python
def post(self, request, *args, **kwargs):
    form = PostForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('posts:index')
    return render(request, 'posts/create.html', {'form': form})  # ← エラー表示
```

**ポイント**
バリデーション失敗時はフォームを再描画してエラーを表示するのが基本パターンです。`redirect` と `render` の使い分けを覚えましょう。
- **成功時** → `redirect`（POST後のリロードによる二重送信を防ぐ）
- **失敗時** → `render`（エラーメッセージ付きフォームを再表示）

---

## まとめ：エラー出現フロー

```
python manage.py runserver
        │
        ├─ Q01: ImproperlyConfigured → settings.py に 'posts' を追加
        │
        ├─ Q02: ModuleNotFoundError → include('posts.urls') に修正
        │
        └─ 起動成功 → ブラウザで /posts/ にアクセス
                │
                ├─ Q03: NoReverseMatch (namespace) → app_name = 'posts' に修正
                │
                ├─ Q04: OperationalError → max_length 追加 + migrate
                │
                ├─ Q05: TemplateDoesNotExist → 'posts/index.html' に修正
                │
                └─ 一覧ページ表示成功 → 「新規投稿」リンクをクリック
                        │
                        ├─ Q06: NoReverseMatch (url tag) → {% url 'posts:create' %}
                        │
                        └─ 投稿フォーム表示成功 → 投稿ボタンを押す
                                │
                                ├─ Q07: 403 Forbidden → {% csrf_token %} 追加
                                │
                                ├─ Q08: TypeError (fields) → fields = ['content']
                                │
                                ├─ Q09: NoReverseMatch (redirect) → redirect('posts:index')
                                │
                                └─ Q10: 空投稿が通る → is_valid False 時に render で返す
```

| # | ファイル | 難易度 | エラー種別 |
|---|---------|--------|-----------|
| Q01 | settings.py | 初級 | INSTALLED_APPS 登録漏れ |
| Q02 | config/urls.py | 初級 | include() パスミス |
| Q03 | posts/urls.py | 初級 | app_name タイポ |
| Q04 | models.py | 初級 | CharField max_length なし |
| Q05 | views.py | 初級 | テンプレートパスミス |
| Q06 | index.html | 初級 | {% url %} 名前空間漏れ |
| Q07 | create.html | 初級 | csrf_token 欠落 |
| Q08 | forms.py | 初級 | fields が文字列 |
| Q09 | views.py | 初級 | redirect 名前空間漏れ |
| Q10 | views.py | 中級 | バリデーション失敗時の処理漏れ |
