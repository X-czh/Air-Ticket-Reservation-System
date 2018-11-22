insert into airline values ('China Eastern');
insert into airport values('JFK', 'NYC');
insert into airport values('PVG', 'Shanghai');
insert into customer values('cust1@outlook.com', 'cust1', '11111111', 
    'A141', '14 ST', 'NYC', 'NY', 1111, 'US111', '2021-01-01', 'USA',
    '1980-01-01');
insert into customer values('cust2@outlook.com', 'cust2', '22222222', 
    '1555', 'Century Avenue', 'Shanghai', 'Shanghai', 2222, 'CN111', '2021-01-01', 'China',
    '1980-01-01');
insert into airplane values('China Eastern', 10001, 11);
insert into airplane values('China Eastern', 10002, 12);
insert into airplane values('China Eastern', 10003, 13);
insert into airline_staff values('I''M_CUTE', '00000000', 'James', 'Chen',
    '1980-01-01', 'China Eastern');
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
insert into booking_agent values('agent1@outlook.com', '00000000', 1001);
insert into ticket values(100, 'China Eastern', 101);
insert into ticket values(200, 'China Eastern', 121);

