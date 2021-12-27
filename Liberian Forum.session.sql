-- SELECT "forum_post"."id",
--        "forum_post"."created_by_id",
--        "forum_post"."message",
--        "forum_post"."date_created",
--        "forum_post"."topic_id",
--        "forum_post"."status",
--        "forum_post"."user_ip"
--   FROM "forum_post"
--  WHERE "forum_post"."topic_id" = 136991
--  ORDER BY "forum_post"."date_created" ASC


-- SELECT "forum_topic"."id",
--        "forum_topic"."slug",
--        "forum_topic"."board_id",
--        "forum_topic"."created_by_id",
--        "forum_topic"."title",
--        "forum_topic"."date_created",
--        "forum_topic"."featured",
--        "forum_topic"."views",
--        "forum_topic"."order",
--        "forum_topic"."post_count",
--        "forum_topic"."status",
--        "forum_topic"."last_updated"
--   FROM "forum_topic"
--  WHERE "forum_topic"."id" = 136991

select * from forum_post where id = 65228