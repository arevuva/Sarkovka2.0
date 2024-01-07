/*$(document).ready(function(){
    $('.menu_burger').click(function(event){
        $('.menu_burger, .header_menu').toggleClass('active');
        $('body').toggleClass('_lock')
    });
});
*/
"use strict"

document.addEventListener('DOMContentLoaded', function(){
let burger=document.querySelector('.menu_burger');
let heamenu=document.querySelector('.header_menu');
let body=document.querySelector('body');
burger.addEventListener('click',
function(event){
    burger.classList.toggle('active');
    heamenu.classList.toggle('active');
    body.classList.toggle('lock');
});

let sub_call=document.querySelectorAll('.sub-call');
let call_act=document.querySelector('.call.active');
let phone=document.querySelector('.icon-phone')
let call=document.querySelector('.call');
call.addEventListener('click',
function(e){
  sub_call.forEach(element => element.classList.toggle('active'));
  if(phone.classList.contains("icon-phone")) {
    phone.classList.remove("icon-phone");
    phone.classList.add("icon-cross");
}
else {
    phone.classList.remove("icon-cross");
    phone.classList.add("icon-phone");
}
});

let kat=document.querySelector('#kat');
let slist=document.querySelector('.slide-list');
kat.addEventListener('click',
function(event){
    slist.classList.toggle('mob');
});

//Плавность прокрутки до элемента
const anchors = document.querySelectorAll('a[href*="#kacheli"]');
for (let anchor of anchors){
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    
    const blockID = anchor.getAttribute('href').substr(1);
    
    document.getElementById(blockID).scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    })
  })
};


// считываем кнопку
const goTopBtn = document.querySelector(".go-top");
// обработчик на скролл окна
window.addEventListener("scroll", trackScroll);
// обработчик на нажатии
goTopBtn.addEventListener("click", goTop);
function trackScroll() {
  // вычисляем положение от верхушки страницы
  const scrolled = window.pageYOffset;
  // считаем высоту окна браузера
  const coords = document.documentElement.clientHeight;
  // если вышли за пределы первого окна
  if (scrolled > coords) {
    // кнопка появляется
    goTopBtn.classList.add("go-top--show");
  } else {
    // иначе исчезает
    goTopBtn.classList.remove("go-top--show");
  }
}

function goTop() {
  // пока не вернулись в начало страницы
  if (window.pageYOffset > 0) {
    // скроллим наверх
    window.scrollBy(0, -75); // второй аргумент - скорость
    setTimeout(goTop, 0); // входим в рекурсию
  }
};


let inp = document.getElementById('tel');
// Проверяем фокус
inp.addEventListener('focus', _ => {
  // Если там ничего нет или есть, но левое
  if(!/^\+\d*$/.test(inp.value))
    // То вставляем знак плюса как значение
    inp.value = '+7';
});

inp.addEventListener('keypress', e => {
  // Отменяем ввод не цифр
  if(!/\d/.test(e.key))
    e.preventDefault();
});



$(".gallery-list").magnificPopup({
    delegate: "a",
    type: "image",
    gallery: {
      enabled: true
    }
  });


const form = document.getElementById('form');
const formReq=document.querySelector('._req');
form.addEventListener('submit', function formSend(e){
    e.preventDefault();
    if(formReq.value=="" || formReq.value.length<11){
      alert('Заполните обязательные поля');
    }
    else{
      alert('Заяка отправлена');
      this.submit();
    }
});

//______________________________________________________________________________________________
let items=document.querySelectorAll(".add_item");
let itemId;
console.log(items);
let formInput=document.querySelector('#curitem');
let selectedItems = new Set();

for (var i = 0 ; i < items.length; i++){
  items[i].addEventListener('click', function (e){
    this.closest(".pic_gallery").classList.toggle('active');
    this.closest(".pic_gallery").previousElementSibling.classList.toggle('active');
    this.classList.toggle('active');
    itemId=this.getAttribute("id");
    if(selectedItems.has(itemId)){
      selectedItems.delete(itemId);
    }
    else{
      selectedItems.add(itemId);
    }
    formInput.value=Array.from(selectedItems).join(', ');
});}


})
