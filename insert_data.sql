insert into airline values ('China Eastern');
insert into airline values ('United Airlines');

insert into airport values('JFK', 'NYC');
insert into airport values('PVG', 'Shanghai');

insert into airplane values('China Eastern', 10001, 3);
insert into airplane values('China Eastern', 10002, 3);
insert into airplane values('China Eastern', 10003, 10);
insert into airplane values('United Airlines', 10001, 3);
insert into airplane values('United Airlines', 10002, 3);
insert into airplane values('United Airlines', 10003, 10);

insert into flight values('China Eastern', 101, 
    'PVG', '2018-10-28 23:59:59',
    'JFK', '2018-10-29 23:59:59',
    6000, 'UPCOMING', 10001);
insert into flight values('China Eastern', 121, 
    'PVG', '2018-10-28 10:59:59',
    'JFK', '2018-10-29 10:59:59',
    6000, 'IN-PROGRESS', 10002);
insert into flight values('China Eastern', 921, 
    'JFK', '2018-10-27 13:59:59',
    'PVG', '2018-10-28 13:59:59',
    6000, 'DELAYED', 10003);
insert into flight values('United Airlines', 101, 
    'PVG', '2018-6-28 23:59:59',
    'JFK', '2018-6-29 23:59:59',
    6000, 'UPCOMING', 10001);
insert into flight values('United Airlines', 121, 
    'PVG', '2017-12-28 10:59:59',
    'JFK', '2017-12-29 10:59:59',
    6000, 'IN-PROGRESS', 10002);
insert into flight values('United Airlines', 921, 
    'JFK', '2017-10-27 13:59:59',
    'PVG', '2017-10-28 13:59:59',
    6000, 'DELAYED', 10003);

insert into ticket values(100, 'China Eastern', 101);
insert into ticket values(101, 'China Eastern', 121);
insert into ticket values(102, 'China Eastern', 921);
insert into ticket values(200, 'United Airlines', 101);
insert into ticket values(201, 'United Airlines', 101);
insert into ticket values(202, 'United Airlines', 101);

insert into purchases values(100, 'test1@test.com', NULL, '2018-6-28');
insert into purchases values(101, 'test2@test.com', NULL, '2018-6-28');
insert into purchases values(102, 'test3@test.com', 102, '2018-6-28');
insert into purchases values(200, 'test2@test.com', 101, '2018-6-28');
insert into purchases values(201, 'test1@test.com', 101, '2017-6-28');
insert into purchases values(202, 'test1@test.com', 101, '2017-6-28');

-- Customer 1:
-- Email: test1@test.com
-- Password: 1111

-- Customer 2:
-- Email: test2@test.com
-- Password: 1111

-- Customer 3:
-- Email: test3@test.com
-- Password: 1111

-- Booking Agent 1:
-- Email: testba1@test.com
-- Password: 1111
-- Booking Agent ID: 101

-- Booking Agent 2:
-- Email: testba2@test.com
-- Password: 1111
-- Booking Agent ID: 102

-- Airline Staff 1:
-- Email: testas1@test.com
-- Password: 1111
-- Airline: China Eastern

-- Airline Staff 2:
-- Email: testas2@test.com
-- Password: 1111
-- Airline: United Airlines
