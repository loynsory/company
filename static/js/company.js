export function statistic_contract_pic_num() {
    let contract_pic_num = 0;
    $('#uploaderInput_contract').on('change', function (e) {
        let selected_pics = contract_pic_num + e.currentTarget.files
        contract_pic_num = contract_pic_num + selected_pics.length
        $('#contract_num').html(contract_pic_num)
    })
}