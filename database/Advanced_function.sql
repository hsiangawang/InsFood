DROP PROCEDURE IF EXISTS getTagRecommend;

DELIMITER //

CREATE PROCEDURE getTagRecommend(IN friend_id integer, IN tag varchar(30))
BEGIN
	SELECT r.name, r.url, r.image_url
    FROM   Restaurant r JOIN LikeList l ON r.restaurant_id = l.restaurant_id
    WHERE  l.user_id = friend_id AND r.categories LIKE CONCAT('%', tag, '%');

END //
DELIMITER ;


