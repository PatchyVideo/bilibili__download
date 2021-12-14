CREATE TABLE patchy_video
    (
        bv varchar(50), 
        av varchar(50), 
        url varchar(255), 
        name varchar(500), 
        path varchar(255), 
        size float, 
        length float, 
        frame float, 
        fps float, 
        aid int
    )
;

CREATE TABLE url_q
    (
        time int,
        url varchar(255)
    )
;