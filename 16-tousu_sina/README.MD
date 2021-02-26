# 介绍

目标网址：
```
aHR0cHM6Ly90b3VzdS5zaW5hLmNvbS5jbi9jb21wYW55L3ZpZXcvP2NvdWlkPTYyNDQyMTEzNzU=
```


讲解：
``` 
https://mp.weixin.qq.com/s/t2eoaLKuqqBRwR1dLiw3hw
```

SHA256 哈希 sigature

```
ts: u,// timestamp
rs: d,// random string
couid: couid,
page_size: page_size,
page: page,
// SHA256 哈希
signature: CryptoJS.SHA256([u, d, l, couid, 1, page_size, page].sort().join("")).toString()
```

