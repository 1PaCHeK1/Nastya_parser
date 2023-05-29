# Rest API:
* /post – create post
* /post/{id} - get post by id
* /post/{id}/comments - get comments by post_id
* /post/{id}/tags - get tags by post_id
* /post/{id}/attachments - get attachments by post_id
* /post/{id}/... - get ... by post_id


# graphql
```gql
{
    post(id) {
        title
        author {
            id
            firstname
            lastname
            avatar {
                path
            }
        }
        body
        comments {
            name
            author {
                id
                firstname
                lastname
                avatar {
                    path
                }
            }
        }
        tags {
            id
            name
        }
    }
}
```