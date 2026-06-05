# django_error_li

# 環境変数にPostgreSQLのパスワードを設定する
config/settings.pyに直接に直接記述しているパスワードを環境変数に格納する。

まず、ターミナルで以下のコマンドを一行ずつ実行する。

```
echo 'export POSTGRESQL_PASSWORD=ご自身の設定したパスワード' >> ~/.zshrc
```

```
echo $POSTGRESQL_PASSWORD
```

結果に設定されたパスワードが表示されれば、成功。

# 環境変数をアプリケーション側で読み込む設定をする

```
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'first_app',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('POSTGRESQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',  #自身の設定したポート番号を設定
    }
}
```

# django_quiz_v3.htmlをブラウザで開いて、問題を解き始めてください