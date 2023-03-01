FROM nginx:1.19.0-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY my_test_site.nginx.conf /etc/nginx/sites-available/my_test_site.nginx.conf
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/my_test_site.nginx.conf /etc/nginx/sites-enabled/
CMD ["nginx", "-g", "daemon off;"]