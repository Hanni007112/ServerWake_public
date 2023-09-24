function submitChangeForm(id, active){
    changeAllocationForm.id.value = id;
    changeAllocationForm.active.checked = active;
    changeAllocationForm.submit();
}

$(document).ready(function(){
    changeAllocationForm = document.changeAllocationForm
})