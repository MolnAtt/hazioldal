function GetApi(){
 var a = $.get("https://api.github.com/repos/MolnAtt/LogoKaresz/commits");
 var count = a.length;
 var list = [];

 for (let i = 0; i < $('.biralatdoboz').length; i++) {
     list.push($('.biralatdoboz')[i])
     console.log(list[i]);
     
 }

 
}