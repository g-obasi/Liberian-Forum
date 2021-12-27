SELECT "forum_topic"."id",
       "forum_topic"."slug",
       "forum_topic"."board_id",
       "forum_topic"."created_by_id",
       "forum_topic"."title",
       "forum_topic"."date_created",
       "forum_topic"."featured",
       "forum_topic"."views",
       "forum_topic"."order",
       "forum_topic"."post_count",
       "forum_topic"."status",
       "forum_topic"."last_updated"
  FROM "forum_topic"
 WHERE "forum_topic"."id" = 136991