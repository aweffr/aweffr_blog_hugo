```bash
hugo -D && \
  ssh aweffr@aweffr.com rm -rf /var/www/aweffr_blog_hugo/public && \
  scp -r ~/aweffr_blog_hugo/public aweffr@aweffr.com:/var/www/aweffr_blog_hugo/public  && \
  ssh aweffr@aweffr.com chown -R aweffr:www-data /var/www/aweffr_blog_hugo/public  && \
  ssh aweffr@aweffr.com sudo nginx -s reload
```
