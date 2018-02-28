aws apigateway test-invoke-method \
--rest-api-id y2fv8g0anl \
--resource-id v8bovl \
--http-method POST \
--path-with-query-string "" --body "{\"operation\":\"create\",\"tableName\":\"Events\",\"payload\":{\"Item\":{\"id\":\"7\",\"organization\":\"Nashville Food Project\",\"description\":\"Garden volunteer\", \"opportunities\":\"Volunteer\", \"category\":\"Food\"}}}"
