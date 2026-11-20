# os.walk 遍历目录树并产出三元组
`os.walk` 就是「按目录逐层吐出 (当前路径, 子目录名列表, 文件名列表) 的惰性遍历器」
```
import os
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tmp:
    root = Path(tmp) / "demo"
    (root / "sub").mkdir(parents=True)
    (root / "a.txt").touch()
    (root / "sub" / "b.txt").touch()
  
    for current, dirs, files in os.walk(root):
        print(Path(current).relative_to(root), dirs, files)
```
```
/tmp
└── /demo
    ├── /sub
    │   └── b.txt
    └── a.txt
```

猜测：不会<br>
实际输出：<br>
. ['sub'] ['a.txt']<br>
sub [] ['b.txt']
