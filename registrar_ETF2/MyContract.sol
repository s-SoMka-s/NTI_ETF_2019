pragma solidity >=0.5.0 <0.6.0;

contract MyContract {
    string ownerName;
    address ownerAddress;
	constructor() public {
		
	}
	
	function delOwnerName() public {
	    delete(ownerName);
	}
	
	function setOwnerName(string memory _name) public {
	    ownerName = _name;
	}
	
	function getOwnerName() public view returns (string memory){
	   return ownerName;
	}
	
	function setOwnerAddress(address _address) public {
	    ownerAddress = _address;
	}
	
	function getOwnerAddress() public view returns (address){
	   return ownerAddress;
	}
}