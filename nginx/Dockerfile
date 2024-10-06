FROM nginx

# remove the default conf
RUN rm /etc/nginx/conf.d/default.conf

#  copy the nginx.conf in our filesystem into the image filesystem
COPY default.conf /etc/nginx/conf.d

EXPOSE 80

# # Nginx 실행
CMD ["nginx", "-g", "daemon off;"]