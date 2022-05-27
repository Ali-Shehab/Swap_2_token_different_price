// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


interface IERC20  {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
}

contract Swap{
    using SafeMathChainlink for uint256;

    address token1;
    address token2;
    AggregatorV3Interface public price1;
    AggregatorV3Interface public price2;
    constructor(address _token1, address _token2,address _price1,address _price2) public
    {
        token1 = _token1;
        token2 = _token2;
        price1 = AggregatorV3Interface(_price1);
        price2 = AggregatorV3Interface(_price2);
    }

    function swap(address token,uint256 amount) public
    {
        if(token == token1)
        {
            IERC20 tokenA = IERC20(token);
            IERC20 tokenB = IERC20(token2);
            uint256 priceTokenA = getPriceToken1();
            uint256 priceTokenB = getPriceToken2();
            uint256 priced1 = (priceTokenA * 10 ** 18 / priceTokenB) * amount;
            amount = priced1 / 10 ** 18;
            tokenB.approve(address(this), amount);
            _safeTransferFrom(tokenA,msg.sender,address(this),amount);
            _safeTransferFrom(tokenB,address(this),msg.sender,amount);
        }
        else
        {
            IERC20 tokenA = IERC20(token);
            IERC20 tokenB = IERC20(token2);
            uint256 priceTokenA = getPriceToken1();
            uint256 priceTokenB = getPriceToken2();
            uint256 priced2 = (priceTokenB * 10 ** 18 / priceTokenA) * amount;
            amount = priced2 / 10 ** 18;
            tokenA.approve(address(this), amount);
            _safeTransferFrom(tokenB,msg.sender,address(this),amount);
            _safeTransferFrom(tokenA,address(this),msg.sender,amount);
        }
    }
    
    function getPriceToken1() public view returns(uint256)
    {
        (,int256 answer,,,) = price1.latestRoundData();
        return uint256(answer) * 10000000000;
    }

    function getPriceToken2() public view returns(uint256)
    {
        (,int256 answer,,,) = price2.latestRoundData();
        return uint256(answer) * 10000000000;
    }



    function _safeTransferFrom(IERC20 token, address sender,address reciever,uint256 amount) internal {
        bool sent = token.transferFrom(sender,reciever, amount);
        require(sent,"The transaction failed");
    }
    
}