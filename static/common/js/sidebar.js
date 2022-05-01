const sidebarToggleTop = document.getElementById('sidebarToggleTop');
const sidebar = document.getElementById('sidebar');
const content = document.getElementById('content');


sidebarToggleTop.addEventListener('click', function(){
    sidebar.classList.toggle('toggled');
    content.classList.toggle('toggled');
});
