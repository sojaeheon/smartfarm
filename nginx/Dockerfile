FROM nginx

# remove the default conf
RUN rm /etc/nginx/conf.d/default.conf

#  copy the nginx.conf in our filesystem into the image filesystem
COPY default.conf /etc/nginx/conf.d

# 프론트엔드 파일을 Nginx의 HTML 폴더에 복사
# COPY --from=frontend-stage /app/dist/index.html /usr/share/nginx/html

EXPOSE 80

# # Nginx 실행
CMD ["nginx", "-g", "daemon off;"]