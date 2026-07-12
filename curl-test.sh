curl http://127.0.0.1:5000/api/timeline_post

curl -X POST http://127.0.0.1:5000/api/timeline_post \
  -d 'name=LinhLe' \
  -d 'email=linhle123@gmail.com' \
  -d 'content=TestPostTimeline'

curl http://127.0.0.1:5000/api/timeline_post

# Bonus: delete a test timeline post at the end of the script.
curl -X DELETE http://127.0.0.1:5000/api/timeline_post/1


