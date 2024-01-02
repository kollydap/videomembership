TO START SERVER
```
uvicorn main:app --reload
```


```
python

from app.users.models import User
import db
db.get_Sessions()

User.objects.create(email="kola@gmail.com", password="1234")

```