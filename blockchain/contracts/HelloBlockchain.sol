// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 < 0.8.0;

contract HelloBlockchain
{
    struct daily_info{
        string visitor_number;
        string male_count;
        string female_count;

        string emotion_neg;
        string emotion_posi;
        string emotion_mild;
        bool is_valid;
        
    }
    mapping (string => daily_info) public dayToNumber;

    function publishData(string memory day, string memory visitor_number,
        string memory male_count,
        string memory female_count,
        string memory emotion_neg,
        string memory emotion_posi,
        string memory emotion_mild) public {
        daily_info memory today = daily_info(visitor_number, male_count,
                            female_count,emotion_neg,emotion_posi,emotion_mild, true);

        dayToNumber[day] = today;
    }
    function getData(string memory day) public view returns(string memory){
        daily_info memory day_info = dayToNumber[day];
        if (day_info.is_valid == false){
            return ("Data not exist!");
        } else {
            return string(abi.encodePacked(day_info.visitor_number," ",day_info.male_count," ",day_info.female_count," ",day_info.emotion_neg," ",day_info.emotion_posi," ",day_info.emotion_mild));
        }
    }

}
