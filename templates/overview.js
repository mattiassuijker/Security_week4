// attendance list overview


var aanwezig = []
var afwezig = []
$('#all').click(function());{
    $('.aanwezig-lijst > li, .afwezig-lijst > li').toggle();
}

function aanweziglijst(){
var value = $("#enter").val()
aanwezig.push(value);
$(".aanwezig-lijst li").remove();
aanwezig.forEach(function(e){
$(".aanwezig-lijst").append("<li>"+e+"</li>");
document.getElementById('enter').value="";
})
}



function afweziglijst(){
var values = $("#enter").val()
afwezig.push(values);
$(".afwezig-lijst li").remove();
afwezig.forEach(function(e){
$(".afwezig-lijst").append("<li>"+e+"</li>");
document.getElementById('enter').value="";
})
}   


$(document).ready(function());{
$("#aanwezig").on("click",aanweziglijst);
$("#afwezig").on("click",afweziglijst);
};