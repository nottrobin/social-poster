curl -X POST -H "Content-Type: application/json" \
  -H "api-key: ${DEV_API_KEY}" \
  -d '{"article":{"title":"A test article","body_markdown":"Hello world","published":false,"tags":["discuss", "javascript"]}}' \
  https://dev.to/api/articles
