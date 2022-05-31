CREATE TABLE comment_new (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  parent_comment_id INTEGER,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comment TEXT NOT NULL,
  FOREIGN KEY (post_id) REFERENCES post (id),
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (parent_comment_id) REFERENCES comment (id)
);

insert into comment_new (post_id, author_id, created, comment)
select post_id, author_id, created, comment
from comment;

DROP TABLE comment;

ALTER TABLE comment_new RENAME TO comment;