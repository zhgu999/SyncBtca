CREATE DEFINER=`btca`@`localhost` PROCEDURE `chart_info`(walletId varchar(64))
BEGIN
	declare bbc_addr_ VARCHAR(64);
	declare height_ int;
    select bbc_addr into bbc_addr_ from addr where addr.walletId = walletId;
    select height into height_ from reward order by id desc limit 1;
    
    select 	cast((amount / 1000000) as char) as balance, 
			-- 持币数量
			cast((stake_reward / amount) as char) as reward,
            -- 持币收益 
			case address 
				when bbc_addr_ then true
				else false
			end as user_balance
            -- 是否是自己
	from reward where height = height_;
END