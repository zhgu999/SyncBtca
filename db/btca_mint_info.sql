CREATE DEFINER=`btca`@`localhost` PROCEDURE `mint_info`(walletId varchar(64))
BEGIN
	declare bbc_addr_ VARCHAR(64);
	declare height_ int;
    declare best_balance_ bigint;
	declare best_balance_reward_ bigint;
    declare min_balance_ bigint;
	declare min_balance_reward_ bigint;
            
    select bbc_addr into bbc_addr_ from addr where addr.walletId = walletId;
    select height into height_ from reward order by id desc limit 1;
    
	select amount,stake_reward into best_balance_, best_balance_reward_ 
    from reward where height = height_ order by stake_reward / amount desc limit 1;
    
	select amount,stake_reward into min_balance_, min_balance_reward_ 
    from reward where height = height_ order by stake_reward / amount asc limit 1;

    select	cast((promotion_reward / 1000000) as char) as promotion_reward,
			-- 推广收益
			cast((stake_reward / 1000000) as char) as stake_reward,
            -- 持币收益
			cast((amount / 1000000) as char) as this_balance,
            -- 当期持币
            cast((stake_reward / 1000000) as char) as this_stake_reward,
            -- 当期收益(与持币收益相同)
			cast((best_balance_ / 1000000) as char) as best_balance,
            -- 最佳持币
			cast((best_balance_reward_ / 1000000) as char) as best_balance_reward,
            -- 最佳持币收益
            cast((min_balance_ / 1000000) as char) as min_balance,
            -- 最差持币
			cast((min_balance_reward_ / 1000000) as char) as min_balance_reward
            -- 最差持币收益
      from reward where address = bbc_addr_ order by id desc limit 1;
      

END