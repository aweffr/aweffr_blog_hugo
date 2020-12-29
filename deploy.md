```bash
hugo -D
scp -r ~/aweffr_blog_hugo/public aweffr@aweffr.com:/var/www/aweffr_blog_hugo/public
ssh aweffr@aweffr.com chown -R aweffr:www-data /var/www/aweffr_blog_hugo/public
```
